from __future__ import annotations

import io
import json
import logging
import os
from typing import Any, Iterator

import lancedb
import numpy as np
import pyarrow as pa
from PIL import Image

from .memory_types import LabeledMemory, LabeledMemoryLookup
from .storage import CACHE_SIZE, CACHE_TTL, MemorysetMetadata, StorageBackend
from .util import MemoryToInsert


def _encode_image(image: Image.Image) -> bytes:
    buffer = io.BytesIO()
    image.save(buffer, format=image.format)
    return buffer.getvalue()


def _decode_image(image_bytes: bytes) -> Image.Image:
    return Image.open(io.BytesIO(image_bytes))


def _prepare_for_insert(datum: MemoryToInsert) -> dict[str, Any]:
    assert datum["memory_id"] is not None
    assert datum["embedding"] is not None
    assert datum["text"] is not None or datum["image"] is not None
    return {
        "text": datum["text"],
        "image": _encode_image(datum["image"]) if datum["image"] is not None else None,
        "label": datum["label"],
        "label_name": datum["label_name"],
        "metadata": datum["metadata"],
        "memory_id": datum["memory_id"],
        "memory_version": datum["memory_version"],
        "embedding": datum["embedding"],
    }


def _to_labeled_memory(row: dict[str, Any]) -> LabeledMemory:
    return LabeledMemory(
        value=_decode_image(row["image"]) if row["image"] is not None else row["text"],
        label=row["label"],
        label_name=row.get("label_name", None),
        metadata=json.loads(row["metadata"]) if row["metadata"] is not None else {},
        embedding=np.array(row["embedding"], dtype=np.float32),
        memory_id=row.get("memory_id", None),
        memory_version=row.get("memory_version", 1),
    )


def _to_labeled_memory_lookup(row: dict[str, Any], query: np.ndarray) -> LabeledMemoryLookup:
    memory = _to_labeled_memory(row)
    return LabeledMemoryLookup(**memory.__dict__, lookup_score=float(np.dot(query, memory.embedding)))


class LanceDBStorageBackend(StorageBackend):
    METADATA_TABLE_NAME = "memoryset_metadata"

    def __init__(
        self, table_name: str, database_uri: str, cache_ttl: int = CACHE_TTL, cache_size: int = CACHE_SIZE
    ) -> None:
        super().__init__(table_name, database_uri, cache_ttl, cache_size)
        self.is_local_database = True

    _connections: dict[str, lancedb.DBConnection] = {}

    @classmethod
    def _get_db_connection(cls, database_uri: str) -> lancedb.DBConnection:
        if database_uri not in cls._connections:
            cls._connections[database_uri] = lancedb.connect(database_uri)
        return cls._connections[database_uri]

    def _drop_database(self):
        self._get_db_connection(self.database_uri).drop_database()

    __metadata_table: lancedb.table.Table | None = None

    @property
    def _metadata_table(self) -> lancedb.table.Table | None:
        if self.__metadata_table is not None:
            return self.__metadata_table
        # We don't want to create the database if it doesn't exist yet
        if not os.path.exists(self.database_uri):
            return None
        db = self._get_db_connection(self.database_uri)
        if self.METADATA_TABLE_NAME not in db.table_names():
            logging.info(f"Creating metadata table for {self.database_uri}")
            metadata_table = db.create_table(
                self.METADATA_TABLE_NAME,
                schema=pa.schema(
                    [
                        pa.field("memoryset_table_name", pa.string(), nullable=False),
                        pa.field("embedding_dim", pa.int64(), nullable=False),
                        pa.field("embedding_model_name", pa.string(), nullable=False),
                        pa.field("embedding_model_max_seq_length_overwrite", pa.int64()),
                    ]
                ),
            )
        else:
            metadata_table = db.open_table(self.METADATA_TABLE_NAME)
            # if the table already exists, migrate it to the latest schema
            if "embedding_model_max_seq_length_overwrite" not in metadata_table.schema.names:
                if "embedding_model_max_seq_length" in metadata_table.schema.names:
                    metadata_table.alter_columns(
                        {"path": "embedding_model_max_seq_length", "name": "embedding_model_max_seq_length_overwrite"}  # type: ignore -- lancedb types are wrong
                    )
                else:
                    metadata_table.add_columns({"embedding_model_max_seq_length_overwrite": "null"})

            if "embedding_model_version" in metadata_table.schema.names:
                metadata_table.drop_columns(["embedding_model_version"])
            if "embedding_model_query_prompt" in metadata_table.schema.names:
                metadata_table.drop_columns(["embedding_model_query_prompt"])
            if "embedding_model_document_prompt" in metadata_table.schema.names:
                metadata_table.drop_columns(["embedding_model_document_prompt"])
            if "embedding_model_embedding_dim" in metadata_table.schema.names:
                if "embedding_dim" not in metadata_table.schema.names:
                    metadata_table.alter_columns(
                        {"path": "embedding_model_embedding_dim", "name": "embedding_dim"}  # type: ignore -- lancedb types are wrong
                    )
                else:
                    metadata_table.drop_columns(["embedding_model_embedding_dim"])
        self.__metadata_table = metadata_table
        return metadata_table

    def get_table_names(self) -> list[str]:
        if self._metadata_table is None:
            return []
        result = self._metadata_table.search().select(["memoryset_table_name"]).to_list()
        return [row["memoryset_table_name"] for row in result]

    def drop(self):
        self.__metadata_table = None
        self.__data_table = None
        if self._metadata_table is None:
            logging.warning(f"Database not found at {self.database_uri}")
            return
        db = self._get_db_connection(self.database_uri)
        if self.table_name not in db.table_names():
            logging.warning(f"Memoryset {self.table_name} not found in {self.database_uri}")
        else:
            db.drop_table(self.table_name)
        self._metadata_table.delete(f"memoryset_table_name == '{self.table_name}'")

    def get_metadata(self) -> MemorysetMetadata | None:
        if self._metadata_table is None:
            return None
        metadata = self._metadata_table.search().where(f"memoryset_table_name == '{self.table_name}'").to_list()
        if len(metadata) == 0:
            return None
        if len(metadata) > 1:
            raise RuntimeError(f"Found {len(metadata)} metadata entries for memoryset {self.table_name}")
        return MemorysetMetadata(
            embedding_dim=metadata[0]["embedding_dim"],
            embedding_model_name=metadata[0]["embedding_model_name"],
            # TODO: fix once LanceDB supports null for ints https://github.com/lancedb/lancedb/issues/1325
            embedding_model_max_seq_length_overwrite=(
                metadata[0]["embedding_model_max_seq_length_overwrite"]
                if metadata[0]["embedding_model_max_seq_length_overwrite"] != -1
                else None
            ),
        )

    __data_table: lancedb.table.Table | None = None

    def _initialize_data_table(self, db: lancedb.DBConnection, embedding_model_dim: int) -> None:
        if self.table_name not in db.table_names():
            schema = pa.schema(
                [
                    pa.field("text", pa.string()),
                    pa.field("image", pa.binary()),
                    pa.field("label", pa.int64()),
                    pa.field("label_name", pa.string()),
                    pa.field("metadata", pa.string()),
                    pa.field("memory_id", pa.string()),
                    pa.field("memory_version", pa.int64()),
                    pa.field("embedding", pa.list_(pa.float32(), list_size=embedding_model_dim)),
                ]
            )
            self.__data_table = db.create_table(self.table_name, schema=schema, exist_ok=False)
        else:
            self.__data_table = db.open_table(self.table_name)

    def _upsert_metadata(self, metadata: MemorysetMetadata) -> None:
        assert self._metadata_table is not None, "make sure to call self._get_db_connection before this"
        self._metadata_table.merge_insert(
            "memoryset_table_name"
        ).when_matched_update_all().when_not_matched_insert_all().execute(
            [
                {
                    "memoryset_table_name": self.table_name,
                    "embedding_dim": metadata.embedding_dim,
                    "embedding_model_name": metadata.embedding_model_name,
                    # TODO: fix once LanceDB supports null for ints https://github.com/lancedb/lancedb/issues/1325
                    "embedding_model_max_seq_length_overwrite": (
                        metadata.embedding_model_max_seq_length_overwrite
                        if metadata.embedding_model_max_seq_length_overwrite is not None
                        else -1
                    ),
                }
            ]
        )

    def connect(self, metadata: MemorysetMetadata) -> LanceDBStorageBackend:
        db = self._get_db_connection(self.database_uri)
        self.connected = True
        self._upsert_metadata(metadata)
        self._initialize_data_table(db, metadata.embedding_dim)
        return self

    @property
    def _data_table(self) -> lancedb.table.Table:
        if self.__data_table is None:
            raise RuntimeError("You need to connect the storage backend before using it")
        return self.__data_table

    def insert(self, data: list[MemoryToInsert]) -> None:
        if len(data) == 0:
            return
        data_to_insert = [_prepare_for_insert(d) for d in data]
        self._data_table.add(data_to_insert)

    def lookup(self, query: np.ndarray, k: int, use_cache: bool) -> list[list[LabeledMemoryLookup]]:
        if len(query.shape) != 2:
            raise ValueError("Query must be a 2D numpy array")

        def single_lookup(q: np.ndarray) -> list[LabeledMemoryLookup]:
            cache_key = self._get_cache_key(q, k)
            result = self._cache.get(cache_key, None) if use_cache else None

            if result is None:
                result = self._data_table.search(q).with_row_id(True).limit(k).to_list()
                if use_cache:
                    self._cache[cache_key] = result

            return [_to_labeled_memory_lookup(row, q) for row in result]

        return [single_lookup(q) for q in query]

    def to_list(self, limit: int | None = None) -> list[LabeledMemory]:
        query_results = self._data_table.search().limit(limit).to_list()
        return [_to_labeled_memory(row) for row in query_results]

    def __iter__(self) -> Iterator[LabeledMemory]:
        return self.to_list().__iter__()

    def __len__(self) -> int:
        return self._data_table.count_rows()

    def __getitem__(self, memory_id: str) -> LabeledMemory | None:
        result = self._data_table.search().where(f"memory_id == '{memory_id}'").to_list()
        if len(result) == 0:
            return None
        assert len(result) == 1
        return _to_labeled_memory(result[0])

    def upsert(self, memory: MemoryToInsert) -> None:
        data_to_insert = [_prepare_for_insert(memory)]
        self._data_table.merge_insert("memory_id").when_matched_update_all().when_not_matched_insert_all().execute(
            data_to_insert
        )

    def delete(self, memory_id: str) -> None:
        self._data_table.delete(f"memory_id == '{memory_id}'")
