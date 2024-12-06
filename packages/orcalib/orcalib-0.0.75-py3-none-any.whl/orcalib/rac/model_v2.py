from __future__ import annotations

import logging
from contextlib import contextmanager
from enum import Enum
from typing import cast, overload

import numpy as np
import torch
from torch import Tensor, nn
from transformers import (
    AutoConfig,
    AutoModelForImageClassification,
    AutoModelForSequenceClassification,
    PretrainedConfig,
    PreTrainedModel,
)
from transformers.modeling_outputs import SequenceClassifierOutput

from orcalib.memoryset.memory_types import InputTypeList, LabeledMemoryLookup
from orcalib.rac.return_types import EvalResult, PredictionResult
from orcalib.rac_util import to_dataset

from ..memoryset import DatasetLike, InputType
from ..memoryset.memoryset_v2 import LabeledMemorysetV2
from ..torch_layers import (
    FeedForwardClassificationHead,
    MemoryMixtureOfExpertsClassificationHead,
    NearestMemoriesClassificationHead,
)
from .model_v2_finetuning import RACTrainingArguments, evaluate, finetune


class RACHeadType(str, Enum):
    KNN = "knn"
    MMOE = "mmoe"
    FF = "ff"


class RACModelConfig(PretrainedConfig):
    model_type = "rac-model"

    head_type: RACHeadType
    num_classes: int | None
    memoryset_uri: str | None
    memory_lookup_count: int | None
    weigh_memories: bool
    min_memory_weight: float | None
    num_layers: int | None
    dropout_prob: float | None

    def __init__(
        self,
        memoryset_uri: str | None = None,
        memory_lookup_count: int | None = None,
        head_type: RACHeadType | str = RACHeadType.MMOE,
        num_classes: int | None = None,
        weigh_memories: bool = False,
        min_memory_weight: float | None = None,
        num_layers: int | None = None,
        dropout_prob: float | None = None,
        **kwargs,
    ):
        """
        Initialize the config

        Note:
            While all args of a pretrained config must be optional, `memoryset_uri` must be specified.

        Args:
            memoryset_uri: URI of the memoryset to use, this is required
            memory_lookup_count: Number of memories to lookup for each input, defaults to 1.5 * num_classes rounded to the nearest 5
            head_type: Type of classification head to use
            num_classes: Number of classes to predict, will be inferred from memoryset if not specified
            weigh_memories: Optional parameter for KNN head, whether to weigh memories by their lookup score
            min_memory_weight: Optional parameter for KNN head, minimum memory weight under which memories are ignored
            num_layers: Optional parameter for FF head, number of layers in the feed forward network
            dropout_prob: Optional parameter for FF head, dropout probability
        """
        # We cannot require memoryset_uri here, because this class must be initializable without
        # passing any parameters for the PretrainedConfig.save_pretrained method to work, so instead
        # we throw an error in the RetrievalAugmentedClassifier initializer if it is missing
        self.memoryset_uri = memoryset_uri
        self.memory_lookup_count = memory_lookup_count
        self.head_type = head_type if isinstance(head_type, RACHeadType) else RACHeadType(head_type)
        self.num_classes = num_classes
        self.weigh_memories = weigh_memories
        self.min_memory_weight = min_memory_weight
        self.num_layers = num_layers
        self.dropout_prob = dropout_prob
        super().__init__(**kwargs)


class RACModelV2(PreTrainedModel):
    config_class = RACModelConfig
    base_model_prefix = "rac"

    def _init_head(self):
        # TODO: break this up into three subclasses that inherit from RACModelV2 and have their own con
        match self.config.head_type:
            case RACHeadType.MMOE:
                self.memory_lookup_count = self.config.memory_lookup_count or min(round(self.num_classes * 1.5) * 5, 50)
                self.head = MemoryMixtureOfExpertsClassificationHead(
                    num_classes=self.num_classes,
                    embedding_dim=self.embedding_dim,
                )
            case RACHeadType.KNN:
                self.memory_lookup_count = self.config.memory_lookup_count or min(round(self.num_classes * 1.5) * 5, 50)
                self.head = NearestMemoriesClassificationHead(
                    num_classes=self.num_classes,
                    weigh_memories=self.config.weigh_memories,
                    min_memory_weight=self.config.min_memory_weight,
                )
            case RACHeadType.FF:
                self.memory_lookup_count = 0
                self.head = FeedForwardClassificationHead(
                    num_classes=self.num_classes,
                    embedding_dim=self.embedding_dim,
                    num_layers=self.config.num_layers,
                )

    @overload
    def __init__(self, config: RACModelConfig):
        pass

    @overload
    def __init__(
        self,
        *,
        memoryset: LabeledMemorysetV2 | str,
        memory_lookup_count: int | None = None,
        head_type: RACHeadType | str = RACHeadType.MMOE,
        num_classes: int | None = None,
        weigh_memories: bool = False,
        min_memory_weight: float | None = None,
        num_layers: int | None = None,
        dropout_prob: float | None = None,
    ):
        pass

    def __init__(
        self,
        config: RACModelConfig | None = None,
        *,
        memoryset: LabeledMemorysetV2 | str | None = None,
        memory_lookup_count: int | None = None,
        head_type: RACHeadType | str = RACHeadType.MMOE,
        num_classes: int | None = None,
        weigh_memories: bool = False,
        min_memory_weight: float | None = None,
        num_layers: int | None = None,
        dropout_prob: float | None = None,
    ):
        if config is None:
            assert memoryset is not None
            if isinstance(memoryset, LabeledMemorysetV2):
                self.memoryset = memoryset
            else:
                self.memoryset = LabeledMemorysetV2(memoryset)
            config = RACModelConfig(
                memoryset_uri=self.memoryset.uri,
                memory_lookup_count=memory_lookup_count,
                head_type=head_type,
                num_classes=num_classes,
                weigh_memories=weigh_memories,
                min_memory_weight=min_memory_weight,
                num_layers=num_layers,
                dropout_prob=dropout_prob,
            )
        else:
            assert (
                memoryset is not None
                or memory_lookup_count is not None
                or head_type is not None
                or num_classes is not None
                or weigh_memories is not None
                or min_memory_weight is not None
                or num_layers is not None
                or dropout_prob is not None
            ), "Either config or kwargs can be provided, not both"
            if not config.memoryset_uri:
                # all configs must have defaults in a PretrainedConfig, but this one is required
                raise ValueError("memoryset_uri must be specified in config")
            self.memoryset = LabeledMemorysetV2(config.memoryset_uri)
        super().__init__(config)
        self.embedding_dim = self.memoryset.embedding_model.embedding_dim
        if config.num_classes is None:
            logging.warning("num_classes not specified in config, using number of classes in memoryset")
            self.num_classes = self.memoryset.num_classes
        else:
            self.num_classes = config.num_classes
        self._init_head()
        self.criterion = nn.CrossEntropyLoss() if config.num_labels > 1 else nn.MSELoss()

    @property
    def num_trainable_parameters(self) -> int:
        return self.num_parameters(only_trainable=True)

    def reset(self):
        self._init_head()

    def attach(self, memoryset: LabeledMemorysetV2 | str):
        self.memoryset = memoryset if isinstance(memoryset, LabeledMemorysetV2) else LabeledMemorysetV2(memoryset)

    def use(self, memoryset: LabeledMemorysetV2 | str):
        @contextmanager
        def ctx_manager():
            previous_memoryset = self.memoryset
            try:
                self.attach(memoryset)
                yield
            finally:
                if previous_memoryset:
                    self.attach(previous_memoryset)

        return ctx_manager()

    def forward(
        self,
        input_embeddings: Tensor | None = None,
        memories_labels: Tensor | None = None,
        memories_embeddings: Tensor | None = None,
        memories_weights: Tensor | None = None,
        labels: Tensor | None = None,
    ) -> SequenceClassifierOutput:
        logits = self.head(input_embeddings, memories_labels, memories_embeddings, memories_weights)
        loss = self.criterion(logits, labels) if labels is not None else None
        return SequenceClassifierOutput(loss=loss, logits=logits)

    def finetune(
        self,
        save_dir: str,
        train_data: DatasetLike | None = None,
        eval_data: DatasetLike | None = None,
        training_args: RACTrainingArguments = RACTrainingArguments(),
    ):
        train_data = self.memoryset.to_dataset() if train_data is None else train_data
        finetune(self, save_dir, to_dataset(train_data), to_dataset(eval_data) if eval_data else None, training_args)

    def evaluate(
        self,
        data: DatasetLike,
    ) -> EvalResult:
        eval_metrics = evaluate(self, to_dataset(data))
        return EvalResult(
            f1=eval_metrics["eval_f1_score"],
            roc_auc=eval_metrics["eval_roc_auc"],
            accuracy=eval_metrics["eval_accuracy"],
            loss=eval_metrics["eval_loss"],
        )

    @overload
    def predict(self, value: InputType) -> PredictionResult:
        pass

    @overload
    def predict(self, value: InputTypeList) -> list[PredictionResult]:
        pass

    @torch.no_grad()
    def predict(self, value: InputType | InputTypeList) -> PredictionResult | list[PredictionResult]:
        lookup_res = self.memoryset.lookup(
            [value] if not isinstance(value, list) else value,
            count=self.memory_lookup_count,
            return_type="columns",
        )
        logits = self.forward(
            input_embeddings=torch.tensor(lookup_res["input_embeddings"]).to(self.device),
            memories_labels=torch.tensor(lookup_res["memories_labels"]).to(self.device),
            memories_embeddings=torch.tensor(lookup_res["memories_embeddings"]).to(self.device),
            memories_weights=torch.tensor(lookup_res["memories_lookup_scores"]).to(self.device),
        ).logits
        predictions = torch.argmax(logits, dim=-1)
        results = [
            PredictionResult(
                label=int(prediction.item()),
                label_name=None,  # TODO: add once available
                confidence=float(logits[i][prediction].item()),
                logits=logits.to("cpu").numpy()[i],
                input_embedding=np.array(lookup_res["input_embeddings"][i], dtype=np.float32),
                memories=[
                    LabeledMemoryLookup(
                        value=memory_value,
                        embedding=np.array(memory_embedding, dtype=np.float32),
                        label=memory_label,
                        label_name=None,  # TODO: add once available
                        memory_id=memory_id,
                        memory_version=memory_version,
                        metadata=memory_metadata,
                        lookup_score=lookup_score,
                        reranker_score=reranker_score,
                        attention_weight=attention_weight,
                        reranker_embedding=None,  # TODO: add once available
                    )
                    for memory_value, memory_label, memory_embedding, memory_id, memory_version, memory_metadata, lookup_score, reranker_score, attention_weight in zip(
                        lookup_res["memories_values"][i],
                        lookup_res["memories_labels"][i],
                        lookup_res["memories_embeddings"][i],
                        lookup_res["memories_ids"][i],
                        lookup_res["memories_versions"][i],
                        lookup_res["memories_metadata"][i],
                        lookup_res["memories_lookup_scores"][i],
                        lookup_res["memories_reranker_scores"][i],
                        (
                            self.head.last_memories_attention_weights.tolist()[i]
                            if self.head.last_memories_attention_weights is not None
                            else []
                        ),
                    )
                ],
            )
            for i, prediction in enumerate(predictions)
        ]
        if not isinstance(value, list):
            return results[0]
        return results

    @classmethod
    def from_pretrained(cls, folder: str) -> RACModelV2:
        return cast(RACModelV2, super().from_pretrained(folder))


AutoConfig.register("rac-model", RACModelConfig)
AutoModelForSequenceClassification.register(RACModelConfig, RACModelV2)
AutoModelForImageClassification.register(RACModelConfig, RACModelV2)
