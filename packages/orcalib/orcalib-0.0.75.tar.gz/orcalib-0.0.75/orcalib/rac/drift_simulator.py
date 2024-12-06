import random
from collections import defaultdict

import pandas as pd
import plotly.graph_objects as go
from datasets import Dataset, DatasetDict, IterableDataset, IterableDatasetDict
from plotly.subplots import make_subplots

from orcalib.memoryset import EmbeddingModel, LabeledMemoryset
from orcalib.rac import RACModel

from .rac import TrainingConfig
from .visualization import plot_model_performance_comparison

default_memoryset_config = {
    "base_uri": "http://localhost:1583",
    "db_name": "default",
    "api_key": "my_api_key",
    "secret": "my_secret_key",
}

training_config = TrainingConfig(epochs=2, lr=1e-4, batch_size=64)


def drift_classes(dataset: DatasetDict | Dataset, drift_ratios: dict[int, float]) -> DatasetDict | Dataset:
    """
    Modify a balanced Huggingface dataset into an unequal distribution.

    Args:
        dataset: The Huggingface dataset (assumed balanced).
        drift_ratios: A dictionary where keys are class ints, and values are the desired proportion
            of samples to retain (e.g., {0: 0.5, 1: 0.2, 2: 1.0}). If a key is missing it will be unchanged.

    Returns:
        A new dataset with drifted class distributions.
    """

    def drift_dataset(dataset: Dataset, drift_ratios: dict) -> Dataset:
        # Define a generator that yields downsampled items directly
        def downsampled_generator(dataset):
            class_groups = defaultdict(list)
            for item in dataset:
                label = item["label"]
                class_groups[label].append(item)

                # Once a class reaches the target size, yield the downsampled items
                if len(class_groups[label]) > 1000:  # Arbitrary chunk size to avoid too large memory usage
                    yield from downsample_class(label, class_groups[label], drift_ratios)
                    class_groups[label] = []  # Clear the class group to free memory

            # Process any remaining samples for each class
            for label, group in class_groups.items():
                yield from downsample_class(label, group, drift_ratios)

        def downsample_class(label, group, drift_ratios):
            retain_count = int(len(group) * drift_ratios.get(label, 1.0))
            return random.sample(group, retain_count)

        # Use the generator to create the final dataset
        final = Dataset.from_generator(lambda: downsampled_generator(dataset))
        assert isinstance(final, Dataset)
        return final

    def drift_dataset_dict(input_dataset: DatasetDict, drift_ratios: dict) -> DatasetDict:
        drifted_datasets_dict = {}
        for dataset_name, dataset in input_dataset.items():
            # Create a new datasetDict from the drifted samples
            drifted_dataset = drift_dataset(dataset, drift_ratios)
            drifted_datasets_dict[dataset_name] = drifted_dataset
        return DatasetDict(drifted_datasets_dict)

    if isinstance(dataset, DatasetDict):
        return drift_dataset_dict(dataset, drift_ratios)
    else:
        return drift_dataset(dataset, drift_ratios)


def test_dataset_drift(
    dataset: Dataset | IterableDataset | IterableDatasetDict | DatasetDict,
    drift_ratios: dict[int, float],
    model_a_config: dict,
    model_b_config: dict,
    memoryset_config: dict[str, str] = default_memoryset_config,
    training_config_a: TrainingConfig = training_config,
    training_config_b: TrainingConfig = training_config,
    graph_config: dict[str, str] = {"title": "Drift performance comparison", "xaxis": "Metrics", "yaxis": "Score"},
    dataset_name: str | None = None,
):
    """
    Evaluate the performance of two models on a dataset that has been artificially drifted.

    Args:
        dataset: huggingface dataset
        drift_ratios: A dictionary of class to drift ratio ex {0: 0.1, 1: 0.2}
        model_a_config: Configuration for model A
        model_b_config: Configuration for model B
        memoryset_config: Configuration for where memorysets are stored. Defaults to default_memoryset_config.
        training_config_a: Training configuration for the first model.
        training_config_b: Training configuration for the second model.
        graph_config: Configuration for the graph titles / axis labels. Defaulted to {"title": "Drift performance comparison", "xaxis": "Metrics", "yaxis": "Score"}

    Info:
        This prints a graph that compares the performance (f1,roc_auc,accuracy) of the models before and after the drift.
    """
    memoryset_config = {**default_memoryset_config, **memoryset_config}

    def create_uri(base_uri, db_name, memoryset_name):
        if base_uri.startswith("file://"):
            return f"{base_uri}#{memoryset_name}"
        return f"{base_uri}/{db_name}#{memoryset_name}"

    # Init memorysets
    starting_memoryset = LabeledMemoryset(
        create_uri(memoryset_config["base_uri"], memoryset_config["db_name"], "starting_memoryset"),
        memoryset_config["api_key"],
        memoryset_config["secret"],
        embedding_model=EmbeddingModel.GTE_BASE,
    )
    ending_memoryset = LabeledMemoryset(
        create_uri(memoryset_config["base_uri"], memoryset_config["db_name"], "ending_memoryset"),
        memoryset_config["api_key"],
        memoryset_config["secret"],
        embedding_model=EmbeddingModel.GTE_BASE,
    )

    assert isinstance(dataset, DatasetDict)
    ending_dataset = dataset

    # Create class imbalance
    starting_dataset = drift_classes(ending_dataset, drift_ratios=drift_ratios)
    results = {}

    # insert data into memorysets
    starting_memoryset.insert(starting_dataset["train"])
    ending_memoryset.insert(ending_dataset["train"])

    # Create Model A
    A = RACModel(
        memoryset=starting_memoryset,
        **model_a_config,
    )

    # finetune on starting dataset
    A.finetune(starting_dataset["train"], log=True, config=training_config_a)

    # eval after tuning
    results["a_pre_drift"] = A.evaluate(starting_dataset["test"]).__dict__

    # Attach the drifted memoryset and evaluate against the drifted dataset
    A.attach(ending_memoryset)
    results["a_post_drift"] = A.evaluate(ending_dataset["test"]).__dict__

    # Create Model B
    B = RACModel(
        memoryset=starting_memoryset,
        **model_b_config,
    )

    # finetune on starting dataset
    B.finetune(starting_dataset["train"], log=True, config=training_config_b)
    results["b_pre_drift"] = B.evaluate(starting_dataset["test"]).__dict__

    # Attach the drifted memoryset and evaluate against the drifted dataset
    B.attach(ending_memoryset)
    results["b_post_drift"] = B.evaluate(ending_dataset["test"]).__dict__

    labels = {
        "a_pre_drift": "Model A Pre Drift",
        "a_post_drift": "Model A Post Drift W/Added Memories",
        "b_pre_drift": "Model B Pre Drift",
        "b_post_drift": "Model B Post Drift W/Added Memories",
    }

    if dataset_name:
        graph_config["title"] = f"Drift performance comparison: {dataset_name}"

    metrics = ["f1", "roc_auc", "accuracy"]
    plot_model_performance_comparison(results, labels, metrics, graph_config)

    f1_data = {
        "Model A": [results["a_pre_drift"]["f1"], results["a_post_drift"]["f1"]],
        "Model B": [results["b_pre_drift"]["f1"], results["b_post_drift"]["f1"]],
    }
    roc_auc_data = {
        "Model A": [results["a_pre_drift"]["roc_auc"], results["a_post_drift"]["roc_auc"]],
        "Model B": [results["b_pre_drift"]["roc_auc"], results["b_post_drift"]["roc_auc"]],
    }
    accuracy_data = {
        "Model A": [results["a_pre_drift"]["accuracy"], results["a_post_drift"]["accuracy"]],
        "Model B": [results["b_pre_drift"]["accuracy"], results["b_post_drift"]["accuracy"]],
    }

    # Create dataframes
    f1_df = pd.DataFrame(f1_data, index=["Pre drift", "Post drift"]).T
    roc_auc_df = pd.DataFrame(roc_auc_data, index=["Pre drift", "Post drift"]).T
    accuracy_df = pd.DataFrame(accuracy_data, index=["Pre drift", "Post drift"]).T

    def create_table(df: pd.DataFrame, title: str):
        # Create table
        header = dict(
            values=[title] + list(df.columns),
            fill_color="green",
            align="center",
            font=dict(color="white", size=17),
            line=dict(color="black", width=1),
        )

        # Set fill color and background for the first column separately
        fill_colors = [["green"] * len(df.index)] + [["white"] * len(df.index) for _ in df.columns]
        font_colors = [["white"] * len(df.index)] + [["black"] * len(df.index) for _ in df.columns]

        # Update fill color for the highest value in each row
        for row_idx, (i, row) in enumerate(df.iterrows()):
            max_value = row.max()
            for col_idx, col in enumerate(df.columns):
                if row[col] == max_value:
                    fill_colors[col_idx + 1][row_idx] = "lightgreen"  # Change the background color of the highest value

        cells = dict(
            values=[df.index] + [df[col] for col in df.columns],
            fill_color=fill_colors,
            align="center",
            font=dict(color=font_colors, size=15),
            line=dict(color="black", width=1),
            height=40,
        )
        table = go.Table(header=header, cells=cells)
        return table

    # Create subplots
    fig = make_subplots(
        rows=3,
        cols=1,
        subplot_titles=("F1", "ROC AUC", "Accuracy"),
        vertical_spacing=0.01,
        specs=[[{"type": "table"}], [{"type": "table"}], [{"type": "table"}]],
    )

    # Add tables to subplots
    fig.add_trace(create_table(f1_df, ""), row=1, col=1)
    fig.add_trace(create_table(roc_auc_df, ""), row=2, col=1)
    fig.add_trace(create_table(accuracy_df, ""), row=3, col=1)

    # Update layout
    fig.update_layout(
        height=700, showlegend=False, title_text=f"Drift comparison {dataset_name if dataset_name else ''}"
    )

    # Show figure
    fig.show()
