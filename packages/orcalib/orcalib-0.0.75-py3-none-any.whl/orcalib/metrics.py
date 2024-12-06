"""
This module contains metrics for usage with the Hugging Face Trainer.
"""

from typing import Literal, TypedDict

import numpy as np
from numpy._typing import NDArray
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from transformers.trainer_utils import EvalPrediction


class ClassificationMetrics(TypedDict):
    accuracy: float
    f1_score: float
    roc_auc: float | None


def compute_classifier_metrics(eval_pred: EvalPrediction) -> ClassificationMetrics:
    """
    Compute standard metrics for classifier with Hugging Face Trainer.

    Args:
        eval_pred: The predictions containing logits and expected labels as given by the Trainer.

    Returns:
        A dictionary containing the accuracy, f1 score, and ROC AUC score.
    """
    logits, references = eval_pred
    if isinstance(logits, tuple):
        logits = logits[0]
    if not isinstance(logits, np.ndarray):
        raise ValueError("Logits must be a numpy array")
    if not isinstance(references, np.ndarray):
        raise ValueError(
            "Multiple label columns found, use the `label_names` training argument to specify which one to use"
        )
    num_labels = logits.shape[1]
    predictions: NDArray[np.int_] = np.argmax(logits, axis=-1)
    if num_labels < 2:
        raise ValueError("Logits are 1 dimensional, use a different metric function for regression tasks")
    average = None if num_labels == 2 else "weighted"
    return classification_scores(references, predictions, average=average)


def classification_scores(
    references: list[int] | NDArray[np.int_],
    predictions: list[int] | NDArray[np.int_],
    average: Literal["micro", "macro", "weighted", "binary"] | None = None,
    multi_class: Literal["ovr", "ovo"] = "ovr",
) -> ClassificationMetrics:
    num_classes_references = len(set(references))
    num_classes_predictions = len(set(predictions))
    if average is None:
        average = "binary" if num_classes_references == 2 else "weighted"
    return {
        "accuracy": float(accuracy_score(references, predictions)),
        "f1_score": float(f1_score(references, predictions, average=average)),
        "roc_auc": (
            float(roc_auc_score(references, predictions, multi_class=multi_class))
            if num_classes_references == num_classes_predictions
            else None
        ),
    }
