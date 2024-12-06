from __future__ import annotations

import base64
import io
import json
import logging
import os
from typing import Any, Iterator

import numpy as np
from PIL import Image
from pymilvus import DataType, MilvusClient

from .memory_types import LabeledMemory, LabeledMemoryLookup
from .storage import CACHE_SIZE, CACHE_TTL, MemorysetMetadata, StorageBackend
from .util import MemoryToInsert

METRIC_TYPE = "IP"  # We always use inner product similarity because we use normalize embeddings


# TODO: Replace this once Milvus supports null values for scalar fields: https://github.com/milvus-io/milvus/issues/31728


def _none_to_empty(value: Any | None, klass) -> Any:
    if klass == str:
        return value if value is not None else ""
    elif klass == int:
        return value if value is not None else -1
    elif klass == float:
        return value if value is not None else float("nan")
    elif klass == dict:
        return value if value is not None else {}
    elif klass == list:
        return value if value is not None else []
    elif klass == bytes:
        return value if value is not None else ""
    else:
        raise ValueError(f"Unsupported class {klass}")


def _empty_to_none(value: Any, klass) -> Any:
    if klass == str:
        return value if value != "" else None
    elif klass == int:
        return value if value != -1 else None
    elif klass == float:
        return value if value != float("nan") else None
    elif klass == dict:
        return value if value != {} else None
    elif klass == list:
        return value if value != [] else None
    else:
        raise ValueError(f"Unsupported class {klass}")


def _encode_image(image: Image.Image) -> str:
    buffer = io.BytesIO()
    image.save(buffer, format=image.format)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def _decode_image(image_str: str) -> Image.Image:
    return Image.open(io.BytesIO(base64.b64decode(image_str)))


def _prepare_for_insert(datum: MemoryToInsert) -> dict[str, Any]:
    assert datum["memory_id"] is not None
    assert datum["embedding"] is not None
    assert datum["text"] is not None or datum["image"] is not None
    return {
        "text": _none_to_empty(datum["text"], str),
        "image": _encode_image(datum["image"]) if datum["image"] is not None else "",
        "label": _none_to_empty(datum["label"], int),
        "label_name": _none_to_empty(datum["label_name"], str),
        "metadata": datum["metadata"] or "{}",
        "memory_id": datum["memory_id"],
        "memory_version": datum["memory_version"],
        "embedding": _none_to_empty(datum["embedding"], list),
    }


def _to_labeled_memory(row: dict[str, Any]) -> LabeledMemory:
    return LabeledMemory(
        embedding=np.array(row["embedding"], dtype=np.float32),
        label_name=_empty_to_none(row["label_name"], str),
        label=row["label"],
        memory_id=row["memory_id"],
        memory_version=row["memory_version"],
        metadata=json.loads(row["metadata"]) if row["metadata"] is not None else {},
        value=_decode_image(row["image"]) if row["image"] is not None and row["image"] != "" else row["text"],
    )


def _to_labeled_memory_lookup(row: dict[str, Any]) -> LabeledMemoryLookup:
    return LabeledMemoryLookup(**_to_labeled_memory(row["entity"]).__dict__, lookup_score=row["distance"])


class MilvusStorageBackend(StorageBackend):
    METADATA_TABLE_NAME = "memoryset_metadata"

    MEMORY_FIELDS = ["text", "image", "label", "label_name", "embedding", "metadata", "memory_id", "memory_version"]

    def __init__(
        self,
        table_name: str,
        database_uri: str,
        cache_ttl: int = CACHE_TTL,
        cache_size: int = CACHE_SIZE,
    ):
        super().__init__(table_name, database_uri, cache_ttl, cache_size)
        self.is_local_database = not database_uri.startswith("http")

    _connections: dict[str, MilvusClient] = {}

    @classmethod
    def _get_client(cls, database_uri: str, create: bool = False) -> MilvusClient | None:
        # We don't want to create a local database file if it doesn't exist yet unless we are connecting
        if not database_uri.startswith("http") and not os.path.exists(database_uri) and not create:
            return None
        if database_uri not in cls._connections:
            cls._connections[database_uri] = MilvusClient(database_uri)
        return cls._connections[database_uri]

    def _drop_database(self):
        raise NotImplementedError("Milvus Lite does not support dropping databases")

    def _initialize_metadata_collection(self):
        client = self._get_client(self.database_uri)
        if client is None:
            return None
        if not client.has_collection(self.METADATA_TABLE_NAME):
            logging.info(f"Creating metadata table for {self.database_uri}")
            schema = client.create_schema(auto_id=False, enable_dynamic_field=True)
            schema.add_field("memoryset_table_name", DataType.VARCHAR, is_primary=True, max_length=256)
            schema.add_field("embedding_dim", DataType.INT64, is_primary=False)
            schema.add_field("embedding_model_name", DataType.VARCHAR, is_primary=False, max_length=256)
            schema.add_field("embedding_model_max_seq_length_overwrite", DataType.INT64, is_primary=False)
            schema.add_field("_unused", DataType.FLOAT_VECTOR, is_primary=False, dim=2)
            client.create_collection(collection_name=self.METADATA_TABLE_NAME, schema=schema)
            # Milvus cloud requires an index, so we create one on the _unused field
            index_params = MilvusClient.prepare_index_params()
            index_params.add_index(field_name="_unused", index_name="_unused", index_type="FLAT", metric_type="L2")
            client.create_index(self.METADATA_TABLE_NAME, index_params=index_params)
        client.load_collection(self.METADATA_TABLE_NAME)

    def get_table_names(self) -> list[str]:
        client = self._get_client(self.database_uri)
        if client is None:
            return []
        self._initialize_metadata_collection()
        result = client.query(
            filter="memoryset_table_name != ''",
            collection_name=self.METADATA_TABLE_NAME,
            output_fields=["memoryset_table_name"],
        )
        return [row["memoryset_table_name"] for row in result]

    def drop(self):
        client = self._get_client(self.database_uri)
        if client is None:
            logging.warning(f"Database not found at {self.database_uri}")
            return
        self.__client = None
        if not client.has_collection(self.table_name):
            logging.warning(f"Memoryset {self.table_name} not found in {self.database_uri}")
        else:
            client.drop_collection(self.table_name)
        client.delete(
            collection_name=self.METADATA_TABLE_NAME,
            filter=f"memoryset_table_name == '{self.table_name}'",
        )

    def get_metadata(self) -> MemorysetMetadata | None:
        client = self._get_client(self.database_uri)
        if client is None:
            return None
        self._initialize_metadata_collection()
        metadata = client.query(
            collection_name=self.METADATA_TABLE_NAME,
            filter=f"memoryset_table_name == '{self.table_name}'",
            output_fields=["embedding_dim", "embedding_model_name", "embedding_model_max_seq_length_overwrite"],
        )
        if len(metadata) == 0:
            return None
        elif len(metadata) > 1:
            raise ValueError("Found multiple metadata entries for memoryset")

        return MemorysetMetadata(
            embedding_dim=metadata[0]["embedding_dim"],
            embedding_model_name=metadata[0]["embedding_model_name"],
            embedding_model_max_seq_length_overwrite=_empty_to_none(
                metadata[0]["embedding_model_max_seq_length_overwrite"], int
            ),
        )

    __client: MilvusClient | None = None

    @property
    def _client(self) -> MilvusClient:
        if self.__client is None:
            raise RuntimeError("You need to connect the storage backend before using it")
        return self.__client

    def _initialize_data_collection(self, embedding_dim: int) -> None:
        if not self._client.has_collection(self.table_name):
            logging.info(f"Creating collection {self.table_name}")
            schema = self._client.create_schema(auto_id=False, enable_dynamic_field=True)
            schema.add_field("memory_id", DataType.VARCHAR, is_primary=True, max_length=36)
            schema.add_field("memory_version", DataType.INT64, is_primary=False)
            schema.add_field("embedding", DataType.FLOAT_VECTOR, dim=embedding_dim, is_primary=False)
            schema.add_field("label", DataType.INT64, is_primary=False)
            schema.add_field("label_name", DataType.VARCHAR, is_primary=False, max_length=256)
            schema.add_field("metadata", DataType.VARCHAR, is_primary=False, max_length=2048)
            schema.add_field("text", DataType.VARCHAR, is_primary=False, max_length=2048)
            # Milvus does not support storing bytes and varchar requires a max length, so to support
            # images for now, we set `enable_dynamic_field=True` and don't specify the image field
            # type. Images are stored as base64 encoded strings in this field for now. In the
            # future, we will probably switch to storing images separately and just storing a URI to
            # the image in this field.
            # schema.add_field("image", DataType.VARCHAR, is_primary=False, max_length=2048)
            self._client.create_collection(collection_name=self.table_name, schema=schema)
            # Create index
            logging.info(f"Creating index for collection {self.table_name}")
            index_params = MilvusClient.prepare_index_params()
            index_params.add_index(
                field_name="embedding",
                index_name=self.table_name + "_index",
                index_type="FLAT",  # We don't support other index types that need more config yet
                metric_type=METRIC_TYPE,
            )
            self._client.create_index(collection_name=self.table_name, index_params=index_params)
        self._client.load_collection(self.table_name)

    def _upsert_metadata(self, metadata: MemorysetMetadata) -> None:
        # if self._client
        self._initialize_metadata_collection()
        self._client.insert(
            collection_name=self.METADATA_TABLE_NAME,
            data=[
                {
                    "memoryset_table_name": self.table_name,
                    "embedding_dim": metadata.embedding_dim,
                    "embedding_model_name": metadata.embedding_model_name,
                    "embedding_model_max_seq_length_overwrite": _none_to_empty(
                        metadata.embedding_model_max_seq_length_overwrite, int
                    ),
                    "_unused": [0.0, 0.0],
                }
            ],
        )

    def connect(self, metadata: MemorysetMetadata) -> MilvusStorageBackend:
        self.__client = self._get_client(self.database_uri, create=True)
        assert self.__client is not None
        self.connected = True
        self._upsert_metadata(metadata)
        self._initialize_data_collection(embedding_dim=metadata.embedding_dim)
        return self

    def insert(self, data: list[MemoryToInsert]) -> None:
        data_to_insert = [_prepare_for_insert(d) for d in data]
        self._client.insert(collection_name=self.table_name, data=data_to_insert)

    def lookup(self, query: np.ndarray, k: int, use_cache: bool) -> list[list[LabeledMemoryLookup]]:
        # keep track of original indices for queries and results for caching
        query_list: list[tuple[int, np.ndarray]] = [(idx, q) for idx, q in enumerate(query)]
        all_results: list[tuple[int, list[LabeledMemoryLookup]]] = []
        if use_cache:
            # resolve cache hits and remove corresponding queries
            for q in query_list:
                cache_key = self._get_cache_key(q[1], k)
                result = self._cache.get(cache_key, None)
                if result is not None:
                    all_results.append((q[0], result))
                    query_list.remove(q)
        # perform lookup for remaining queries
        query_results = self._client.search(
            collection_name=self.table_name,
            data=[q[1] for q in query_list],
            limit=k,
            output_fields=self.MEMORY_FIELDS,
            consistency_level="Strong",
            search_params={"metric_type": METRIC_TYPE},
        )
        # process new results adding them to the cache and all results list
        for q, r in zip(query_list, query_results):
            result = [_to_labeled_memory_lookup(row) for row in r]
            if use_cache:
                cache_key = self._get_cache_key(q[1], k)
                self._cache[cache_key] = result
            all_results.append((q[0], result))
        # return all results in order of original queries
        all_results.sort(key=lambda x: x[0])
        return [r[1] for r in all_results]

    def to_list(self, limit: int | None = None) -> list[LabeledMemory]:
        result = self._client.query(
            collection_name=self.table_name,
            filter="memory_id != ''",
            output_fields=self.MEMORY_FIELDS,
            limit=limit,
            consistency_level="Strong",
        )
        return [_to_labeled_memory(row) for row in result]

    def __iter__(self) -> Iterator[LabeledMemory]:
        return self.to_list().__iter__()

    def __len__(self) -> int:
        result = self._client.query(
            collection_name=self.table_name, output_fields=["count(*)"], consistency_level="Strong"
        )
        return result[0]["count(*)"]

    def __getitem__(self, memory_id: str) -> LabeledMemory | None:
        result = self._client.get(collection_name=self.table_name, ids=[memory_id], consistency_level="Strong")
        if len(result) == 0:
            return None
        assert len(result) == 1
        return _to_labeled_memory(result[0])

    def upsert(self, memory: MemoryToInsert) -> None:
        data_to_insert = [_prepare_for_insert(memory)]
        self._client.upsert(collection_name=self.table_name, data=data_to_insert)

    def delete(self, memory_id: str) -> None:
        self._client.delete(collection_name=self.table_name, ids=[memory_id])
