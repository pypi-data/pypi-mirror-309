from __future__ import annotations

import json
import logging
from dataclasses import replace
from typing import Any, Callable, Literal, cast, overload

import lancedb
import numpy as np
import pyarrow as pa
from cachetools import TTLCache
from datasets import ClassLabel, Dataset
from pandas import DataFrame
from PIL import Image
from tqdm.auto import tqdm, trange
from typing_extensions import deprecated

from orca_common.api_types import ColumnName, TableCreateMode
from orcalib.database import OrcaDatabase
from orcalib.exceptions import OrcaBadRequestException
from orcalib.orca_types import EnumT, EnumTypeHandle, ImageT, IntT, TextT, VectorT
from orcalib.orcadb_url import OrcaServerLocation, is_url, parse_orcadb_url
from orcalib.rac_util import format_dataset

from .embedding_models import (
    EmbeddingFinetuningMethod,
    EmbeddingModel,
    EmbeddingTrainingArguments,
)
from .memory_types import (
    DatasetLike,
    InputType,
    InputTypeList,
    LabeledMemory,
    LabeledMemoryLookup,
    LabeledMemoryLookupColumnResult,
    LookupReturnType,
)
from .memoryset_analysis import LabeledMemorysetAnalysisResults
from .reranker import (
    MemoryPairsDataset,
    Reranker,
    RerankerTrainingArguments,
    SharedEncoderReranker,
)
from .util import (
    MemoryToInsert,
    bytes_to_pil_image,
    get_embedding_hash,
    pil_image_to_bytes,
    transform_data_to_dict_list,
    transform_rows_to_labeled_memories,
)

# 2 weeks in seconds
CACHE_TTL = 1.21e6


METADATA_TABLE_NAME = "memoryset_metadata"


class LabeledMemoryset:  # TODO (2): metaclass this so we can split out the implementations of local and hosted into separate classes
    """
    Collection of memories with labels that are stored in an OrcaDB table and can be queried using embedding similarity search.
    """

    # TODO(p2): `adapt` method to change embedding models (i.e. re-compute embeddings for the entire dataset with a new model)

    def _get_metadata_table_local(self):
        assert isinstance(self.db, lancedb.DBConnection) and self.mode == "local"

        if METADATA_TABLE_NAME not in self.db.table_names():
            return self.db.create_table(
                METADATA_TABLE_NAME,
                schema=pa.schema(
                    [
                        pa.field("memoryset_table_name", pa.string()),
                        pa.field("embedding_model_name", pa.string()),
                        pa.field("embedding_model_embedding_dim", pa.int64()),
                    ]
                ),
            )
        else:
            return self.db.open_table(METADATA_TABLE_NAME)

    def _load_metadata_local(self) -> tuple[str, int] | None:
        metadata_table = self._get_metadata_table_local()
        metadata_rows = metadata_table.search().where(f"memoryset_table_name == '{self.table_name}'").to_list()
        if len(metadata_rows) == 0:
            return None
        if len(metadata_rows) > 1:
            raise ValueError("found multiple metadata entries for memoryset")
        metadata = metadata_rows[0]
        return metadata["embedding_model_name"], metadata["embedding_model_embedding_dim"]

    def _upsert_metadata_local(self, embedding_model_name: str, embedding_dim: int):
        assert isinstance(self.db, lancedb.DBConnection) and self.mode == "local"
        metadata_table = self.db.open_table(METADATA_TABLE_NAME)
        metadata_table.merge_insert(
            "memoryset_table_name"
        ).when_matched_update_all().when_not_matched_insert_all().execute(
            [
                {
                    "memoryset_table_name": self.table_name,
                    "embedding_model_name": embedding_model_name,
                    "embedding_model_embedding_dim": embedding_dim,
                }
            ]
        )

    def _drop_metadata_local(self):
        metadata_table = self._get_metadata_table_local()
        metadata_table.delete(f"memoryset_table_name == '{self.table_name}'")

    def _get_metadata_table_hosted(self):
        assert isinstance(self.db, OrcaDatabase) and self.mode == "hosted"
        return self.db.create_table(
            METADATA_TABLE_NAME,
            memoryset_table_name=TextT.unique.notnull,
            embedding_model_embedding_dim=IntT,
            embedding_model_name=TextT.notnull,
            embedding_model_version=IntT.notnull,  # not used anymore
            embedding_model_query_prompt=TextT,  # not used anymore
            embedding_model_document_prompt=TextT,  # not used anymore
            if_table_exists=TableCreateMode.RETURN_CURR_TABLE,
        )

    def _load_metadata_hosted(self) -> tuple[str, int] | None:
        metadata_table = self._get_metadata_table_hosted()
        metadata_rows = metadata_table.select().where(metadata_table.memoryset_table_name == self.table_name).fetch()
        if len(metadata_rows) == 0:
            return None
        if len(metadata_rows) > 1:
            raise ValueError("found multiple metadata entries for memoryset")
        metadata = metadata_rows[0]
        return metadata["embedding_model_name"], metadata["embedding_model_embedding_dim"]

    def _upsert_metadata_hosted(self, embedding_model_name: str, embedding_dim: int):
        assert isinstance(self.db, OrcaDatabase) and self.mode == "hosted"
        metadata_table = self._get_metadata_table_hosted()
        metadata_table.upsert(
            {
                "memoryset_table_name": self.table_name,
                "embedding_model_name": embedding_model_name,
                "embedding_model_version": 0,
                "embedding_model_embedding_dim": embedding_dim,
            },
            ["memoryset_table_name"],
        )

    def _drop_metadata_hosted(self):
        metadata_table = self._get_metadata_table_hosted()
        metadata_table.delete(metadata_table.memoryset_table_name == self.table_name)

    def _init_local_db(self):
        """Initializes a local (embedded!) database for storing memories and their embeddings."""
        # TODO: optimize vector index a bit incl supporting CUDA where available (lance has cuda support)

        assert isinstance(self.db, lancedb.DBConnection) and self.mode == "local"

        # create table if it doesn't exist
        if self.table_name not in self.db.table_names():
            _memoryset_schema = pa.schema(
                [
                    pa.field("text", pa.string()),
                    pa.field("image", pa.binary()),
                    pa.field("label", pa.int64()),
                    pa.field("label_name", pa.string()),
                    pa.field("metadata", pa.string()),
                    pa.field("memory_id", pa.string()),
                    pa.field("memory_version", pa.int64()),
                    pa.field(
                        "embedding",
                        pa.list_(pa.float32(), list_size=self.embedding_model.embedding_dim),
                    ),
                ]
            )

            self.db.create_table(self.table_name, schema=_memoryset_schema, exist_ok=True)
            # TODO: add vector index (for more speed - works without it but is slow)

    mode: Literal["local", "hosted"]
    embedding_model: EmbeddingModel

    def _initialize_metadata(self, embedding_model: EmbeddingModel | None = None):
        metadata = self._load_metadata_hosted() if self.mode == "hosted" else self._load_metadata_local()
        if metadata is not None:
            if embedding_model and (embedding_model.name != metadata[0]):
                raise ValueError(
                    f"Given embedding model '{embedding_model.name}' does not match previously used model '{metadata[0]}' for this memoryset"
                )
            self.embedding_model = EmbeddingModel(metadata[0])
        else:
            self.embedding_model = embedding_model or EmbeddingModel.GTE_BASE
            if self.mode == "hosted":
                self._upsert_metadata_hosted(self.embedding_model.name, self.embedding_model.embedding_dim)
            if self.mode == "local":
                self._upsert_metadata_local(self.embedding_model.name, self.embedding_model.embedding_dim)

        if self.mode == "local":
            self._init_local_db()

    def __init__(
        self,
        uri: str | None = None,
        api_key: str | None = None,
        secret_key: str | None = None,
        database: str | None = None,
        table: str | None = None,
        embedding_model: EmbeddingModel | None = None,
        reranker: Reranker | None = None,  # TODO: make this a reranker model enum class instead
    ):
        """
        Create a new LabeledMemoryset.

        Note:
            This will create a database if it doesn't exist yet and a table in it.

        Args:
            uri: URL of the database that should store the memories table or name of the table for
                the memories. Either a file URL or the URL to a hosted OrcaDB instance is accepted.
                If empty, the `ORCADB_URL` environment variable is used instead. If a string is
                provided, it is interpreted as the name of the table to create in the database
                specified by the `ORCADB_URL` environment variable.
            api_key: API key for the OrcaDB instance. If not provided, the `ORCADB_API_KEY`
                environment variable or the credentials encoded in the uri are used
            secret_key: Secret key for the OrcaDB instance. If not provided, the `ORCADB_SECRET_KEY`
                environment variable or the credentials encoded in the uri are used.
            database: Name of the database. Do not provide this if it is already encoded in the `uri`.
            table: Name of the table. Do not provide this if it is already encoded in the `uri`.
            embedding_model: Embedding model to use for semantic similarity search. If not provided,
                will either reload the embedding model from the database if it exists or default to
                the [`GTE-BASE`][orcalib.EmbeddingModel.GTE_BASE] model.
            reranker: optional reranking model to use during lookup.

        Examples:
            Infer connection details from the ORCADB_URL, ORCADB_API_KEY, and ORCADB_SECRET_KEY environment variables:

            >>> import os
            >>> os.environ["ORCADB_URL"] = "https://<my-api-key>:<my-secret-key>@instance.orcadb.cloud/my-db"
            >>> LabeledMemoryset()
            LabeledMemoryset(table="memories", database="my-db")
            >>> LabeledMemoryset("my_memories_table")
            LabeledMemoryset(table="my_memories_table", database="my-db")

            All connection details can be fully encoded in the the uri:

            >>> LabeledMemoryset("https://<my-api-key>:<my-secret-key>@instance.orcadb.cloud/my-db/my-memories-table")
            LabeledMemoryset(table="my-memories-table", database="my-db")

            Or they can be provided explicitly:

            >>> LabeledMemoryset(
            ...    "https://instance.orcadb.cloud",
            ...    api_key="my-api-key",
            ...    secret_key="my-secret-key",
            ...    database="my-db",
            ...    table="my-memories-table"
            ... )
            LabeledMemoryset(table="my-memories-table", database="my-db")
        """
        self.table = None
        self.index = None
        self.reranker = reranker
        self.cache = TTLCache(maxsize=25000, ttl=CACHE_TTL)

        self._location = parse_orcadb_url(
            uri if is_url(uri) else None,
            api_key=api_key,
            secret_key=secret_key,
            database=database,
            table=table if is_url(uri) else (table or uri),
        )
        if not self._location.table:
            self._location.table = "memories"
        self.url = self._location.url
        self.table_name = self._location.table
        if isinstance(self._location, OrcaServerLocation):
            self.mode = "hosted"
            self.database_name = self._location.database
            self.db = OrcaDatabase(
                self._location.base_url,
                api_key=self._location.api_key,
                secret_key=self._location.secret_key,
                name=self._location.database,
            )
        else:
            self.mode = "local"
            self.path = self._location.path
            self.db = lancedb.connect(self.path)

        self._initialize_metadata(embedding_model)
        # initialize context if the model uses it and there are enough memories
        if self.embedding_model.uses_context and len(self) > 10:
            self.embedding_model.update_context([m.value for m in self.to_list() if isinstance(m.value, str)])

    @property
    def num_classes(self) -> int:
        """The number of unique labels present in the memoryset."""
        return len(set(mem.label for mem in self.to_list()))

    def __repr__(self) -> str:
        return "".join(
            [
                "LabeledMemoryset({\n",
                f"    uri: {self.url.split('#')[0]},\n",
                f"    table_name: {self.table_name},\n",
                f"    embedding_model: {self.embedding_model},\n",
                f"    num_rows: {len(self)}\n",
                "})",
            ]
        )

    def _insert_local(self, data: list[MemoryToInsert]):
        assert self.mode == "local" and isinstance(self.db, lancedb.DBConnection)
        if len(data) > 0:
            for d in data:
                if d["image"] is not None:
                    d["image"] = pil_image_to_bytes(d["image"])  # type: ignore -- we need to transform this to insert it
            self.db.open_table(self.table_name).add(data)

    def _insert_hosted(self, data: list[MemoryToInsert], label_col_type: EnumTypeHandle | None = None):
        assert self.mode == "hosted" and isinstance(self.db, OrcaDatabase)

        if not self.table:
            self.table = self.db.create_table(
                self.table_name,
                text=TextT,
                image=ImageT["PNG"],  # type: ignore -- ImageT takes a format param
                memory_id=TextT,
                memory_version=IntT,
                label=label_col_type or IntT,
                label_name=TextT,
                metadata=TextT,
                embedding=VectorT[self.embedding_model.embedding_dim],
                if_table_exists=TableCreateMode.RETURN_CURR_TABLE,
            )
            self.index = self.db.create_vector_index(
                index_name=f"{self.table_name}_embedding_index",
                table_name=self.table_name,
                column="embedding",
                error_if_exists=False,
            )
            if self.index is None:
                logging.info(f"Using existing {self.table_name}_embedding_index")
                self.index = self.db.get_index(f"{self.table_name}_embedding_index")

        # table.insert takes in list of dicts and we must leave off image if there is no data for it or we will get an error
        data_to_insert = [cast(dict, mem) for mem in data]
        for mem in data_to_insert:
            if mem["image"] is None:
                del mem["image"]
        self.table.insert(data_to_insert)

    def insert(
        self,
        dataset: DatasetLike,
        log: bool = True,
        compute_embeddings: bool = True,
        batch_size: int = 32,
        only_if_empty: bool = False,
    ):
        """
        Inserts a dataset into the LabeledMemoryset database.

        For dict-like or list of dict-like datasets, there must be a `label` key and one of the following keys: `text`, `image`, or `value`.
        If there are only two keys and one is `label`, the other will be inferred to be `value`.

        For list-like datasets, the first element of each tuple must be the value and the second must be the label.

        Args:
            dataset: data to insert into the memoryset
            log: whether to show a progressbar and log messages
            compute_embeddings: whether to compute embeddings for the dataset or take them from the dataset
            batch_size: the batch size when creating embeddings from memories
            only_if_empty: whether to skip the insert if the memoryset is not empty
        Examples:
            # Example 1: Inserting a dictionary-like dataset
            >>> dataset = [{
            ...    "text": "text 1",
            ...    "label": 0
            ... }]
            >>> memoryset = LabeledMemoryset("file:///path/to/memoryset")
            >>> memoryset.insert(dataset)

            # Example 2: Inserting a list-like dataset
            >>> dataset = [
            ...    ("text 1", 0),
            ...    ("text 2", 1)
            ]
            >>> memoryset = LabeledMemoryset("file:///path/to/memoryset")
            >>> memoryset.insert(dataset)

            # Example 3: Inserting a Hugging Face Dataset
            from datasets import Dataset
            >>> dataset = load_dataset("frgfm/imagenette", "320px")
            >>> memoryset = LabeledMemoryset("file:///path/to/memoryset")
            >>> memoryset.insert(dataset)
        """
        if len(self) and only_if_empty:
            logging.warning("Skipping insert: `only_if_empty` is True and memoryset is not empty.") if log else None
            return
        transformed_data = transform_data_to_dict_list(dataset)
        if len(transformed_data) > 0 and "text" in transformed_data[0]:
            # This sorts the data by text length so that batches are created from similar length samples
            # This smaller amount of added padding decreases overall computational complexity.
            transformed_data = sorted(transformed_data, key=lambda x: -len(x["text"]) if x["text"] is not None else 0)

        if self.embedding_model.uses_context:
            # if the dataset changes by more than 20% and at least 10 items then update the context
            current_size = len(self)
            if len(transformed_data) > 10 and len(transformed_data) > current_size / 5:
                self.embedding_model.update_context(
                    [m["text"] for m in transformed_data if m["text"] is not None]
                    + (
                        [m.value for m in self.to_list() if m.value is not None and isinstance(m.value, str)]
                        if current_size > 0
                        else []
                    )
                )

        if compute_embeddings:
            # Add embeddings to the transformed data
            embeddings = self.embedding_model.embed(
                cast(InputTypeList, [mem["text"] or mem["image"] for mem in transformed_data]),
                show_progress_bar=log,
                value_kind="document",
                batch_size=batch_size,
            )
            for item, embedding in zip(transformed_data, embeddings):
                item["embedding"] = embedding.tolist()
        else:
            if not all(item["embedding"] is not None for item in transformed_data):
                raise ValueError("Embedding must be provided if compute_embeddings is False.")

        if self.mode == "local":
            self._insert_local(transformed_data)
        elif self.mode == "hosted":
            label_col_type = (
                EnumT[dataset.features["label"].names]
                if isinstance(dataset, Dataset) and isinstance(dataset.features["label"], ClassLabel)
                else None
            )
            self._insert_hosted(transformed_data, label_col_type=label_col_type)
        else:
            raise Exception("Memoryset not initialized correctly")

    def _lookup_local(
        self, query: np.ndarray, k: int, log: bool, cache_disabled: bool
    ) -> list[list[LabeledMemoryLookup]]:
        assert self.mode == "local"

        def single_lookup(q: np.ndarray) -> list[LabeledMemoryLookup]:
            assert isinstance(self.db, lancedb.DBConnection)

            cache_key = (get_embedding_hash(q), k)
            result = self.cache.get(cache_key, None) if not cache_disabled else None

            if result is None:
                result = self.db.open_table(self.table_name).search(q).limit(k).to_list()
                if not cache_disabled:
                    self.cache[cache_key] = result

            return [
                LabeledMemoryLookup(
                    value=bytes_to_pil_image(row["image"]) if row["image"] is not None else row["text"],
                    embedding=np.array(row["embedding"], dtype=np.float32),
                    memory_id=row["memory_id"],
                    memory_version=row["memory_version"],
                    label=row["label"],
                    label_name=row["label_name"],
                    metadata=json.loads(row["metadata"]) if row["metadata"] is not None else {},
                    lookup_score=float(np.dot(q, np.array(row["embedding"]))),  # Calculate inner product
                )
                for row in result
            ]

        assert len(query.shape) == 2
        return [single_lookup(q) for q in tqdm(query, disable=not log or len(query) <= 100)]

    def _lookup_hosted(
        self,
        query: np.ndarray,
        k: int,
        batch_size: int,
        run_ids: list[int] | None,
        log: bool,
        cache_disabled: bool,
    ) -> list[list[LabeledMemoryLookup]]:
        assert self.mode == "hosted" and isinstance(self.db, OrcaDatabase)
        if self.table is None:
            try:
                self.table = self.db.get_table(self.table_name)
            except ValueError:
                raise ValueError(
                    f"Table '{self.table_name}' not found in database '{self.database_name}'. Please call insert to create table and add data."
                )
        if self.index is None:
            try:
                self.index = self.db.get_index(f"{self.table_name}_embedding_index")
            except OrcaBadRequestException:
                raise ValueError(
                    f"Index '{self.table_name}_embedding_index' not found in table '{self.table_name}'. Please call insert first to create the index."
                )

        assert len(query.shape) == 2
        query_list = [(idx, q) for idx, q in enumerate(query)]

        # save results in a list of tuples where the first element is the query index and the second element is the result
        all_results: list[tuple[int, list[LabeledMemoryLookup]]] = []

        # run_ids are only set if we have enabled curate tracking in which case caching is not possible
        if not run_ids:
            for q in query_list:
                cache_key = (get_embedding_hash(q[1]), k)
                result = self.cache.get(cache_key, None) if not cache_disabled else None
                if result is not None:
                    all_results.append((q[0], result))
                    query_list.remove(q)

        for i in trange(0, len(query_list), batch_size, disable=(not log) or (len(query_list) <= 5 // batch_size)):
            batch = query_list[i : i + (batch_size or len(query_list))]
            batch_list = [q[1].tolist() for q in batch]
            index_query = self.index.vector_scan(batch_list).select(
                "metadata",  # 0
                "image",  # 1
                "text",  # 2
                "label",  # 3
                "label_name",  # 4
                "memory_version",  # 5
                "$embedding",  # 6
                "$row_id",  # 7
                "$score",  # 8
            )
            if run_ids:
                batch_run_ids = run_ids[i : i + (batch_size or len(query_list))]
                index_query = index_query.track_with_curate(batch_run_ids, "rac_lookup")
            results_batch = index_query.fetch(k).to_list()
            formatted_results = [
                [
                    LabeledMemoryLookup(
                        value=(
                            (bytes_to_pil_image(row[1]) if isinstance(row[1], bytes) else cast(Image.Image, row[1]))
                            if row[1] is not None
                            else cast(str, row[2])
                        ),
                        embedding=np.array(row[6]),
                        memory_id=row[7],
                        memory_version=row[5],
                        label=row[3],
                        label_name=row[4],
                        metadata=json.loads(row[0]) if row[0] is not None else {},
                        lookup_score=row[8],
                    )
                    for row in batch
                ]
                for batch in results_batch
            ]

            for idx, result in enumerate(formatted_results):
                cache_key = (get_embedding_hash(batch[idx][1]), k)
                if not cache_disabled:
                    self.cache[cache_key] = result
                all_results.append((batch[idx][0], result))

        all_results.sort(key=lambda x: x[0])
        return [x[1] for x in all_results]

    @overload
    def lookup(
        self,
        query: InputTypeList | np.ndarray,
        *,
        return_type: Literal[LookupReturnType.ROWS, "rows"] = LookupReturnType.ROWS,
        k: int = 1,
        batch_size: int = 32,
        run_ids: list[int] | None = None,
        rerank: bool | None = None,
        log: bool = False,
        cache: bool = True,
    ) -> list[list[LabeledMemoryLookup]]:
        pass

    @overload
    def lookup(
        self,
        query: InputType,
        *,
        return_type: Literal[LookupReturnType.ROWS, "rows"] = LookupReturnType.ROWS,
        k: int = 1,
        batch_size: int = 32,
        run_ids: list[int] | None = None,
        rerank: bool | None = None,
        log: bool = False,
        cache: bool = True,
    ) -> list[LabeledMemoryLookup]:
        pass

    @overload
    def lookup(
        self,
        query: InputTypeList,
        *,
        return_type: Literal["columns", LookupReturnType.COLUMNS],
        k: int = 1,
        batch_size: int = 32,
        run_ids: list[int] | None = None,
        rerank: bool | None = None,
        log: bool = False,
        cache: bool = True,
    ) -> LabeledMemoryLookupColumnResult:
        pass

    def lookup(
        self,
        query: InputType | InputTypeList | np.ndarray,
        *,
        return_type: LookupReturnType | str = LookupReturnType.ROWS,
        k: int = 1,
        batch_size: int = 32,
        run_ids: list[int] | None = None,
        rerank: bool | None = None,
        log: bool = False,
        cache: bool = True,
    ) -> list[list[LabeledMemoryLookup]] | list[LabeledMemoryLookup] | LabeledMemoryLookupColumnResult:
        """
        Retrieves the most similar memories to the query from the memoryset.

        Args:
            query: The query to retrieve memories for. Can be a single value, a list of values, or a numpy array with value embeddings.
            k: The number of memories to retrieve.
            batch_size: The number of queries to process at a time.
            run_ids: A list of run IDs to track with the lookup.
            rerank: Whether to rerank the results. If None (default), results will be reranked if a reranker is attached to the Memoryset.
            log: Whether to log the lookup process and show progress bars.

        Returns:
            A list of lists of LabeledMemoryLookups, where each inner list contains the k most similar memories to the corresponding query.

        Examples:
            # Example 1: Retrieving the most similar memory to a single example
            >>> memoryset = LabeledMemoryset("file:///path/to/memoryset")
            >>> query = "Apple"
            >>> memories = memoryset.lookup(query, k=1)
            [
                LabeledMemoryLookup(
                    value='Orange',
                    memory_id=12,
                    memory_version=1,
                    label=0,
                    label_name='fruit',
                    embedding=array([...], dtype=float32),
                    metadata=None,
                    lookup_score=.98,
                    reranker_score=None,
                    reranker_embedding=None
                )
            ]
        """
        # create embedded query matrix of shape num_queries x embedding_dim
        if isinstance(query, np.ndarray):
            embedded_query = query if len(query.shape) == 2 else np.array([query])
        else:
            embedded_query = self.embedding_model.embed(query if isinstance(query, list) else [query])
        assert len(embedded_query.shape) == 2, "Query embedding is not in a valid shape"
        assert embedded_query.shape[1] == self.embedding_model.embedding_dim

        # Default reranking to `True` if a reranker is attached and to `False` otherwise.
        rerank = rerank or (rerank is None and self.reranker is not None)
        if rerank:
            if not self.reranker:
                raise ValueError("rerank is set to true but no reranker model has been set on this memoryset")
            k = k * self.reranker.compression

        # perform the lookup
        if k == 0:
            memories_batch = [[] for _ in range(len(embedded_query))]
        elif self.mode == "local":
            memories_batch = self._lookup_local(embedded_query, k=k, log=log, cache_disabled=not cache)
        elif self.mode == "hosted":
            memories_batch = self._lookup_hosted(
                embedded_query, k=k, batch_size=batch_size, run_ids=run_ids, log=log, cache_disabled=not cache
            )
        else:
            raise Exception("Memoryset not initialized correctly")

        # rerank the results if necessary
        if rerank:
            assert self.reranker is not None
            if isinstance(query, str):
                queries_list = [query]
            else:
                if not isinstance(query, list) or not isinstance(query[0], str):
                    raise ValueError("reranking only works when passing a string as the query")
                queries_list = cast(list[str], query)
            # TODO: use cached reranker embeddings if available
            reranked_results = [
                self.reranker.rerank(q, memories=[cast(str, m.value) for m in ms], top_k=k)
                for q, ms in zip(queries_list, memories_batch)
            ]
            memories_batch = [
                [
                    LabeledMemoryLookup(
                        reranker_score=reranked_results[j].scores[idx],
                        # TODO: add reranker embedding
                        **memories_batch[j][idx].__dict__,
                    )
                    for idx in reranked_results[j].indices
                ]
                for j in range(len(reranked_results))
            ]

        # return correctly formatted results
        if return_type == "columns":
            return LabeledMemoryLookupColumnResult(
                input_embeddings=[e for e in embedded_query],
                memories_values=[[m.value for m in memories] for memories in memories_batch],
                memories_labels=[[m.label for m in memories] for memories in memories_batch],
                memories_embeddings=[[m.embedding for m in memories] for memories in memories_batch],
                memories_ids=[[m.memory_id for m in memories] for memories in memories_batch],
                memories_versions=[[m.memory_version for m in memories] for memories in memories_batch],
                memories_metadata=[[m.metadata for m in memories] for memories in memories_batch],
                memories_lookup_scores=[[m.lookup_score for m in memories] for memories in memories_batch],
                memories_reranker_scores=[[m.reranker_score for m in memories] for memories in memories_batch],
            )

        if not isinstance(query, list) and not isinstance(query, np.ndarray):
            assert len(memories_batch) == 1
            return memories_batch[0]

        return memories_batch

    def to_list(self, limit: int | None = None) -> list[LabeledMemory]:
        """
        Get a list of all the memories in the memoryset.

        Returns:
            list containing the memories
        """
        if self.mode == "local" and isinstance(self.db, lancedb.DBConnection):
            return transform_rows_to_labeled_memories(
                self.db.open_table(self.table_name).search().limit(limit).to_list()
            )
        elif self.mode == "hosted" and isinstance(self.db, OrcaDatabase):
            if self.table is None:
                try:
                    self.table = self.db.get_table(self.table_name)
                except ValueError:
                    raise ValueError(
                        f"Table '{self.table_name}' not found in database '{self.database_name}'. Please call insert to create table and add data."
                    )
            return transform_rows_to_labeled_memories(
                cast(list[tuple[int, dict[ColumnName, Any]]], self.table.select().fetch(limit=limit, include_ids=True))
            )
        else:
            raise Exception("Memoryset not initialized correctly")

    def to_pandas(self, limit: int | None = None) -> DataFrame:
        """
        Get a [DataFrame][pandas.DataFrame] representation of the memoryset.

        Returns:
            DataFrame containing the memories
        """
        return DataFrame(self.to_list(limit))

    def to_dataset(self, limit: int | None = None) -> Dataset:
        return Dataset.from_pandas(self.to_pandas(limit))

    def __getitem__(self, idx: int) -> LabeledMemory:
        return self.to_list()[idx]

    def __len__(self) -> int:
        if self.mode == "local" and isinstance(self.db, lancedb.DBConnection):
            return self.db.open_table(self.table_name).count_rows()
        elif self.mode == "hosted" and isinstance(self.db, OrcaDatabase):
            return self.db[self.table_name].count() if self.table_name in self.db else 0
        else:
            raise Exception("Memoryset not initialized correctly")

    @property
    def num_rows(self) -> int:
        return len(self)

    def _get_reset_destination_memoryset(
        self, destination: LabeledMemoryset | str | None, embedding_model: EmbeddingModel | None = None
    ) -> LabeledMemoryset:
        """Gets destination memoryset, RESETS THE DESTINATION MEMORYSET IF IT ALREADY EXISTS"""
        # If destination is None or matches self, return self
        if destination is None or (
            (isinstance(destination, LabeledMemoryset) and destination.url == self.url)
            or ((isinstance(destination, str) and (destination == self.url or destination == self.table_name)))
        ):
            destination = self
            if embedding_model is not None:
                self.drop_table()
                self.embedding_model = embedding_model
                self._initialize_metadata(embedding_model)
        elif isinstance(destination, str):
            if not is_url(destination):
                self.drop_table(destination)
            destination = LabeledMemoryset(
                destination if is_url(destination) else self.url.split("#")[0],
                table=None if is_url(destination) else destination,
                api_key=(
                    self._location.api_key
                    if self.mode == "hosted" and isinstance(self._location, OrcaServerLocation)
                    else None
                ),
                secret_key=(
                    self._location.secret_key
                    if self.mode == "hosted" and isinstance(self._location, OrcaServerLocation)
                    else None
                ),
                embedding_model=self.embedding_model if embedding_model is None else embedding_model,
                reranker=self.reranker,
            )

        destination.reset()
        return destination

    def update_embedding_model(
        self, embedding_model: EmbeddingModel, destination: LabeledMemoryset | str | None = None, batch_size: int = 32
    ) -> LabeledMemoryset:
        """
        Updates the embedding model for the memoryset and re-embeds all memories in the current
        memoryset or a new destination memoryset if it is provided.

        Note:
            This will reset the destination memoryset if it already exists.

        Args:
            embedding_model: new embedding model to use.
            destination: destination memoryset to store the results in, this can either be
                a memoryset instance, or the URL to a new memoryset, or the name of a table in the
                same database. A table for the destination will be created if it does not already
                exist. It this is `None` the current memoryset will be updated.
            batch_size: size of the batches to use for embedding updates

        Returns:
            The destination memoryset with the updated embeddings.

        Examples:
            Replace the embedding model for the current memoryset:
            >>> memoryset = LabeledMemoryset("file:./orca.db#my_memoryset")
            >>> memoryset.update_model(EmbeddingModel.CLIP_BASE)

            Create a new memoryset with a new embedding model:
            >>> memoryset = LabeledMemoryset("file:./orca.db#my_memoryset")
            >>> new_memoryset = memoryset.update_model(EmbeddingModel.CLIP_BASE, "my_new_memoryset")
        """
        memories = self.to_list()
        destination = self._get_reset_destination_memoryset(destination, embedding_model)
        destination.insert(memories, batch_size=batch_size)
        return destination

    def clone(self, destination: LabeledMemoryset | str) -> LabeledMemoryset:
        """
        Clone the current memoryset into a new memoryset.

        Note:
            This will reset the destination memoryset if it already exists.

        Args:
            destination: The destination memoryset to clone this memoryset into, this can either be
                a memoryset instance, or the URL to a new memoryset, or the name of a table in the
                same database. A table for the destination will be created if it does not already
                exist.

        Returns:
            The destination memoryset that the memories were cloned into.

        Examples:
            Clone a local memoryset into a hosted database:
            >>> memoryset = LabeledMemoryset("file:./orca.db#my_memoryset")
            >>> memoryset.clone("https://<my-api-key>:<my-secret-key>@instance.orcadb.cloud/my-database#my_memoryset")

            Clone a local memoryset into a new table in the same database:
            >>> memoryset = LabeledMemoryset("file:./orca.db#my_memoryset")
            >>> memoryset.clone("my_new_memoryset")
        """
        memories = self.to_list()
        destination = self._get_reset_destination_memoryset(destination)
        if destination.url == self.url:
            logging.info("Warning: Source and destination are the same. No data will be cloned.")
            return self
        destination.insert(memories, compute_embeddings=self.embedding_model != destination.embedding_model)
        return destination

    def map(
        self,
        fn: Callable[[LabeledMemory], dict[str, Any] | LabeledMemory],
        destination: LabeledMemoryset | str | None = None,
    ) -> LabeledMemoryset:
        """
        Apply a function to all the memories in the memoryset and store them in the current
        memoryset or a new destination memoryset if it is provided.

        Note:
            If your function returns a column that already exists, then it overwrites it.

        Args:
            fn: Function that takes in the memory and returns a new memory or a dictionary
                containing the values to update in the memory.
            destination: The destination memoryset to store the results in, this can either be
                a memoryset instance, or the URL to a new memoryset, or the name of a table in the
                same database. A table for the destination will be created if it does not already
                exist.

        Returns:
            The destination memoryset with the updated memories.

        Examples:
            Add new metadata to all memories in the memoryset:
            >>> memoryset = LabeledMemoryset("file:./orca.db#my_memoryset")
            >>> memoryset.map(lambda m: dict(metadata=dict(**m.metadata, new_key="new_value")))

            Create a new memoryset with swapped labels in a new table in the same database:
            >>> memoryset = LabeledMemoryset("file:./orca.db#my_memoryset")
            >>> swapped_memoryset = memoryset.map(
            ...     lambda m: dict(label=1 if m.label == 0 else 0),
            ...     "my_swapped_memoryset"
            ... )
        """
        memories = self.to_list()
        destination = self._get_reset_destination_memoryset(destination)

        compute_embeddings = self.embedding_model != destination.embedding_model if destination else True

        def replace_fn(memory: LabeledMemory) -> LabeledMemory:
            result = fn(memory)
            # recompute embedding if the value has changed and the embedding was not provided
            if not compute_embeddings and memory.value != result["value"] and "embedding" not in result:
                result["embedding"] = destination.embedding_model.embed(result["value"])
            return result if isinstance(result, LabeledMemory) else replace(memory, **result)

        mapped_memories = [replace_fn(memory) for memory in memories]
        destination.insert(mapped_memories, compute_embeddings=compute_embeddings)
        return destination

    def filter(
        self, fn: Callable[[LabeledMemory], bool], destination: LabeledMemoryset | str | None = None
    ) -> LabeledMemoryset:
        """
        Filters the current memoryset using the given function and stores the result in the current
        memoryset or a new destination memoryset if it is provided.

        Note:
            This will reset the destination memoryset if it already exists.

        Args:
            fn: Function that takes in the memory and returns a boolean indicating whether the
                memory should be included or not.
            destination: The destination memoryset to store the results in, this can either be
                a memoryset instance, or the URL to a new memoryset, or the name of a table in the
                same database. A table for the destination will be created if it does not already
                exist.

        Returns:
            The destination memoryset with the filtered memories.

        Examples:
            Filter out memories with a label of 0:
            >>> memoryset = LabeledMemoryset("file:./orca.db#my_memoryset")
            >>> memoryset.filter(lambda m: m.label != 0)

            Create a new memoryset with some metadata in a new table in the same database:
            >>> memoryset = LabeledMemoryset("file:./orca.db#my_memoryset")
            >>> filtered_memoryset = memoryset.filter(
            ...     lambda m: m.metadata["key"] == "filter_value",
            ...     "my_filtered_memoryset"
            ... )
        """
        filtered_memories = [memory for memory in self.to_list() if fn(memory)]
        destination = self._get_reset_destination_memoryset(destination)
        destination.insert(filtered_memories, compute_embeddings=self.embedding_model != destination.embedding_model)
        return destination

    def finetune_reranker(
        self,
        data: DatasetLike,
        save_dir: str,
        training_args: RerankerTrainingArguments = RerankerTrainingArguments(),
        num_memories: int = 9,  # TODO: unify this default with the rac memory_lookup_count
    ) -> None:
        if self.reranker is None:
            self.reranker = SharedEncoderReranker("Alibaba-NLP/gte-base-en-v1.5")
        pairs_dataset = MemoryPairsDataset(
            samples=cast(list[tuple[str, int]], format_dataset(data)),
            lookup_fn=lambda query, num_memories: [
                (cast(str, memory.value), memory.label) for memory in self.lookup(query, k=num_memories)
            ],
            num_memories=num_memories * self.reranker.compression,
        )
        self.reranker.finetune(save_dir, pairs_dataset, training_args)
        # TODO: save reranker embeddings to database

    def finetune_embedding_model(
        self,
        save_dir: str,
        destination: LabeledMemoryset | str | None = None,
        training_args: EmbeddingTrainingArguments | None = None,
        train_data: DatasetLike | None = None,
        eval_data: DatasetLike | None = None,
        method: EmbeddingFinetuningMethod | str = EmbeddingFinetuningMethod.CLASSIFICATION,
        batch_size: int = 32,
    ):
        """
        Finetunes the embedding model for the memoryset.

        Note:
            This will reset the destination memoryset if it already exists.

        Args:
            save_dir: The directory to save the finetuned model to.
            destination: The destination memoryset to store the results in, this can either be
                a memoryset instance, or the URL to a new memoryset, or the name of a table in the
                same database. A table for the destination will be created if it does not already
                exist. If this is `None` the current memoryset will be used.
            training_args: The training arguments to use for the finetuning. If this is `None`
                sensible defaults will be used based on the finetuning method.
            train_data: The data to finetune on, if this is `None` the memories from the current
                memoryset will be used.
            eval_data: The data to evaluate the finetuned model on, if this is `None` a 10% holdout
                from the training data will be used.
            method: The method to use for finetuning, "triplets" uses a contrastive triplet loss to pull
            batch_size: size of the batches to use for embedding updates

        Returns:
            The destination memoryset with the finetuned embedding model. All memories will be
            re-embedded using the finetuned model.
        """
        finetuned_embedding_model = self.embedding_model.finetune(
            save_dir, train_data or self.to_dataset(), eval_data, training_args, method
        )
        return self.update_embedding_model(finetuned_embedding_model, destination, batch_size)

    def drop_table(self, table_name: str | None = None):
        """
        Drop the table associated with this Memoryset.
        """
        if self.mode == "local" and isinstance(self.db, lancedb.DBConnection):
            try:
                self.db.drop_table(table_name or self.table_name)
            except FileNotFoundError:
                pass
            self._drop_metadata_local()
        elif self.mode == "hosted" and isinstance(self.db, OrcaDatabase):
            self.db.drop_table(table_name or self.table_name, error_if_not_exists=False)
            self._drop_metadata_hosted()
            self.table = None
        else:
            raise Exception("Memoryset not initialized correctly")

    def reset(self):
        """
        Drop all data from the table associated with this Memoryset.
        """
        if self.cache is not None:
            self.cache.clear()
        self.drop_table()
        self._initialize_metadata(self.embedding_model)

    @deprecated("Use reset instead")
    def _drop_database(self, *, yes_i_am_sure: bool = False):
        """
        Drop the whole database that the table associated with this Memoryset lives in.
        """

        if not yes_i_am_sure:
            logging.warning("This will delete all data in the database. If you are sure, set `yes_i_am_sure` to True.")
        if self.mode == "local" and isinstance(self.db, lancedb.DBConnection):
            self.db.drop_database()
        elif self.mode == "hosted" and isinstance(self.db, OrcaDatabase):
            self.db.drop()
        else:
            raise Exception("Memoryset not initialized correctly")

    def analyze(self, log: bool = True) -> LabeledMemorysetAnalysisResults:
        memoryset = self.to_list()
        return LabeledMemorysetAnalysisResults(memoryset, lambda q, k: self.lookup(q, k=k), log)
