from collections import Counter

from datasets import Dataset, DatasetDict

from orcalib.rac.drift_simulator import drift_classes


def test_drift_classes_from_dataset_dict():
    #  Create a balanced dataset dict with one feature, 2 classes, and 100 rows
    train = {"train": []}
    for label in range(2):
        for j in range(50):
            train["train"].append(
                {
                    "value": f"value_{j}",
                    "label": label,
                }
            )
    input_dataset_dict: DatasetDict = DatasetDict({"train": Dataset.from_dict(train)["train"]})

    balanced_label_counts = Counter(item["label"] for item in input_dataset_dict["train"])  # type: ignore
    assert balanced_label_counts[0] == 50

    #  Drift the dataset to have 10% of class 0
    new_dataset_dict = drift_classes(input_dataset_dict, {0: 0.1})
    imbalanced_label_counts = Counter(item["label"] for item in new_dataset_dict["train"])  # type: ignore
    assert imbalanced_label_counts[0] == 5
    assert imbalanced_label_counts[1] == 50


def test_drift_classes_from_dataset():
    #  Create a balanced dataset with 2 classes and 100 rows
    train = []
    for label in range(2):
        for j in range(50):
            train.append(
                {
                    "value": f"value_{j}",
                    "label": label,
                }
            )
    input_dataset = Dataset.from_list(train)
    balanced_label_counts = Counter(item["label"] for item in input_dataset)  # type: ignore
    assert balanced_label_counts[0] == 50

    #  Drift the dataset to have 10% of class 0
    new_dataset = drift_classes(input_dataset, {0: 0.1})
    imbalanced_label_counts = Counter(item["label"] for item in new_dataset)  # type: ignore
    assert imbalanced_label_counts[0] == 5
    assert imbalanced_label_counts[1] == 50
