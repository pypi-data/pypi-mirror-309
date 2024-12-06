import json
import uuid
from typing import Any, cast

import numpy as np
import pandas as pd
import pytest
from datasets import Dataset
from PIL import Image
from torch.utils.data import DataLoader as TorchDataLoader
from torch.utils.data import Dataset as TorchDataset

from .memory_types import InputType, LabeledMemory
from .util import MemoryToInsert, transform_data_to_dict_list

#################### Transforming to and from LabeledMemorys ####################


def test_transform_data_to_dict_list_from_labeled_memories():
    # Test case 1: LabeledMemory input
    embedding = np.random.rand(768)
    memory_id = str(uuid.uuid4())
    memories_to_insert = transform_data_to_dict_list(
        LabeledMemory(
            value="National Parks are fun",
            label=1,
            label_name="Outdoor Recreation",
            metadata={},
            memory_version=3,
            memory_id=memory_id,
            embedding=embedding,
        )
    )
    assert len(memories_to_insert) == 1
    assert memories_to_insert[0]["text"] == "National Parks are fun"
    assert memories_to_insert[0]["image"] is None
    assert memories_to_insert[0]["label"] == 1
    assert memories_to_insert[0]["label_name"] == "Outdoor Recreation"
    assert memories_to_insert[0]["metadata"] is None
    assert memories_to_insert[0]["memory_version"] == 3
    assert memories_to_insert[0]["embedding"] == embedding.tolist()
    assert memories_to_insert[0]["memory_id"] == memory_id

    # Test case 2: list of LabeledMemory input
    embeddings = [np.random.rand(768) for _ in range(2)]
    memory_ids = [str(uuid.uuid4()) for _ in range(2)]
    memories_to_insert = transform_data_to_dict_list(
        [
            LabeledMemory(
                value="National Parks are fun",
                label=1,
                label_name="Outdoor Recreation",
                metadata={},
                memory_version=2,
                memory_id=memory_ids[0],
                embedding=embeddings[0],
            ),
            LabeledMemory(
                value=Image.open("./orcalib/rac/tests/test_image.png"),
                label=1,
                label_name="Outdoor Recreation",
                metadata={},
                memory_version=1,
                memory_id=memory_ids[1],
                embedding=embeddings[1],
            ),
        ]
    )
    assert len(memories_to_insert) == 2

    assert memories_to_insert[0]["text"] == "National Parks are fun"
    assert memories_to_insert[0]["image"] is None
    assert memories_to_insert[0]["label"] == 1
    assert memories_to_insert[0]["label_name"] == "Outdoor Recreation"
    assert memories_to_insert[0]["metadata"] is None
    assert memories_to_insert[0]["memory_version"] == 2
    assert memories_to_insert[0]["embedding"] == embeddings[0].tolist()
    assert memories_to_insert[0]["memory_id"] == memory_ids[0]

    assert memories_to_insert[1]["text"] is None
    assert memories_to_insert[1]["image"] == Image.open("./orcalib/rac/tests/test_image.png")
    assert memories_to_insert[1]["label"] == 1
    assert memories_to_insert[1]["label_name"] == "Outdoor Recreation"
    assert memories_to_insert[1]["metadata"] is None
    assert memories_to_insert[1]["memory_version"] == 1
    assert memories_to_insert[1]["embedding"] == embeddings[1].tolist()
    assert memories_to_insert[1]["memory_id"] == memory_ids[1]


inputs = [
    {
        "value": "value1",
        "label": 1,
        "label_name": "label_name1",
        "metadata": {"value_metadata": "metadata1"},
    },
    {
        "value": "value2",
        "label": 2,
        "label_name": "label_name2",
        "metadata": {"value_metadata": "metadata2"},
    },
]

expected_memories_to_insert: list[MemoryToInsert] = [
    {
        "text": "value1",
        "image": None,
        "label": 1,
        "label_name": "label_name1",
        "metadata": json.dumps({"value_metadata": "metadata1"}),
        "memory_version": 1,
        "embedding": None,
        "memory_id": None,
    },
    {
        "text": "value2",
        "image": None,
        "label": 2,
        "label_name": "label_name2",
        "metadata": json.dumps({"value_metadata": "metadata2"}),
        "memory_version": 1,
        "embedding": None,
        "memory_id": None,
    },
]

expected_simple_memory_to_insert: MemoryToInsert = {
    "text": "this is text",
    "image": None,
    "label": 3,
    "label_name": None,
    "metadata": None,
    "memory_version": 1,
    "embedding": None,
    "memory_id": None,
}

expected_simple_memory_to_insert_with_label_name: MemoryToInsert = {
    "text": None,
    "image": Image.open("./orcalib/rac/tests/test_image.png"),
    "label": 3,
    "label_name": "label_name",
    "metadata": None,
    "memory_version": 1,
    "embedding": None,
    "memory_id": None,
}


@pytest.mark.parametrize(
    "input, expected_memories",
    [
        (inputs[0], [expected_memories_to_insert[0]]),
        (inputs, expected_memories_to_insert),
        (
            [{"label": 3, "text": "this is text"}],
            [expected_simple_memory_to_insert],
        ),
        (
            [{"label": 3, "image": Image.open("./orcalib/rac/tests/test_image.png"), "label_name": "label_name"}],
            [expected_simple_memory_to_insert_with_label_name],
        ),
    ],
)
def test_transform_data_to_dict_list_from_dict(
    input: dict | list[dict], expected_memories: LabeledMemory | list[LabeledMemory]
):
    assert transform_data_to_dict_list(input) == expected_memories


@pytest.mark.parametrize(
    "input",
    [
        [{"label": 3}],
        {"label": 3, "not_correct_value_key": "this is text", "something_else": "this is ignored"},
        {"value": 12, "label": 1},
        {"value": "test", "label": "string"},
        {"text": "test", "label": ("string")},
        {"value": "test", "label": 1, "label_name": 2},
        {"text": "test", "label": 1, "label_name": "test", "metadata": 2},
        {"value": "test", "label": 1, "label_name": "test", "metadata": "string"},
    ],
)
def test_transform_data_to_dict_list_errors(input: dict | list[dict]):
    with pytest.raises(ValueError):
        transform_data_to_dict_list(input)


def test_transform_data_to_dict_list_from_tuple():
    # list of tuples input
    data: list[tuple[InputType, int]] = [
        (
            cast(InputType, "value1"),
            1,
        )
    ]
    expected_memory_to_insert: MemoryToInsert = {
        "text": "value1",
        "image": None,
        "label": 1,
        "label_name": None,
        "metadata": None,
        "memory_version": 1,
        "embedding": None,
        "memory_id": None,
    }
    assert transform_data_to_dict_list(data) == [expected_memory_to_insert]


def test_transform_data_to_dict_list_from_tuple_error():
    # list of tuples input
    data = [(cast(InputType, "value1"), 1, "something else")]

    with pytest.raises(ValueError):
        transform_data_to_dict_list(data)  # type: ignore -- testing bad type


def test_transform_data_to_dict_list_from_dataframe():
    # pd.DataFrame input
    data = pd.DataFrame(
        [
            {
                "value": "value1",
                "label": 1,
                "label_name": "label_name1",
                "metadata": {"value_metadata": "metadata1"},
            },
            {
                "value": "value2",
                "label": 2,
                "label_name": "label_name2",
                "metadata": {"value_metadata": "metadata2"},
            },
        ]
    )
    assert transform_data_to_dict_list(data) == expected_memories_to_insert


def test_transform_data_to_dict_list_from_hf_dataset():
    # HuggingFace Dataset input

    data = Dataset.from_dict(
        {
            "value": ["Sea turtles are really cool"],
            "label": [0],
            "label_name": ["sea animals"],
            "metadata": [{"value_metadata": "metadata"}],
            "memory_version": [1],
        }
    )
    expected_memory_to_insert: MemoryToInsert = {
        "text": "Sea turtles are really cool",
        "image": None,
        "label": 0,
        "label_name": "sea animals",
        "metadata": json.dumps({"value_metadata": "metadata"}),
        "memory_version": 1,
        "embedding": None,
        "memory_id": None,
    }

    assert transform_data_to_dict_list(data) == [expected_memory_to_insert]


def test_transform_data_to_dict_list_from_torch_dataset():
    #  TorchDataset and TorchDataLoader input

    class TorchDatasetSubclassed(TorchDataset):
        def __init__(
            self,
            value: list[str],
            label: list[int],
            label_name: list[str | None],
            metadata: list[dict[str, Any] | None],
            memory_version: list[int],
        ):
            self.value = value
            self.label = label
            self.label_name = label_name
            self.metadata = metadata
            self.memory_version = memory_version

        def __getitem__(self, idx):
            return {
                "value": self.value[idx],
                "label": self.label[idx],
                "label_name": self.label_name[idx],
                "metadata": self.metadata[idx],
                "memory_version": self.memory_version[idx],
            }

        def __len__(self):
            return len(self.value)

    # Sample Data
    data_dict = {
        "value": ["test", "bread", "air", "bread", "test"],
        "label": [0, 1, 2, 1, 0],
    }
    torch_dataset = TorchDatasetSubclassed(
        value=data_dict["value"],
        label=data_dict["label"],
        label_name=[None, "None", None, None, None],
        metadata=[None, {"foo": "bar"}, None, None, None],
        memory_version=[1, 1, 1, 1, 1],
    )

    def collate(item):
        if item is None:
            return item
        return item

    torch_dataloader = TorchDataLoader(torch_dataset, batch_size=1, collate_fn=collate)

    memories: list[MemoryToInsert] = [
        {
            "text": "test",
            "image": None,
            "embedding": None,
            "label": 0,
            "label_name": None,
            "memory_version": 1,
            "metadata": None,
            "memory_id": None,
        },
        {
            "text": "bread",
            "image": None,
            "embedding": None,
            "label": 1,
            "label_name": "None",
            "metadata": json.dumps({"foo": "bar"}),
            "memory_version": 1,
            "memory_id": None,
        },
        {
            "text": "air",
            "image": None,
            "embedding": None,
            "label": 2,
            "label_name": None,
            "memory_version": 1,
            "metadata": None,
            "memory_id": None,
        },
        {
            "text": "bread",
            "image": None,
            "embedding": None,
            "label": 1,
            "label_name": None,
            "memory_version": 1,
            "metadata": None,
            "memory_id": None,
        },
        {
            "text": "test",
            "image": None,
            "embedding": None,
            "label": 0,
            "label_name": None,
            "memory_version": 1,
            "metadata": None,
            "memory_id": None,
        },
    ]
    assert transform_data_to_dict_list(torch_dataset) == memories
    assert transform_data_to_dict_list(torch_dataloader) == memories
