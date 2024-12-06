from __future__ import annotations

import hashlib
import logging
import re
from abc import ABC, abstractmethod
from typing import Any, Iterator

import numpy as np
from cachetools import TTLCache
from pydantic import BaseModel, Field

from .memory_types import LabeledMemory, LabeledMemoryLookup
from .util import MemoryToInsert

logging.basicConfig(level=logging.INFO)

CACHE_TTL = 2 * 60 * 60  # 2h
CACHE_SIZE = 25000


class MemorysetMetadata(BaseModel):
    embedding_dim: int = Field(..., gt=1)
    embedding_model_name: str
    embedding_model_max_seq_length_overwrite: int | None = Field(None, gt=0)

    class Config:
        frozen = True
        extra = "forbid"


class StorageBackend(ABC):
    table_name: str
    database_uri: str
    is_local_database: bool
    connected: bool = False

    @classmethod
    def _get_cache_key(cls, query: np.ndarray, k: int) -> str:
        return hashlib.md5(query.tobytes(order="C")).hexdigest() + f"_{k}"

    def __init__(
        self,
        table_name: str,
        database_uri: str,
        cache_ttl: int = CACHE_TTL,
        cache_size: int = CACHE_SIZE,
    ) -> None:
        """
        Create a storage backend for the memoryset without connecting to it.

        Warning:
            Before performing any operations on the storage backend other than `drop` and
            `get_metadata`, you must call `connect` on it.

        Args:
            table_name: Name of the table to use for the memoryset
            database_uri: URI of the database to connect to
        """
        if not re.match(r"^[a-zA-Z0-9_]+$", table_name):
            raise ValueError("Table name can only contain letters, numbers, underscores, and dashes")
        self.table_name = table_name
        self.database_uri = database_uri
        self._cache = TTLCache(maxsize=cache_size, ttl=cache_ttl)

    @abstractmethod
    def drop(self):
        """
        Drop the data table of the memoryset and delete its metadata.

        Notes:
            This does not drop the database file itself, only the data table for the memoryset and
            the row for the memoryset's metadata. If the memoryset has not been created yet, this
            operation is a no-op.
        """
        pass

    @abstractmethod
    def get_metadata(self) -> MemorysetMetadata | None:
        """
        Get the metadata for the memoryset if it exists.

        Notes:
            This will not create a local database file if it does not exist.

        Returns:
            Metadata for the memoryset or None if the memoryset has not been created yet.
        """
        pass

    @abstractmethod
    def connect(self, metadata: MemorysetMetadata) -> StorageBackend:
        """
        Connect to the database, initialize the database and memories table if necessary, and upsert
        the metadata for the memoryset.
        """
        pass

    def reset(self, metadata: MemorysetMetadata):
        """
        Drop the table of the memoryset and delete its metadata, then recreate it.
        """
        self.drop()
        self.connect(metadata)

    @abstractmethod
    def insert(self, data: list[MemoryToInsert]) -> None:
        pass

    @abstractmethod
    def lookup(self, query: np.ndarray, k: int, use_cache: bool) -> list[list[LabeledMemoryLookup]]:
        pass

    @abstractmethod
    def to_list(self, limit: int | None = None) -> list[LabeledMemory]:
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[LabeledMemory]:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__
            and self.database_uri == other.database_uri
            and self.table_name == other.table_name
        )

    @abstractmethod
    def __getitem__(self, memory_id: str) -> LabeledMemory | None:
        pass

    @abstractmethod
    def upsert(self, memory: MemoryToInsert) -> None:
        pass

    @abstractmethod
    def delete(self, memory_id: str) -> None:
        pass
