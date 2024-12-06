from unittest.mock import MagicMock

import numpy as np

from orcalib.memoryset.embedding_models import EmbeddingModel
from orcalib.rac.rac import RACModel
from orcalib.rac.return_types import (
    AnalyzePrediction,
    AnalyzeResult,
    LabeledMemoryLookup,
    PredictionResult,
)

test_rac = RACModel(num_classes=3, embedding_model=EmbeddingModel.CLIP_BASE)

prediction_result = PredictionResult(
    label=1,
    label_name="bear",
    confidence=0.9,
    memories=[
        LabeledMemoryLookup(
            memory_version=0,
            value="pear",
            label=0,
            label_name="pear",
            lookup_score=0.5,
            memory_id=5,
            attention_weight=0.9,
            embedding=np.random.rand(768),
            metadata={},
        ),
        LabeledMemoryLookup(
            value="apple",
            label=0,
            label_name="apple",
            lookup_score=0.5,
            memory_id=4,
            attention_weight=0.9,
            memory_version=0,
            embedding=np.random.rand(768),
            metadata={},
        ),
        LabeledMemoryLookup(
            value="peach",
            label=2,
            label_name="peach",
            lookup_score=0.5,
            memory_id=3,
            attention_weight=0.9,
            memory_version=0,
            embedding=np.random.rand(768),
            metadata={},
        ),
        LabeledMemoryLookup(
            value="apple",
            label=0,
            label_name="apple",
            lookup_score=0.5,
            memory_id=2,
            attention_weight=0.9,
            memory_version=0,
            embedding=np.random.rand(768),
            metadata={},
        ),
        LabeledMemoryLookup(
            value="banana",
            label=1,
            lookup_score=0.5,
            memory_id=1,
            memory_version=0,
            attention_weight=0.9,
            embedding=np.random.rand(768),
            metadata={},
        ),
    ],
    logits=np.array([0.8999999761581421, 0.0, 0.10000000149011612]),
    input_embedding=np.random.rand(768),
)


test_rac.predict = MagicMock(return_value=prediction_result)

expected_stats = AnalyzeResult(
    num_memories_accessed=5,
    label_counts={0: 3, 2: 1, 1: 1},
    label_stats=[
        {"label": 0, "label_name": "apple", "count": 3, "variance": 0.0, "mean": 0.5},
        {"label": 2, "label_name": "peach", "count": 1, "variance": 0.0, "mean": 0.5},
        {"label": 1, "label_name": None, "count": 1, "variance": 0.0, "mean": 0.5},
    ],
    memory_stats=[
        {
            "label": 0,
            "label_name": "pear",
            "lookup_score": 0.5,
            "attention_weight": 0.9,
            "memory_value": "pear",
            "memory_id": 5,
        },
        {
            "label": 0,
            "label_name": "apple",
            "lookup_score": 0.5,
            "attention_weight": 0.9,
            "memory_value": "apple",
            "memory_id": 4,
        },
        {
            "label": 2,
            "label_name": "peach",
            "lookup_score": 0.5,
            "attention_weight": 0.9,
            "memory_value": "peach",
            "memory_id": 3,
        },
        {
            "label": 0,
            "label_name": "apple",
            "lookup_score": 0.5,
            "attention_weight": 0.9,
            "memory_value": "apple",
            "memory_id": 2,
        },
        {
            "label": 1,
            "label_name": None,
            "lookup_score": 0.5,
            "attention_weight": 0.9,
            "memory_value": "banana",
            "memory_id": 1,
        },
    ],
    mean_memory_lookup_score=0.5,
    mean_memory_attention_weight=0.9,
    prediction=AnalyzePrediction(label=1, logits=[0.8999999761581421, 0.0000, 0.10000000149011612], confidence=0.9),
)


def test_explain_returns():
    stats = test_rac.explain(inpt="test")

    assert stats is not None
    assert stats == expected_stats
    # for key in stats.keys():
    #     if key != "prediction":
    #         assert stats[key] == expected_stats[key]
    #     else:
    #         for sub_key in stats[key].keys():
    #             if sub_key != "logits":
    #                 assert stats[key][sub_key] == expected_stats[key][sub_key]
    #             else:
    #                 assert stats[key][sub_key] == expected_stats[key][sub_key]


def test_explain_returns_with_prediction_result():
    stats = test_rac.explain(prediction_result=prediction_result)

    assert stats is not None
    assert stats == expected_stats
    # for key in stats.keys():
    #     if key != "prediction":
    #         assert stats[key] == expected_stats[key]
    #     else:
    #         for sub_key in stats[key].keys():
    #             if sub_key != "logits":
    #                 assert stats[key][sub_key] == expected_stats[key][sub_key]
    #             else:
    #                 assert stats[key][sub_key] == expected_stats[key][sub_key]
