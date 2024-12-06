from collections import defaultdict
from typing import Callable

import numpy as np
from prettytable import PrettyTable
from tqdm.auto import tqdm

from .memory_types import LabeledMemory, LabeledMemoryLookup


def _show_table(data: list[tuple[LabeledMemory, float, int]], k: int = 10, target_label: int | None = None):
    if target_label is not None:
        data = [d for d in data if d[0].label == target_label]
    table = PrettyTable()
    table.field_names = ["Suspicion Score", "Label", "Proposed Label", "Text"]
    for memory, score, better_label in data[:k]:
        assert isinstance(memory.value, str)
        table.add_row(
            [
                f"{score:.3f}",
                f"{memory.label_name}({memory.label})",
                better_label,
                memory.value.replace("\n", "  "),
            ]
        )
    table.align = "l"
    print(table)


def _best_label(data: dict[int, float]) -> tuple[int, float]:
    return max(data.items(), key=lambda x: x[1])


class LabeledMemorysetAnalysisResults:
    def __init__(
        self,
        memories: list[LabeledMemory],
        lookup: Callable[[np.ndarray, int], list[list[LabeledMemoryLookup]]],
        log: bool,
    ):
        self.lookup = lookup

        self.memories_with_scores = []
        for memory in tqdm(memories, disable=not log):
            suspicion_score, better_label = self._suspicion_score(memory)
            self.memories_with_scores.append((memory, suspicion_score, better_label))
        self.memories_with_scores.sort(key=lambda x: x[1], reverse=True)

    def _suspicion_score(self, memory: LabeledMemory) -> tuple[float, int]:
        assert memory.embedding is not None
        memory_lookups = self.lookup(memory.embedding, 11)[0][1:]
        label_weights = defaultdict(float)
        for mem in memory_lookups:
            assert isinstance(mem.label, int)
            assert mem.lookup_score is not None
            label_weights[mem.label] += mem.lookup_score
        normalization_factor = sum(label_weights.values())
        assert isinstance(memory.label, int)
        if normalization_factor == 0:
            return 0.0, memory.label
        return 1 - (label_weights[memory.label] / normalization_factor), _best_label(label_weights)[0]

    def show_outliers(self, k: int = 10, target_label: int | None = None):
        _show_table(self.memories_with_scores, k, target_label)

    def data_score(self, target_label: int | None = None):
        if target_label is not None:
            data = [d for d in self.memories_with_scores if d[0].label == target_label]
        else:
            data = self.memories_with_scores

        return sum(1 - score for _, score, _ in data) / len(data) if data else 0.0
