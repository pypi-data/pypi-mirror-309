import base64
import tempfile
from io import BytesIO

import numpy as np
import pytest
from datasets import Dataset
from PIL import Image

from orcalib.memoryset.embedding_models import (
    EmbeddingModel,
    EmbeddingTrainingArgumentsForClassification,
    EmbeddingTrainingArgumentsWithTriplets,
)

TEST_DATASET = Dataset.from_dict(
    {
        "text": [
            "I'm over the moon with how things turned out!",
            "This is the happiest I've felt in a long time.",
            "My heart feels so full and content.",
            "Everything feels perfect right now, I couldn't ask for more.",
            "I'm just so grateful for all the little things today.",
            "I feel like I'm floating on air after that news!",
            "The sun is shining, and life feels amazing.",
            "I can't stop smiling; everything is just falling into place.",
            "I feel so blessed to have these wonderful people in my life.",
            "This moment is everything I dreamed it would be.",
            "It's like all my dreams are finally coming true.",
            "I couldn't be happier with how things are going.",
            "There's a warmth in my heart that I can't describe.",
            "I feel truly alive and connected to everything around me.",
            "This accomplishment means the world to me.",
            "It's amazing to feel so supported and loved.",
            "I am so fed up with dealing with this over and over.",
            "Why does it always feel like I'm hitting a brick wall?",
            "I'm getting really tired of this never-ending cycle.",
            "It's so frustrating when things just never go my way.",
            "I can't believe I'm still dealing with this nonsense.",
            "Every small setback is just adding to my frustration.",
            "I'm done putting up with these constant roadblocks.",
            "It feels like everything is working against me lately.",
            "I feel trapped by all these obstacles I can't control.",
            "Nothing I do seems to make a difference at this point.",
            "I'm at my wits' end with all of this chaos.",
            "I can't stand how unfair this situation is becoming.",
            "It feels like I'm pouring energy into a black hole.",
            "I'm exhausted from dealing with this repeated hassle.",
            "Why does it feel like every step forward is two steps back?",
            "I'm so frustrated that I can't seem to make progress.",
        ],
        "label": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    }
)


@pytest.fixture()
def temp_folder():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


def test_default_embedding_models():
    # When a default embedding model is instantiated
    embedding_model = EmbeddingModel.GTE_BASE
    # Then it has the correct name
    assert embedding_model.name == "OrcaDB/gte-base-en-v1.5"


def test_embedder_caching():
    # When two embedding models with the same name and max sequence length are instantiated
    embedding_model_1 = EmbeddingModel("distilbert-base-uncased", max_seq_length=15)
    embedding_model_2 = EmbeddingModel("distilbert-base-uncased", max_seq_length=15)
    # Then they share the same embedder
    assert embedding_model_1._embedder is embedding_model_2._embedder


def test_embed_text():
    # When generating embeddings for a single string
    embeddings = EmbeddingModel.GTE_BASE.embed("Hello, world!")
    # Then a 2-dimensional array of floats with a single row is returned
    assert embeddings.shape == (1, 768)
    assert embeddings.dtype == np.float32
    # And the embedding is normalized
    assert np.isclose(np.linalg.norm(embeddings), 1.0)


def test_embed_image():
    # Given an image
    base64_image = "iVBORw0KGgoAAAANSUhEUgAAAAkAAAAJCAIAAABv85FHAAAAN0lEQVR4nGP8//8/Aw7AgmAyMkIZMNVM6BJIbCZ0CSRpJnRRJEBQDtOp//8j6UOWhrFZMIXgAABurQ8RDsBcHQAAAABJRU5ErkJggg=="
    image = Image.open(BytesIO(base64.b64decode(base64_image)))
    # When embedding the image
    embeddings = EmbeddingModel.CLIP_BASE.embed(image)
    # Then a 2-dimensional array of floats with a single row is returned
    assert embeddings.shape == (1, 768)
    assert embeddings.dtype == np.float32
    # And the embedding is normalized
    assert np.isclose(np.linalg.norm(embeddings), 1.0)


def test_embed_batch():
    # When generating embeddings for a batch of strings
    embeddings = EmbeddingModel.GTE_BASE.embed(["Hello, world!", "Goodbye, world!"])
    # Then a 2-dimensional array of floats is returned
    assert embeddings.shape == (2, 768)
    assert embeddings.dtype == np.float32


def test_classification_finetuning(temp_folder: str):
    # When finetuning a classification model
    finetuned_model = EmbeddingModel.GTE_BASE.finetune(
        f"{temp_folder}/gte_base_classification_finetuned",
        train_dataset=TEST_DATASET,
        method="classification",
        training_args=EmbeddingTrainingArgumentsForClassification(max_steps=2),
    )
    # Then a finetuned model is returned
    assert finetuned_model is not None
    # And the model can embed strings
    embeddings = finetuned_model.embed(["Hello, world!"])
    assert embeddings.shape == (1, 768)
    assert embeddings.dtype == np.float32


def test_triplets_finetuning(temp_folder: str):
    # Given an embedding model with a max sequence length override
    model = EmbeddingModel("distilbert-base-uncased", max_seq_length=15)
    assert model.max_seq_length == 15
    # And a train and eval dataset
    dataset = TEST_DATASET.train_test_split(test_size=8, seed=42)
    # When finetuning the model with triplets
    finetuned_model = model.finetune(
        f"{temp_folder}/distilbert_triplets_finetuned",
        train_dataset=dataset["train"],
        eval_dataset=dataset["test"],
        method="triplets",
        training_args=EmbeddingTrainingArgumentsWithTriplets(
            per_device_train_batch_size=8,
            per_device_eval_batch_size=8,
        ),
    )
    # Then a finetuned model is returned
    assert finetuned_model is not None
    # And the model has the same max sequence length override as the original model
    assert finetuned_model.max_seq_length == 15
    # And the model can embed strings
    embeddings = finetuned_model.embed(["Hello, world!"])
    assert embeddings.shape == (1, 768)
    assert embeddings.dtype == np.float32
