import logging
import os
import tempfile

import numpy as np
import pytest
import torch
from datasets import ClassLabel, Dataset

from ..memoryset import EmbeddingModel, LabeledMemoryLookup, LabeledMemorysetV2
from .model_v2 import (
    EvalResult,
    MemoryMixtureOfExpertsClassificationHead,
    NearestMemoriesClassificationHead,
    PredictionResult,
    RACModelV2,
    RACTrainingArguments,
)

TEST_DATASET = (
    Dataset.from_dict(
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
    .cast_column("label", ClassLabel(names=["positive", "negative"]))
    .train_test_split(test_size=8, seed=42, stratify_by_column="label")
)


@pytest.fixture()
def temp_folder():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture()
def memoryset(temp_folder):
    memoryset = LabeledMemorysetV2(
        f"{temp_folder}/milvus.db#memoryset",
        embedding_model=EmbeddingModel.GTE_BASE,
    )
    memoryset.insert(TEST_DATASET["train"])
    return memoryset


def test_initialize_model(memoryset):
    # When a model is initialized with a memoryset
    model = RACModelV2(
        memoryset=memoryset,
        head_type="mmoe",
    )
    # Then the model is initialized without errors
    assert model is not None
    # And the memoryset is attached to the model
    assert model.memoryset is memoryset
    # And it has the correct head
    assert isinstance(model.head, MemoryMixtureOfExpertsClassificationHead)
    # And a reasonable memory lookup count is inferred
    assert model.memory_lookup_count == 15
    # And the number of classes is inferred from the memoryset
    assert model.num_classes == 2
    # And the forward method returns a valid output
    batch_size = 2
    memories_labels = torch.tensor([[1] * 15, [0] * 15])
    assert memories_labels.shape == (batch_size, model.memory_lookup_count)
    input_embeddings = torch.rand(batch_size, model.memoryset.embedding_model.embedding_dim)
    memories_embeddings = torch.rand(
        batch_size, model.memory_lookup_count, model.memoryset.embedding_model.embedding_dim
    )
    expected_labels = torch.tensor([1, 0])
    assert expected_labels.shape == (batch_size,)
    output = model(
        input_embeddings=input_embeddings,
        memories_labels=memories_labels,
        memories_embeddings=memories_embeddings,
        memories_weights=None,
        labels=expected_labels,
    )
    assert output is not None
    assert output.loss is not None
    assert output.logits is not None
    assert output.logits.shape == (batch_size, model.num_classes)
    assert (output.logits.argmax(dim=-1) == expected_labels).all()


def test_save_and_load_model(temp_folder, memoryset):
    # Given a RAC model
    model = RACModelV2(memoryset=memoryset, head_type="knn", weigh_memories=True)
    # When the model is saved
    location = f"{temp_folder}/model"
    model.save_pretrained(location)
    # And loaded back up
    del model
    loaded_model = RACModelV2.from_pretrained(location)
    # Then the model is loaded without errors
    assert loaded_model is not None
    # And the memoryset is correctly attached
    assert loaded_model.memoryset.uri == memoryset.uri
    assert len(loaded_model.memoryset) == len(memoryset)
    # And the config is loaded correctly
    assert isinstance(loaded_model.head, NearestMemoriesClassificationHead)
    assert loaded_model.config.weigh_memories is True


def test_evaluate(memoryset):
    # Given a RAC model
    model = RACModelV2(memoryset=memoryset, head_type="knn", min_memory_weight=0.5)
    # When the model is evaluated
    result = model.evaluate(TEST_DATASET["test"])
    # Then a result is returned
    assert isinstance(result, EvalResult)
    # And the result contains all the metrics
    assert result.accuracy > 0.7
    assert result.f1 > 0.7
    assert result.roc_auc is not None
    assert result.roc_auc > 0.7
    assert isinstance(result.loss, float)


def test_finetune(temp_folder, memoryset):
    # Given a RAC model
    model = RACModelV2(memoryset=memoryset, head_type="ff")
    # When the model is finetuned
    location = f"{temp_folder}/model"
    pre_finetune_metrics = model.evaluate(TEST_DATASET["train"])
    print(f"pre finetune accuracy: {pre_finetune_metrics.accuracy:.1%}")
    model.finetune(
        location,
        train_data=TEST_DATASET["train"],
        eval_data=TEST_DATASET["test"],
        training_args=RACTrainingArguments(
            max_steps=4, warmup_steps=0, eval_strategy="steps", eval_steps=4, logging_steps=1
        ),
    )
    # Then the checkpoints are saved to the location
    assert os.path.exists(location)
    # And the model is fit to the training data
    post_finetune_metrics = model.evaluate(TEST_DATASET["train"])
    print(f"post finetune accuracy: {post_finetune_metrics.accuracy:.1%}")
    assert post_finetune_metrics.loss < pre_finetune_metrics.loss
    assert post_finetune_metrics.accuracy > pre_finetune_metrics.accuracy


def test_predict(memoryset):
    # Given a RAC model
    model = RACModelV2(memoryset=memoryset)
    # When predict is called with a single text
    prediction = model.predict(TEST_DATASET["test"]["text"][0])
    # Then a single prediction is returned
    assert prediction is not None
    assert isinstance(prediction, PredictionResult)
    # And the prediction contains a label
    assert prediction.label in [0, 1]
    # And the prediction contains a confidence
    assert 0 <= prediction.confidence <= 1
    # And the logits are a numpy array
    assert isinstance(prediction.logits, np.ndarray)
    assert prediction.logits.shape == (model.num_classes,)
    assert prediction.logits.dtype == np.float32
    # And the input embedding
    assert isinstance(prediction.input_embedding, np.ndarray)
    assert prediction.input_embedding.shape == (model.memoryset.embedding_model.embedding_dim,)
    assert prediction.input_embedding.dtype == np.float32
    # And the memory lookups
    assert isinstance(prediction.memories, list)
    assert len(prediction.memories) == model.memory_lookup_count
    assert isinstance(prediction.memories[0], LabeledMemoryLookup)
    # And the memory lookups contain the attention weights
    assert prediction.memories[0].attention_weight is not None
    assert isinstance(prediction.memories[0].attention_weight, float)


def test_predict_batch(memoryset):
    # Given a RAC model
    model = RACModelV2(memoryset=memoryset)
    # When predict is called with a batch of texts
    predictions = model.predict(TEST_DATASET["test"]["text"][:2])
    # Then a list of predictions is returned
    assert isinstance(predictions, list)
    assert len(predictions) == 2
    # And each prediction is a PredictionResult
    assert all(isinstance(prediction, PredictionResult) for prediction in predictions)
    # And the prediction results contain memories
    assert all(isinstance(prediction.memories[0], LabeledMemoryLookup) for prediction in predictions)
