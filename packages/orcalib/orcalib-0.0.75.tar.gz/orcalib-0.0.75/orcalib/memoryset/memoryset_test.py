import hashlib
import uuid
from unittest.mock import patch

import lancedb
import numpy as np
import pandas as pd
import pytest
from numpy.linalg import norm
from PIL import Image, ImageChops

from .embedding_models import EmbeddingModel
from .memoryset import LabeledMemoryLookupColumnResult, LabeledMemoryset
from .util import get_embedding_hash


@pytest.fixture()
def memoryset():
    db_name = f"local{str(uuid.uuid4()).replace('-', '')[0:12]}"
    memoryset = LabeledMemoryset(f"file:./{db_name}.db", embedding_model=EmbeddingModel.CLIP_BASE)
    yield memoryset
    assert isinstance(memoryset.db, lancedb.DBConnection)
    memoryset.db.drop_database()


@pytest.fixture()
def another_memoryset(memoryset):
    return memoryset


def _images_are_approximately_equal(image1: Image.Image, image2: Image.Image, tolerance: float = 0.1) -> bool:
    # Ensure both images are in the same mode and size
    image1 = image1.convert("RGB")
    image2 = image2.convert("RGB")

    if image1.size != image2.size:
        image2 = image2.resize(image1.size)

    # Compute the difference between the two images
    diff = ImageChops.difference(image1, image2)

    # Convert the difference image to a numpy array
    diff_array = np.array(diff)

    # Calculate the total difference
    total_diff = np.sum(np.abs(diff_array))

    # Normalize by the number of pixels and color channels
    max_diff = np.prod(diff_array.shape) * 255  # 255 is the maximum possible difference per channel
    normalized_diff = total_diff / max_diff

    # Check if the normalized difference is within the tolerance
    return normalized_diff <= tolerance


# Test table and database name init


def test_local_passed_table_name():
    M = LabeledMemoryset("file:./delete_me_test_db#test_table")
    assert M.table_name == "test_table"
    assert isinstance(M.db, lancedb.DBConnection)

    # drop the data
    M.db.drop_database()


def test_local_default_table_name():
    M = LabeledMemoryset("file:./delete_me_test_db")
    assert M.table_name == "memories"
    assert isinstance(M.db, lancedb.DBConnection)

    # drop the data
    M.db.drop_database()


def test_get_embedding_hash():
    sample_array = EmbeddingModel.CLIP_BASE.embed("Test a real embedding")[0]
    expected_hash = hashlib.sha256(sample_array.tobytes()).hexdigest()

    result_hash = get_embedding_hash(sample_array)

    assert result_hash == expected_hash, f"Expected {expected_hash}, but got {result_hash}"


def test_get_embedding_hash_always_returns_same():
    sample_array = EmbeddingModel.CLIP_BASE.embed("Test a real embedding")[0]

    result_hash1 = get_embedding_hash(sample_array)
    result_hash2 = get_embedding_hash(sample_array)

    assert result_hash1 == result_hash2


def test_insert_and_lookup_multimodal(memoryset):
    test_image = Image.open("./orcalib/memoryset/test_image.png")
    test_text = "Scooby Doo where are you?"

    memoryset.insert(
        [
            {
                "value": test_image,
                "label": 7,
                "label_name": "Biters",
                "metadata": {"source": "screenshot"},
            },
            {
                "value": test_text,
                "label": 1,
                "label_name": "Scoooby!!",
                "metadata": {"source": "hanna babera"},
            },
        ]
    )
    # ensure the data is inserted
    assert len(memoryset) == 2

    # do a lookup (single and batch), ensure the correct top result is returned
    result1 = memoryset.lookup("Some Cartoon Dog Thing", k=1)
    assert len(result1) == 1
    assert isinstance(result1, list)
    assert result1[0].label == 1
    assert result1[0].value == "Scooby Doo where are you?"

    result1 = memoryset.lookup("Some Cartoon Dog Thing", k=1)
    assert isinstance(result1, list)
    assert result1[0].label == 1
    assert result1[0].value == "Scooby Doo where are you?"

    result2 = memoryset.lookup(test_image, k=1)
    assert isinstance(result2, list)
    assert result2[0].label == 7
    assert _images_are_approximately_equal(result2[0].value, test_image)  # type: ignore -- we know value is an image
    assert result2[0].metadata == {"source": "screenshot"}


def test_lookup_column_oriented(memoryset):
    test_image = Image.open("./orcalib/memoryset/test_image.png")
    test_text = "Scooby Doo where are you?"

    memoryset.insert(
        [
            {
                "image": test_image,
                "label": 7,
                "label_name": "Biters",
                "metadata": {"source": "screenshot"},
            },
            {
                "text": test_text,
                "label": 1,
                "label_name": "Scoooby!!",
                "metadata": {"source": "hanna babera"},
            },
        ]
    )
    # ensure the data is inserted
    assert len(memoryset) == 2

    # do a lookup (single and batch), ensure the correct top result is returned
    result = memoryset.lookup(["Some Cartoon Dog Thing"], k=2, return_type="columns")
    assert isinstance(result, dict)
    assert isinstance(result["memories_values"], list)
    assert len(result["memories_values"]) == 1
    assert isinstance(result["memories_values"][0], list)
    assert len(result["memories_values"][0]) == 2
    assert result["memories_values"][0][0] == "Scooby Doo where are you?"
    assert result["memories_labels"][0][0] == 1
    assert isinstance(result["input_embeddings"], list)
    assert len(result["input_embeddings"]) == 1
    assert isinstance(result["input_embeddings"][0], np.ndarray)
    assert result["input_embeddings"][0].dtype == np.float32
    assert isinstance(result["memories_embeddings"], list)
    assert len(result["memories_embeddings"]) == 1
    assert isinstance(result["memories_embeddings"][0], list)
    assert len(result["memories_embeddings"][0]) == 2
    assert isinstance(result["memories_embeddings"][0][0], np.ndarray)
    assert result["memories_embeddings"][0][0].dtype == np.float32
    assert isinstance(result["memories_embeddings"][0][1], np.ndarray)
    assert result["memories_embeddings"][0][1].dtype == np.float32


def test_clone(memoryset):
    # Given a memoryset with some data
    memoryset.insert(
        {
            "value": "Scooby Doo where are you?",
            "label": 1,
            "label_name": "Scoooby!!",
            "metadata": {"source": "hanna babera"},
        }
    )
    assert len(memoryset) == 1
    # When we clone it
    cloned_memoryset = memoryset.clone("destination1")
    # Then the cloned memoryset is created in a new table
    assert cloned_memoryset.table_name == "destination1"
    # Then the cloned memoryset has the same data
    assert len(cloned_memoryset) == 1
    assert cloned_memoryset[0].value == "Scooby Doo where are you?"
    assert cloned_memoryset[0].label == 1
    # And inserting into the original memoryset does not affect the cloned memoryset
    memoryset.insert([{"value": "Scooby Doo where are you?", "label": 1}])
    assert len(memoryset) == 2
    assert len(cloned_memoryset) == 1
    # And inserting into the cloned memoryset does not affect the original memoryset
    cloned_memoryset.insert([{"value": "Scooby Doo where are you?", "label": 1}])
    assert len(cloned_memoryset) == 2
    assert len(memoryset) == 2


def test_map(memoryset):
    # Given a memoryset with some data
    memoryset.insert([{"text": "Scooby Doo where are you?", "label": 1}])
    assert len(memoryset) == 1
    # When we use map to adjust the label
    mapped_memoryset = memoryset.map(lambda x: dict(label=x.label + 1), "destination2")
    # Then the mapped memoryset is in a new table
    assert mapped_memoryset.table_name == "destination2"
    # And the mapped memoryset has the adjusted label
    assert len(mapped_memoryset) == 1
    assert mapped_memoryset[0].label == 2
    assert mapped_memoryset[0].value == "Scooby Doo where are you?"
    # And the original memoryset is unchanged
    assert len(memoryset) == 1
    assert memoryset[0].label == 1
    assert memoryset[0].value == "Scooby Doo where are you?"


def test_filter(memoryset):
    # Given a memoryset with some data
    memoryset.insert([{"text": "Scooby Doo where are you?", "label": 1}, {"text": "Something else", "label": 2}])
    assert len(memoryset) == 2
    # When we filter the memoryset
    filtered_memoryset = memoryset.filter(lambda x: x.label == 1, "destination3")
    # Then the filtered memoryset is in a new table
    assert filtered_memoryset.table_name == "destination3"
    assert filtered_memoryset.mode == "local"
    # And the filtered memoryset has the correct data
    assert len(filtered_memoryset) == 1
    assert filtered_memoryset[0].value == "Scooby Doo where are you?"
    # And the original memoryset is unchanged
    assert len(memoryset) == 2


def _cos_sim(memory_embedding: np.ndarray, model_embedding: np.ndarray):
    return np.dot(memory_embedding, model_embedding) / (norm(memory_embedding) * norm(model_embedding))


def test_update_model_in_place(memoryset):
    # Insert some data
    memoryset.insert(
        [
            {
                "value": "Scooby Doo where are you?",
                "label": 1,
                "label_name": "Scoooby!!",
                "metadata": {"source": "hanna babera"},
            }
        ]
    )
    assert memoryset.embedding_model.name == EmbeddingModel.CLIP_BASE.name

    memory = memoryset.lookup(["Some Cartoon Dog Thing"], k=1)
    assert isinstance(memory[0], list)
    memory_embedding = memory[0][0].embedding
    model_embedding = EmbeddingModel.CLIP_BASE.embed("Scooby Doo where are you?")[0]
    assert memory_embedding is not None
    assert _cos_sim(memory_embedding, model_embedding) > 0.98

    # Update the embedding model
    new_model = EmbeddingModel.GTE_BASE
    memoryset.update_embedding_model(new_model)
    assert memoryset.embedding_model == new_model

    memory = memoryset.lookup(["Some Cartoon Dog Thing"], k=1)
    assert isinstance(memory[0], list)
    memory_embedding = memory[0][0].embedding
    model_embedding = EmbeddingModel.GTE_BASE.embed("Scooby Doo where are you?")[0]
    assert memory_embedding is not None
    assert _cos_sim(memory_embedding, model_embedding) > 0.98


def test_update_model_new_destination(memoryset, another_memoryset):
    # Insert some data
    memoryset.insert(
        [
            {
                "value": "Scooby Doo where are you?",
                "label": 1,
                "label_name": "Scoooby!!",
                "metadata": {"source": "hanna babera"},
            }
        ]
    )
    assert memoryset.embedding_model.name == EmbeddingModel.CLIP_BASE.name

    memory = memoryset.lookup(["Some Cartoon Dog Thing"], k=1)
    assert isinstance(memory[0], list)
    memory_embedding = memory[0][0].embedding
    model_embedding = EmbeddingModel.CLIP_BASE.embed("Scooby Doo where are you?")[0]
    assert memory_embedding is not None
    assert _cos_sim(memory_embedding, model_embedding) > 0.98

    # Update the embedding model
    new_model = EmbeddingModel.GTE_BASE
    memoryset.update_embedding_model(new_model, another_memoryset)
    assert another_memoryset.embedding_model == new_model

    memory = another_memoryset.lookup(["Some Cartoon Dog Thing"], k=1)
    assert isinstance(memory[0], list)
    memory_embedding = memory[0][0].embedding
    model_embedding = EmbeddingModel.GTE_BASE.embed("Scooby Doo where are you?")[0]
    assert memory_embedding is not None
    assert _cos_sim(memory_embedding, model_embedding) > 0.98


def test_lookup_caching(memoryset):
    test_text = "Scooby Doo where are you?"
    memoryset.insert(
        [
            {
                "value": test_text,
                "memory_version": 0,
                "label": 1,
                "label_name": "Scoooby!!",
                "metadata": {"source": "hanna babera"},
            },
        ]
    )

    memory_embedding = memoryset.embedding_model.embed("Some Cartoon Dog Thing")[0]
    # cache is empty initially
    assert memoryset.cache.currsize == 0

    assert isinstance(memoryset.db, lancedb.DBConnection)
    with patch.object(memoryset.db, "open_table", wraps=memoryset.db.open_table) as wrapped_open_table:
        result = memoryset.lookup("Some Cartoon Dog Thing", k=1)
        wrapped_open_table.assert_called_once()
        assert memoryset.cache.currsize == 1
        assert memoryset.cache[(get_embedding_hash(memory_embedding), 1)] is not None
        assert len(memoryset.cache[(get_embedding_hash(memory_embedding), 1)]) == len(result)

        memoryset.lookup("Some Cartoon Dog Thing", k=1)
        wrapped_open_table.assert_called_once()  # did not get called again


def test_metadata_mismatch(memoryset):
    # try to re-initialize with a different model
    with pytest.raises(ValueError):
        LabeledMemoryset(memoryset.url, embedding_model=EmbeddingModel.GTE_BASE)


def test_existing_metadata(memoryset):
    # assert no error raised and no new metadata is added
    memoryset_reconnect = LabeledMemoryset(memoryset.url)
    assert len(memoryset_reconnect) == len(memoryset)
    assert memoryset_reconnect.embedding_model.name == memoryset.embedding_model.name


def test_to_list(memoryset):
    # Given a memoryset with some data
    memoryset.insert([{"text": "Scooby Doo where are you?", "label": 1}, {"text": "Something else", "label": 2}])
    # When to_list is called
    memory_list = memoryset.to_list()
    # Then the list contains the correct data
    assert len(memory_list) == 2
    assert memory_list[0].value == "Scooby Doo where are you?"
    assert memory_list[0].label == 1
    assert memory_list[1].value == "Something else"
    assert memory_list[1].label == 2


def test_to_pandas(memoryset):
    # Given a memoryset with some data
    memoryset.insert([{"text": "Scooby Doo where are you?", "label": 1}, {"text": "Something else", "label": 2}])
    # When to_pandas is called
    memories = memoryset.to_pandas(limit=1)
    # Then the returned list is a pandas Dataframe with the correct limit
    assert isinstance(memories, pd.DataFrame)
    assert memories.shape[0] == 1
    assert memories.iloc[0].value == "Scooby Doo where are you?"
    assert memories.iloc[0].label == 1


def test_analyze(memoryset):
    # Given a memoryset with some data
    memoryset.insert([{"text": "Scooby Doo where are you?", "label": 1}, {"text": "Something else", "label": 2}])
    # When analyze is called
    analysis = memoryset.analyze()
    # Then an analysis score can be computed
    assert isinstance(analysis.data_score(), float)
