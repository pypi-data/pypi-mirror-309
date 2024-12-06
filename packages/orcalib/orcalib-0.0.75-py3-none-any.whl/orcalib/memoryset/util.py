import hashlib
import io
import json
import uuid
from collections.abc import Mapping
from typing import Any, TypedDict, cast

import numpy as np
import pandas as pd
from datasets import Dataset
from PIL import Image
from torch.utils.data import DataLoader as TorchDataLoader
from torch.utils.data import Dataset as TorchDataset

from orcalib import ColumnName

from .memory_types import DatasetLike, InputType, LabeledMemory


def get_embedding_hash(q: np.ndarray) -> str:
    query_bytes = q.tobytes()
    hash_obj = hashlib.sha256()
    hash_obj.update(query_bytes)
    return hash_obj.hexdigest()


def pil_image_to_bytes(image: Image.Image, format: str = "JPEG") -> bytes:
    if not isinstance(image, Image.Image):
        raise ValueError("Image must be a PIL Image.")

    byte_array = io.BytesIO()
    if format == "JPEG":
        image = image.convert("RGB")
    image.save(byte_array, format=format)
    byte_data = byte_array.getvalue()
    return byte_data


# Convert Bytes to PIL Image
def bytes_to_pil_image(byte_data: bytes) -> Image.Image:
    if not isinstance(byte_data, bytes):
        raise ValueError("Data must be bytes.")

    byte_array = io.BytesIO(byte_data)
    image = Image.open(byte_array)
    return image


class MemoryToInsert(TypedDict):
    text: str | None
    image: Image.Image | None
    label: int
    label_name: str | None
    metadata: str | None
    memory_id: str | None
    embedding: list[float] | None
    memory_version: int


def _transform_to_memory_to_insert_dict(item: LabeledMemory | Mapping | tuple) -> MemoryToInsert:
    match item:
        case LabeledMemory():
            memory_to_insert: MemoryToInsert = {
                "text": item.value if isinstance(item.value, str) else None,
                "image": item.value if isinstance(item.value, Image.Image) else None,
                "label": item.label,
                "label_name": item.label_name,
                "metadata": json.dumps(item.metadata) if item.metadata else None,
                "embedding": item.embedding.tolist() if item.embedding is not None else None,
                "memory_version": item.memory_version,
                "memory_id": item.memory_id,
            }
            return memory_to_insert
        # This also handles the dict case
        case Mapping():
            label = item["label"]
            if label is None:
                raise ValueError("Label must be provided.")
            label_name = item.get("label_name", None)
            metadata = item.get("metadata", None)
            embedding = item.get("embedding", None)
            if "value" in item:
                value = item["value"]
            elif "text" in item:
                value = item["text"]
            elif "image" in item:
                value = item["image"]
            else:
                keys = [k for k in item.keys() if k != "label" and k != "label_name" and k != "metadata"]
                if len(keys) == 1:
                    value = item[keys[0]]
                else:
                    raise ValueError("No 'value' column found and one could not be inferred.")

            ## Validate dictionary values ##

            # if value is bytes, transform to image before validation
            value = bytes_to_pil_image(value) if isinstance(value, bytes) else value

            # value validation
            if not isinstance(value, InputType):
                raise ValueError("value must be a string or PIL Image.")

            # Label validation
            if not isinstance(label, int):
                try:
                    label = int(label)
                except ValueError as e:
                    raise ValueError(f"Label must be an int: {e}")

            # Label name validation
            if label_name is not None and not isinstance(label_name, str):
                raise ValueError("Label name must be a string.")

            # Metadata validation
            if metadata is not None:
                if not isinstance(metadata, (str, dict)):
                    raise ValueError("Metadata must be a JSON-serializable string or dict.")
                if isinstance(metadata, str):
                    try:
                        metadata = json.loads(metadata)
                    except json.JSONDecodeError:
                        raise ValueError("Metadata must be a JSON-serializable string or dict.")

            if embedding is not None and (not isinstance(embedding, np.ndarray) or len(embedding.shape) != 1):
                raise ValueError("Embedding must be a 1D numpy array.")

            memory_to_insert: MemoryToInsert = {
                "text": value if isinstance(value, str) else None,
                "image": value if isinstance(value, Image.Image) else None,
                "label": label,
                "label_name": label_name,
                "metadata": json.dumps(metadata) if metadata else None,
                "embedding": embedding.tolist() if embedding is not None else None,
                "memory_version": 1,
                "memory_id": None,
            }
            return memory_to_insert

        case tuple():
            if len(item) == 2 and isinstance(item[0], InputType) and (isinstance(item[1], int)):
                memory_to_insert: MemoryToInsert = {
                    "text": item[0] if isinstance(item[0], str) else None,
                    "image": item[0] if isinstance(item[0], Image.Image) else None,
                    "label": item[1],
                    "label_name": None,
                    "metadata": None,
                    "embedding": None,
                    "memory_version": 1,
                    "memory_id": None,
                }
                return memory_to_insert
            else:
                raise ValueError(
                    "Tuple must only have two elements; the first being the data and the second being the label."
                )
        case _:
            raise ValueError(f"Item must be a LabeledMemory, a Mapping, or a tuple: {type(item)}")


def transform_data_to_dict_list(data: DatasetLike) -> list[MemoryToInsert]:
    match data:
        case LabeledMemory():
            return [_transform_to_memory_to_insert_dict(data)]
        case dict():
            return [_transform_to_memory_to_insert_dict(data)]
        case list():
            return [_transform_to_memory_to_insert_dict(item) for item in data]
        case pd.DataFrame():
            return [_transform_to_memory_to_insert_dict(item) for item in data.to_dict("records")]
        case Dataset():
            return [_transform_to_memory_to_insert_dict(item) for item in data]  # type: ignore -- For our purposes, we can assume the item type is a Mapping
        case TorchDataset():
            return [_transform_to_memory_to_insert_dict(item) for item in data]
        case TorchDataLoader():
            return [_transform_to_memory_to_insert_dict(item[0]) for item in data]
        case _:
            raise ValueError(
                f"Dataset must be a list of tuples, dicts, or LabeledMemories, or a single DataFrame, HuggingFace Dataset, Torch Dataset, Torch Data Loader, LabeledMemory, or dict: {type(data)}"
            )


def transform_data_to_dataset(data: DatasetLike) -> Dataset:
    if isinstance(data, Dataset) and "value" in data.column_names and "label" in data.column_names:
        return data.select_columns(["value", "label"])
    transformed_data = transform_data_to_dict_list(data)
    return Dataset.from_dict(
        {
            "value": [cast(InputType, m["text"] or m["image"]) for m in transformed_data],
            "label": [m["label"] for m in transformed_data],
        }
    )


class MemoryRecord(TypedDict):
    id: str
    text: str | None
    image: bytes | None
    label: int
    label_name: str | None
    embedding: np.ndarray
    metadata: str


def transform_rows_to_labeled_memories(
    memory_records: list[dict[str, Any]] | list[tuple[int, dict[ColumnName, Any]]]
) -> list[LabeledMemory]:
    if len(memory_records) == 0:
        return []
    if isinstance(memory_records[0], tuple):
        memory_records = cast(list[tuple[int, dict[ColumnName, Any]]], memory_records)
        memory_records = [{"_rowid": memory_record[0], **memory_record[1]} for memory_record in memory_records]

    memoryset: list[LabeledMemory] = []
    for record in memory_records:
        memory_record = cast(MemoryRecord, record)
        label = memory_record.get("label", None)
        if label is None:
            raise ValueError("Label must be provided.")
        else:
            metadata = memory_record.get("metadata", None)
            embedding = memory_record.get("embedding")
            if isinstance(embedding, list):
                embedding = np.array(embedding)
            memoryset.append(
                LabeledMemory(
                    value=memory_record.get("value", memory_record.get("text", memory_record.get("image", None))),
                    label=label,
                    label_name=memory_record.get("label_name", None),
                    embedding=embedding,
                    metadata=json.loads(metadata) if metadata else {},
                    memory_version=memory_record.get("memory_version", 1),
                    memory_id=memory_record.get("memory_id", str(uuid.uuid4())),
                )
            )
    return memoryset
