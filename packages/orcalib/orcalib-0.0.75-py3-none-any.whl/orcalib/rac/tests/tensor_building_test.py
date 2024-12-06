import torch

from orcalib.rac.head_models import _build_memory_tensor, _build_one_hot_label_tensor


def test_label_tensor_building():
    labels = [[1, 2, 3], [4, 5, 6]]
    num_classes = 10
    label_tensor = _build_one_hot_label_tensor(labels, num_classes)
    assert label_tensor.shape == (2, 3, 10)  # batch x memory_width x num_classes
    assert label_tensor[0, 0, 1] == 1
    assert label_tensor[0, 1, 2] == 1
    assert label_tensor[0, 2, 3] == 1
    assert label_tensor[1, 0, 4] == 1
    assert label_tensor[1, 1, 5] == 1
    assert label_tensor[1, 2, 6] == 1
    assert sum(label_tensor.flatten().tolist()) == 6


def test_memory_tensor_building():
    # batch size = 2, memory width = 3, embedding dim = 4
    memories = [
        [
            torch.tensor([1, 2, 3, 4]),
            torch.tensor([5, 6, 7, 8]),
            torch.tensor([9, 10, 11, 12]),
        ],
        [
            torch.tensor([13, 14, 15, 16]),
            torch.tensor([17, 18, 19, 20]),
            torch.tensor([21, 22, 23, 24]),
        ],
    ]
    memory_tensor = _build_memory_tensor(memories)
    assert memory_tensor.shape == (2, 4, 3)  # batch x memory_width x embedding_dim
    assert memory_tensor[0, 0, 0] == 1
    assert memory_tensor[0, 1, 0] == 2
    assert memory_tensor[0, 2, 0] == 3
    assert memory_tensor[0, 3, 0] == 4
    assert memory_tensor[1, 0, 2] == 21
    assert memory_tensor[1, 1, 2] == 22
    assert memory_tensor[1, 2, 2] == 23
