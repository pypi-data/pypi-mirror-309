import base64
import io
import tempfile
import uuid
from time import perf_counter
from typing import Generator

import numpy as np
import pytest
from PIL import Image, ImageChops

from .embedding_models import EmbeddingModel
from .memory_types import LabeledMemory
from .storage import MemorysetMetadata, StorageBackend
from .storage_lancedb import LanceDBStorageBackend
from .storage_milvus import MilvusStorageBackend
from .util import MemoryToInsert

MEMORYSET_METADATA = MemorysetMetadata(
    embedding_dim=EmbeddingModel.CLIP_BASE.embedding_dim,
    embedding_model_name=EmbeddingModel.CLIP_BASE.name,
    embedding_model_max_seq_length_overwrite=None,
)


TEXT_DATA: list[MemoryToInsert] = [
    MemoryToInsert(
        text=text,
        label=label,
        label_name="positive" if label == 0 else "negative",
        metadata="{}",
        embedding=EmbeddingModel.CLIP_BASE.embed(text).tolist()[0],
        image=None,
        memory_id=str(uuid.uuid4()),
        memory_version=1,
    )
    for text, label in [
        ("I'm over the moon with how things turned out!", 0),
        ("This is the happiest I've felt in a long time.", 0),
        ("My heart feels so full and content.", 0),
        ("Everything feels perfect right now, I couldn't ask for more.", 0),
        ("I am so fed up with dealing with this over and over.", 1),
        ("Why does it always feel like I'm hitting a brick wall?", 1),
        ("I'm getting really tired of this never-ending cycle.", 1),
        ("It's so frustrating when things just never go my way.", 1),
    ]
]


@pytest.fixture()
def temp_folder() -> Generator[str, None, None]:
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture(params=["lancedb", "milvus"])
def unconnected_storage_backend(request, temp_folder) -> StorageBackend:
    match request.param:
        case "lancedb":
            return LanceDBStorageBackend(
                database_uri=f"{temp_folder}/lance.db",
                table_name="memories",
            )
        case "milvus":
            return MilvusStorageBackend(
                database_uri=f"{temp_folder}/milvus.db",
                table_name="memories",
            )
        case _:
            raise ValueError(f"Invalid storage backend: {request.param}")


@pytest.fixture()
def storage_backend(unconnected_storage_backend) -> StorageBackend:
    return unconnected_storage_backend.connect(MEMORYSET_METADATA)


def test_meta_tables(unconnected_storage_backend):
    # When getting metadata for a new storage backend that has never been connected
    metadata = unconnected_storage_backend.get_metadata()
    # Then the metadata is None
    assert metadata is None
    # When the storage backend is connected
    connected_storage_backend = unconnected_storage_backend.connect(MEMORYSET_METADATA)
    # Then the metadata is not None anymore
    metadata = connected_storage_backend.get_metadata()
    assert metadata is not None
    for m in MEMORYSET_METADATA.__dict__.keys():
        assert getattr(metadata, m) == getattr(MEMORYSET_METADATA, m)
    # When reconnecting to the storage backend without connecting
    StorageBackendImplementation = connected_storage_backend.__class__
    database_uri = connected_storage_backend.database_uri
    table_name = connected_storage_backend.table_name
    del unconnected_storage_backend
    del connected_storage_backend
    reconnected_storage_backend = StorageBackendImplementation(database_uri=database_uri, table_name=table_name)
    # Then the metadata is not None
    metadata = reconnected_storage_backend.get_metadata()
    assert metadata is not None


def test_reload_storage_backend(storage_backend):
    # Given a storage backend with some data
    storage_backend.insert(TEXT_DATA)
    assert len(storage_backend) == len(TEXT_DATA)
    StorageBackendImplementation = storage_backend.__class__
    database_uri = storage_backend.database_uri
    table_name = storage_backend.table_name
    del storage_backend
    # When we reconnect to the storage backend
    reconnected_storage_backend = StorageBackendImplementation(
        database_uri=database_uri, table_name=table_name
    ).connect(MEMORYSET_METADATA)
    # Then we can access its memories
    assert len(reconnected_storage_backend) == len(TEXT_DATA)


def test_drop_table(storage_backend):
    # Given a storage backend with some data
    storage_backend.insert(TEXT_DATA)
    assert len(storage_backend) == len(TEXT_DATA)
    # When we drop the storage backend
    storage_backend.drop()
    # Then we can no longer access its memories
    with pytest.raises(RuntimeError):
        len(storage_backend)
    # When we re instantiate the storage backend
    StorageBackendImplementation = storage_backend.__class__
    database_uri = storage_backend.database_uri
    table_name = storage_backend.table_name
    del storage_backend
    reconnected_storage_backend = StorageBackendImplementation(database_uri=database_uri, table_name=table_name)
    # Then the storage backend does not exist anymore
    metadata = reconnected_storage_backend.get_metadata()
    assert metadata is None
    # And it has no memories after reconnecting
    assert len(reconnected_storage_backend.connect(MEMORYSET_METADATA)) == 0


def test_reset_storage_backend(storage_backend):
    # Given a storage backend with some data
    storage_backend.insert(TEXT_DATA)
    assert len(storage_backend) == len(TEXT_DATA)
    # When we reset the storage backend
    storage_backend.reset(MEMORYSET_METADATA)
    # Then the storage backend is empty
    assert len(storage_backend) == 0


def test_to_list(storage_backend):
    # Given a storage backend with some data
    storage_backend.insert(TEXT_DATA)
    assert len(storage_backend) == len(TEXT_DATA)
    # When we get the list of memories
    values = storage_backend.to_list()
    # Then we get a list of all the memories
    assert len(values) == len(TEXT_DATA)
    # And the memories have the correct value, embedding, and embedding shape and type
    for value in values:
        assert isinstance(value, LabeledMemory)
        assert isinstance(value.memory_id, str)
        assert isinstance(value.memory_version, int)
        assert isinstance(value.value, str)
        assert isinstance(value.embedding, np.ndarray)
        assert value.embedding.shape == (MEMORYSET_METADATA.embedding_dim,)
        assert value.embedding.dtype == np.float32


def test_get_by_id(storage_backend):
    # Given a storage backend with some data
    storage_backend.insert(TEXT_DATA)
    # When we get a memory by its memory_id
    memory = storage_backend[TEXT_DATA[0]["memory_id"]]
    # Then we get the correct memory
    assert isinstance(memory, LabeledMemory)
    assert memory.value == TEXT_DATA[0]["text"]


def test_upsert(storage_backend):
    # When we insert a memory
    storage_backend.upsert(TEXT_DATA[0])
    # Then the memory is inserted
    assert len(storage_backend) == 1
    # And the memory has the correct value
    assert storage_backend[TEXT_DATA[0]["memory_id"]].value == TEXT_DATA[0]["text"]
    # When we update the memory
    storage_backend.upsert(TEXT_DATA[0] | {"text": "updated_value", "label": 3, "memory_version": 2})
    # Then no new memory is inserted
    assert len(storage_backend) == 1
    # And the memory has the updated value
    assert storage_backend[TEXT_DATA[0]["memory_id"]].value == "updated_value"
    assert storage_backend[TEXT_DATA[0]["memory_id"]].label == 3
    assert storage_backend[TEXT_DATA[0]["memory_id"]].memory_version == 2


def test_delete(storage_backend):
    # Given a storage backend with some data
    storage_backend.insert(TEXT_DATA)
    assert len(storage_backend) == len(TEXT_DATA)
    # When we delete a memory
    storage_backend.delete(TEXT_DATA[0]["memory_id"])
    # Then the memory is deleted
    assert storage_backend[TEXT_DATA[0]["memory_id"]] is None
    assert len(storage_backend) == len(TEXT_DATA) - 1


def test_insert_and_lookup_text(storage_backend):
    # Given a storage backend with some text memories
    storage_backend.insert(TEXT_DATA)
    # And a query vector
    query = np.array(TEXT_DATA[0]["embedding"]).reshape(1, -1)
    # When we look up the query vector
    memory_lookups = storage_backend.lookup(query, 4, use_cache=False)
    # Then we get a list of lists of memories
    assert isinstance(memory_lookups, list)
    assert len(memory_lookups) == 1
    assert isinstance(memory_lookups[0], list)
    assert len(memory_lookups[0]) == 4
    # And the first memory in the list is the one with the matching text
    assert isinstance(memory_lookups[0][0].value, str)
    assert memory_lookups[0][0].value == TEXT_DATA[0]["text"]
    # And the lookup score is high
    assert memory_lookups[0][0].lookup_score >= 0.99
    # And the embedding is a numpy array of the correct shape and type
    assert isinstance(memory_lookups[0][0].embedding, np.ndarray)
    assert memory_lookups[0][0].embedding.shape == (MEMORYSET_METADATA.embedding_dim,)
    assert memory_lookups[0][0].embedding.dtype == np.float32


def test_lookup_caching(storage_backend):
    # Given a storage backend with some data
    storage_backend.insert(TEXT_DATA)
    # When we lookup a few queries
    queries = np.array([m["embedding"] for m in TEXT_DATA])
    assert queries.shape == (8, MEMORYSET_METADATA.embedding_dim)
    memory_lookups = storage_backend.lookup(queries, 4, use_cache=True)
    assert len(memory_lookups) == len(queries)
    # Then the results are stored in the cache
    assert len(storage_backend._cache) == len(queries)
    # When we lookup a subset of those queries again
    start = perf_counter()
    cached_memory_lookups = storage_backend.lookup(queries[:6], 4, use_cache=True)
    cached_duration = perf_counter() - start
    start = perf_counter()
    uncached_memory_lookups = storage_backend.lookup(queries[:6], 4, use_cache=False)
    uncached_duration = perf_counter() - start
    # Then the lookup is faster
    assert cached_duration < uncached_duration
    # And the cached results are the same as the uncached results
    assert all(
        all(
            cached_memory_lookups[i][j].value == uncached_memory_lookups[i][j].value
            for j in range(len(cached_memory_lookups[i]))
        )
        for i in range(len(cached_memory_lookups))
    )


def test_insert_and_lookup_image(storage_backend):
    # Given a storage backend with a few PNG images
    images = [
        Image.open(io.BytesIO(base64.b64decode(base64_string)))
        for base64_string in [
            "iVBORw0KGgoAAAANSUhEUgAAAAkAAAAJCAIAAABv85FHAAAAN0lEQVR4nGP8//8/Aw7AgmAyMkIZMNVM6BJIbCZ0CSRpJnRRJEBQDtOp//8j6UOWhrFZMIXgAABurQ8RDsBcHQAAAABJRU5ErkJggg==",  # red circle
            "iVBORw0KGgoAAAANSUhEUgAAAAkAAAAJCAIAAABv85FHAAAALUlEQVR4nGP8//8/Aw7AhMxhbGTEKYdTH0QTslYi9CErh7MJ6UNzHsJuPP4DANsWCaCKZRMuAAAAAElFTkSuQmCC",  # green triangle
            "iVBORw0KGgoAAAANSUhEUgAAAAkAAAAJCAIAAABv85FHAAAAKElEQVR4nM2PsQ0AMAyDcJX/XyYP1HtYEQNRKQyQfITyWgSn3ADtcAGzGQcROl7AigAAAABJRU5ErkJggg==",  # blue square
        ]
    ]
    storage_backend.insert(
        [
            MemoryToInsert(
                text=None,
                label=i,
                label_name=None,
                metadata="{}",
                embedding=EmbeddingModel.CLIP_BASE.embed(image).tolist()[0],
                image=image,
                memory_version=1,
                memory_id=str(uuid.uuid4()),
            )
            for i, image in enumerate(images)
        ]
    )
    # When we look up the first image by its embedding
    memory_lookups = storage_backend.lookup(EmbeddingModel.CLIP_BASE.embed(images[0]), 2, use_cache=False)
    # Then we get a list of lists of memories
    assert isinstance(memory_lookups, list)
    assert len(memory_lookups) == 1
    assert isinstance(memory_lookups[0], list)
    assert len(memory_lookups[0]) == 2
    # And the first memory in the list is the one with the matching image
    assert memory_lookups[0][0].label == 0
    # And the lookup score is high
    assert memory_lookups[0][0].lookup_score >= 0.99
    # And the image value is returned properly
    assert isinstance(memory_lookups[0][0].value, Image.Image)
    assert ImageChops.difference(memory_lookups[0][0].value, images[0]).getbbox() is None


def test_storage_backend_equality():
    # Given two storage backends with the same database URI and table name
    storage_backend1 = LanceDBStorageBackend(database_uri="test", table_name="test")
    storage_backend2 = LanceDBStorageBackend(database_uri="test", table_name="test")
    # Then the storage backends are equal
    assert storage_backend1 == storage_backend2
