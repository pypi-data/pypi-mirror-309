from __future__ import annotations

import logging
import os
import uuid
from dataclasses import replace
from typing import Any, Callable, Iterator, Literal, cast, overload

import numpy as np
from datasets import Dataset
from more_itertools import chunked
from pandas import DataFrame

from .embedding_models import EmbeddingModel
from .memory_types import (
    DatasetLike,
    InputType,
    InputTypeList,
    LabeledMemory,
    LabeledMemoryLookup,
    LabeledMemoryLookupColumnResult,
    LookupReturnType,
)
from .reranker import Reranker
from .storage import MemorysetMetadata, StorageBackend
from .storage_lancedb import LanceDBStorageBackend
from .storage_milvus import MilvusStorageBackend
from .util import transform_data_to_dict_list

logging.basicConfig(level=logging.INFO)


class LabeledMemorysetV2:
    storage_backend: StorageBackend
    embedding_model: EmbeddingModel
    reranker: Reranker | None

    DEFAULT_TABLE_NAME = "memories"

    @staticmethod
    def _is_database_uri(uri: str) -> bool:
        return ".db" in uri or uri.startswith("http")

    @classmethod
    def storage_backend_from_uri(cls, uri: str) -> StorageBackend:
        if not cls._is_database_uri(uri):
            if "MILVUS_URL" in os.environ:
                database_uri = os.environ["MILVUS_URL"]
                logging.info(f"Using `MILVUS_URL` env var for memoryset `{database_uri}#{uri}`")
                return MilvusStorageBackend(uri, database_uri)
            elif "MILVUS_HOST" in os.environ and "MILVUS_PORT" in os.environ:
                database_uri = f"http://{os.environ['MILVUS_HOST']}:{os.environ['MILVUS_PORT']}"
                logging.info(f"Using `MILVUS_HOST` and `MILVUS_PORT` env vars for memoryset `{database_uri}#{uri}`")
                return MilvusStorageBackend(uri, database_uri)
            elif "LANCEDB_URI" in os.environ:
                database_uri = os.environ["LANCEDB_URI"]
                logging.info(f"Using `LANCEDB_URI` env var for memoryset `{database_uri}#{uri}`")
                return LanceDBStorageBackend(uri, database_uri)
            else:
                raise ValueError(
                    "No `MILVUS_URL` or `LANCEDB_URI` environment variable present and URI does not start with `http` or contain `.db`"
                )
        uri = uri.replace("file://", "").replace("file:", "")
        database_uri, table_name = uri.split("#") if "#" in uri else (uri, cls.DEFAULT_TABLE_NAME)
        if "milvus" in database_uri:
            logging.info(f"Inferring Milvus storage backend from URI: {database_uri}")
            return MilvusStorageBackend(table_name, database_uri)
        else:
            logging.info(f"Inferring LanceDB storage backend from URI: {database_uri}")
            return LanceDBStorageBackend(table_name, database_uri)

    @classmethod
    def drop(cls, uri: str):
        """
        Drop the memoryset and its metadata from the database.

        Args:
            uri: URI where the memoryset is stored (e.g. "file:./temp/orca.db#my_memoryset")
        """
        cls.storage_backend_from_uri(uri).drop()

    @classmethod
    def exists(cls, uri: str) -> bool:
        """
        Check if a memoryset exists.

        Args:
            location: URI where the memoryset is stored (e.g. "file:./temp/orca.db#my_memoryset")

        Returns:
            True if the memoryset exists, False otherwise.
        """
        return cls.storage_backend_from_uri(uri).get_metadata() is not None

    def __init__(
        self,
        location: str | StorageBackend,
        embedding_model: EmbeddingModel | None = None,
        reranker: Reranker | None = None,
    ):
        """
        Initialize a labeled memoryset

        Args:
            location: location where the memoryset is stored. Can either be directly a storage
                backend instance, or a URI like `"file:~/.orca/milvus.db#my_memoryset"`, or just a
                table name like `"my_memoryset"` if a `MILVUS_URL` or `LANCEDB_URI` environment
                variable is set.
            embedding_model: Embedding model to use for semantic similarity search. When reconnecting
                to an existing memoryset the correct embedding model will automatically be loaded,
                otherwise an embedding model must be specified.
            reranker: Optional reranker to use for reranking the results of memory lookups.
        """
        unconnected_storage_backend = self.storage_backend_from_uri(location) if isinstance(location, str) else location
        previous_metadata = unconnected_storage_backend.get_metadata()
        if previous_metadata is None:
            if embedding_model is None:
                raise ValueError("Embedding model must be specified when creating a new memoryset.")
            self.embedding_model = embedding_model
            self.metadata = MemorysetMetadata(
                embedding_dim=embedding_model.embedding_dim,
                embedding_model_name=embedding_model.name,
                embedding_model_max_seq_length_overwrite=embedding_model._max_seq_length_overwrite,
            )
        else:
            if embedding_model and embedding_model.name != previous_metadata.embedding_model_name:
                raise ValueError(
                    f"Given embedding model ({embedding_model.name}) does not match previously used embedding model ({previous_metadata.embedding_model_name})."
                )
            self.embedding_model = embedding_model or EmbeddingModel(
                previous_metadata.embedding_model_name,
                max_seq_length=previous_metadata.embedding_model_max_seq_length_overwrite,
            )
            self.metadata = previous_metadata
        self.storage_backend = unconnected_storage_backend.connect(self.metadata)

        # initialize context if the model uses it and there are enough memories
        if self.embedding_model.uses_context and len(self) > 10:
            self.embedding_model.update_context([m.value for m in self.to_list() if isinstance(m.value, str)])

        self.reranker = reranker

    @property
    def uri(self) -> str:
        """URI where the memoryset is stored."""
        return self.storage_backend.database_uri + "#" + self.storage_backend.table_name

    def __repr__(self) -> str:
        return (
            "LabeledMemoryset({\n"
            f"    uri: {self.uri},\n"
            f"    embedding_model: {self.embedding_model},\n"
            f"    num_rows: {len(self)},\n"
            "})"
        )

    @property
    def num_classes(self) -> int:
        """Number of unique labels in the memoryset."""
        return len(set(mem.label for mem in self.to_list()))

    def to_list(self, limit: int | None = None) -> list[LabeledMemory]:
        """
        Get a list of all the memories in the memoryset.

        Args:
            limit: optional maximum number of memories to include in the list

        Returns:
            list containing the memories
        """
        return self.storage_backend.to_list(limit)

    def to_pandas(self, limit: int | None = None) -> DataFrame:
        """
        Get a [DataFrame][pandas.DataFrame] representation of the memoryset.

        Args:
            limit: optional maximum number of memories to include in the dataframe

        Returns:
            DataFrame containing the memories
        """
        return DataFrame(self.to_list(limit))

    def to_dataset(self, limit: int | None = None) -> Dataset:
        """
        Get a [Dataset][datasets.Dataset] representation of the memoryset.

        Args:
            limit: optional maximum number of memories to include in the dataset

        Returns:
            Dataset containing the memories
        """
        return Dataset.from_pandas(self.to_pandas(limit))

    def __len__(self) -> int:
        return len(self.storage_backend)

    @property
    def num_rows(self) -> int:
        """Number of memories in the memoryset."""
        return len(self)

    def __iter__(self) -> Iterator[LabeledMemory]:
        return self.storage_backend.__iter__()

    def insert(
        self,
        dataset: DatasetLike,
        *,
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
            ... ]
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
            if len(transformed_data) > 0 and "text" in transformed_data[0]:
                # This sorts the data by text length so that batches are created from similar length samples
                # This smaller amount of added padding decreases overall computational complexity.
                transformed_data = sorted(
                    transformed_data, key=lambda x: -len(x["text"]) if x["text"] is not None else 0
                )
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

        for item in transformed_data:
            if item["memory_id"] is None:
                item["memory_id"] = str(uuid.uuid4())

        for chunk in chunked(transformed_data, batch_size):
            self.storage_backend.insert(list(chunk))

    @overload
    def lookup(
        self,
        query: InputTypeList | np.ndarray,
        *,
        return_type: Literal[LookupReturnType.ROWS, "rows"] = LookupReturnType.ROWS,
        count: int = 1,
        rerank: bool | None = None,
        use_cache: bool = True,
    ) -> list[list[LabeledMemoryLookup]]:
        pass

    @overload
    def lookup(
        self,
        query: InputType,
        *,
        return_type: Literal[LookupReturnType.ROWS, "rows"] = LookupReturnType.ROWS,
        count: int = 1,
        rerank: bool | None = None,
        use_cache: bool = True,
    ) -> list[LabeledMemoryLookup]:
        pass

    @overload
    def lookup(
        self,
        query: InputTypeList | InputType,
        *,
        return_type: Literal["columns", LookupReturnType.COLUMNS],
        count: int = 1,
        rerank: bool | None = None,
        use_cache: bool = True,
    ) -> LabeledMemoryLookupColumnResult:
        pass

    def lookup(
        self,
        # TODO: remove np.ndarray as query input after migrating to model v2
        query: InputType | InputTypeList | np.ndarray,
        *,
        return_type: LookupReturnType | str = LookupReturnType.ROWS,
        count: int = 1,
        rerank: bool | None = None,
        use_cache: bool = True,
    ) -> list[list[LabeledMemoryLookup]] | list[LabeledMemoryLookup] | LabeledMemoryLookupColumnResult:
        """
        Retrieves the most similar memories to the query from the memoryset.

        Args:
            query: The query to retrieve memories for. Can be a single value or a list of values.
            count: The number of memories to retrieve.
            rerank: Whether to rerank the results. If None (default), results will be reranked if a
                reranker is attached to the Memoryset.
            use_cache: Whether to use the cache to speed up lookups. This controls both reading from the
                cache and storing results in the cache.

        Returns:
            The memory lookup results for the query. If the return type is columns, this will be a
                dictionary of columns containing the embeddings for the inputs and all the query
                results. If a single input value is passed the result will be a list of memory
                lookups. If a list of input values is passed the result will be a list of lists
                of memory lookups.

        Examples:
            Retrieve the most similar memory to a query
            >>> memories = memoryset.lookup("happy")
            [LabeledMemoryLookup(
                value='im feeling quite joyful today',
                label=0,
                embedding=<array.float32(768,)>,
                memory_id=1027,
                memory_version=1,
                lookup_score=0.7021239399909973,
            )]

            Retrieve memories for a batch of queries
            >>> res = memoryset.lookup(["happy", "angry"], count=3, return_type="columns")
            >>> res["memories_values"]
            [['joyful', 'brimming', 'ecstatic'], ['frustrated', 'annoyed', 'disheartened']]
            >>> res["memories_labels"]
            [[0, 0, 0], [1, 1, 1]]
            >>> res["input_embeddings"]
            [array([...], dtype=float32), array([...], dtype=float32)]
            >>> res["memories_embeddings"]
            [[array([...], dtype=float32), array([...], dtype=float32), array([...], dtype=float32)],
             [array([...], dtype=float32), array([...], dtype=float32), array([...], dtype=float32)]]
            >>> res["memories_lookup_scores"]
            [[0.7021238803863525, 0.6859346628189087, 0.6833891272544861],
             [0.7464785575866699, 0.7334979772567749, 0.7299057245254517]]
        """
        # create embedded query matrix of shape num_queries x embedding_dim
        if isinstance(query, np.ndarray):
            embedded_query = query
        elif isinstance(query, list):
            embedded_query = self.embedding_model.embed(query)
        else:
            embedded_query = self.embedding_model.embed([query])

        assert len(embedded_query.shape) == 2, "Query embedding is not in a valid shape"
        assert embedded_query.shape[1] == self.embedding_model.embedding_dim

        # Default reranking to `True` if a reranker is attached and to `False` otherwise.
        rerank = rerank or (rerank is None and self.reranker is not None)
        if rerank:
            if not self.reranker:
                raise ValueError("rerank is set to true but no reranker model has been set on this memoryset")
            count = count * self.reranker.compression

        if count == 0:
            memories_batch = [[] for _ in range(len(embedded_query))]
        elif count > 0:
            memories_batch = self.storage_backend.lookup(embedded_query, k=count, use_cache=use_cache)
        else:
            raise ValueError("count must be greater than or equal to 0")

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
                self.reranker.rerank(q, memories=[cast(str, m.value) for m in ms], top_k=count)
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

    @overload
    def get(self, memory_id: str, exists: Literal[True]) -> LabeledMemory:
        pass

    @overload
    def get(self, memory_id: str, exists: Literal[False] = False) -> LabeledMemory | None:
        pass

    def get(self, memory_id: str, exists: bool = False) -> LabeledMemory | None:
        """
        Get a memory from the memoryset by its UUID.

        Args:
            memory_id: The UUID of the memory to get.
            exists: whether to assert that the memory exists, this will raise an error if the memory
                does not exist and guarantee a LabeledMemory return type otherwise.

        Returns:
            The memory if it exists, otherwise None.

        Raises:
            ValueError: if the memory does not exist and `exists` is True.
        """
        memory = self.storage_backend[memory_id]
        if memory is None and exists:
            raise ValueError(f"Memory with id {memory_id} not found")
        return memory

    def update(self, memory_id: str, updates: dict[str, Any]) -> None:
        """
        Update a memory in the memoryset.

        Notes:
            * The embedding cannot be manually updated, it is automatically recomputed as needed.
            * The version is automatically incremented, it cannot be manually set.

        Args:
            memory_id: The UUID of the memory to update.
            updates: A dictionary containing the values to update in the memory.

        Raises:
            ValueError: if the memory does not exist
        """
        memory = self.get(memory_id, exists=True)
        if "embedding" in updates:
            raise ValueError("Embedding cannot be updated. Memoryset automatically calculates embeddings as needed.")
        if "memory_id" in updates:
            raise ValueError("memory_id cannot be updated.")
        if "memory_version" in updates:
            raise ValueError("memory_version cannot be updated.")
        if "value" in updates and memory.value != updates["value"]:
            # If the value is changing, we need to re-embed it
            updates["embedding"] = self.embedding_model.embed(updates["value"]).reshape(-1)
        if "value" in updates or "label" in updates:
            updates["memory_version"] = memory.memory_version + 1
        transformed_memory = transform_data_to_dict_list(replace(memory, **updates))[0]
        self.storage_backend.upsert(transformed_memory)

    def delete(self, memory_id: str, exists: bool = False) -> None:
        """
        Delete a memory from the memoryset.

        Args:
            memory_id: The UUID of the memory to delete.
            exists: whether to assert that the memory exists, and raise an error otherwise.

        Raises:
            ValueError: if the memory does not exist and `exists` is True.
        """
        if exists:
            self.get(memory_id, exists=True)
        self.storage_backend.delete(memory_id)

    def reset(self):
        """
        Remove all memories from the memoryset and reinitialize it.
        """
        self.storage_backend.reset(self.metadata)

    def _prepare_destination(
        self, destination: str | StorageBackend, embedding_model: EmbeddingModel
    ) -> LabeledMemorysetV2:
        if isinstance(destination, str) and not self._is_database_uri(destination):
            destination = f"{self.storage_backend.database_uri}#{destination}"
        destination_memoryset = LabeledMemorysetV2(destination, embedding_model=embedding_model)
        if destination_memoryset.storage_backend == self.storage_backend:
            raise ValueError("Destination memoryset cannot be the same as the source memoryset.")
        if len(destination_memoryset) > 0:
            raise ValueError("Destination memoryset must be empty.")
        return destination_memoryset

    def filter(
        self,
        fn: Callable[[LabeledMemory], bool],
        destination: str | StorageBackend,
        *,
        log: bool = True,
    ) -> LabeledMemorysetV2:
        """
        Filter memories out from the current memoryset and store them in a new destination.

        Args:
            fn: Function that takes in the memory and returns a boolean indicating whether the
                memory should be included or not.
            destination: location where the filtered memoryset will be stored. Can either be
                a storage backend instance, or a URI like `"file:~/.orca/milvus.db#my_memoryset"`,
                or a table name like `"my_memoryset"` which will be created in the same database as
                the source memoryset.
            log: whether to show a progressbar and log messages

        Returns:
            The memoryset with the filtered memories at the given destination.

        Examples:
            Create a memoryset with a subset of memories that have some metadata:
            >>> memoryset = LabeledMemoryset("./lance.db#my_memoryset")
            >>> filtered_memoryset = memoryset.filter(
            ...     lambda m: m.metadata["key"] == "filter_value",
            ...     "./lance.db#my_filtered_memoryset"
            ... )
        """
        destination_memoryset = self._prepare_destination(destination, self.embedding_model)
        values_to_insert = [m for m in self if fn(m)]
        destination_memoryset.insert(values_to_insert, compute_embeddings=False, log=log)
        return destination_memoryset

    def map(
        self,
        fn: Callable[[LabeledMemory], dict[str, Any]],
        destination: str | StorageBackend,
        *,
        log: bool = True,
    ) -> LabeledMemorysetV2:
        """
        Apply updates to all the memories in the memoryset and store them in a new destination.

        Args:
            fn: Function that takes in the memory and returns a dictionary containing the values to
                update in the memory.
            destination: location where the updated memoryset will be stored. Can either be
                a storage backend instance, or a URI like `"file:~/.orca/milvus.db#my_memoryset"`,
                or a table name like `"my_memoryset"` which will be created in the same database as
                the source memoryset.
            log: whether to show a progressbar and log messages

        Returns:
            The memoryset with the changed memories at the given destination.

        Examples:
            Create a new memoryset with swapped labels
            >>> memoryset = LabeledMemoryset("./lance.db#my_memoryset")
            >>> swapped_memoryset = memoryset.map(
            ...     lambda m: dict(label=1 if m.label == 0 else 0),
            ...     "./lance.db#my_swapped_memoryset"
            ... )
        """
        # TODO: This function calculates embeddings one at a time. It should be optimized to calculate embeddings in batches.

        def replace_fn(memory: LabeledMemory) -> LabeledMemory:
            fn_result = fn(memory)
            if not isinstance(fn_result, dict):
                raise ValueError("Map function must return a dictionary with updates.")
            if "embedding" in fn_result:
                raise ValueError(
                    "Embedding cannot be updated. Memoryset automatically calculates embeddings as needed."
                )
            value_changed = "value" in fn_result and memory.value != fn_result["value"]
            if value_changed:
                fn_result["embedding"] = destination_memoryset.embedding_model.embed(fn_result["value"]).reshape(-1)
                fn_result["memory_version"] = memory.memory_version + 1
            return replace(memory, **fn_result)

        destination_memoryset = self._prepare_destination(destination, self.embedding_model)
        mapped_memories = [replace_fn(memory) for memory in self.to_list()]
        destination_memoryset.insert(mapped_memories, compute_embeddings=False, log=log)
        return destination_memoryset

    def clone(
        self,
        destination: str | StorageBackend,
        *,
        embedding_model: EmbeddingModel | None = None,
        limit: int | None = None,
        batch_size: int = 32,
        log: bool = True,
    ) -> LabeledMemorysetV2:
        """
        Clone the current memoryset into a new memoryset.

        Args:
            destination: location where the copied memoryset will be stored. Can either be
                a storage backend instance, or a URI like `"file:~/.orca/milvus.db#my_memoryset"`,
                or a table name like `"my_memoryset"` which will be created in the same database as
                the source memoryset.
            embedding_model: optional different embedding model to use for the cloned memoryset.
                When provided the memories will be re-embedded using the new embedding model. If not
                provided, the cloned memoryset will use the same embedding model as the current
                memoryset and the embeddings are not recomputed.
            limit: optional maximum number of memories to clone. If not provided, all memories will be cloned.
            batch_size: size of the batches to use for re-embedding the memories
            log: whether to show a progressbar and log messages

        Returns:
            The memoryset that the memories were cloned into at the given destination.

        Examples:
            Clone a local memoryset into a hosted database:
            >>> memoryset = LabeledMemoryset("./lance.db#my_memoryset")
            >>> memoryset.clone("https://my_database.region.milvus.cloud#my_memoryset")

            Clone a local memoryset into a new table with a different embedding model:
            >>> memoryset = LabeledMemoryset("./lance.db#my_memoryset")
            >>> memoryset.clone("./lance.db#my_new_memoryset", embedding_model=EmbeddingModel.CLIP_BASE)
        """
        destination_memoryset = self._prepare_destination(destination, embedding_model or self.embedding_model)
        destination_memoryset.insert(
            self.to_list(limit), batch_size=batch_size, compute_embeddings=bool(embedding_model), log=log
        )
        return destination_memoryset
