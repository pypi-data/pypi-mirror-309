from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np
import typer
import yaml
from rich import print
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.tree import DecisionTreeClassifier

from mlops_misis.config import Config, ModelType, cfg_helper
from mlops_misis.dataset import Dataset, generate_dataset

app = typer.Typer()


@dataclass
class Metrics:
    """Metrics class."""

    accuracy: float
    precision: float
    recall: float
    f1_score: float

    def save(self, run_name: str) -> None:
        """Save the metrics to the specified path (reports/run_name/metrics.yaml).

        Parameters
        ----------
        run_name : str
            Name of the run to save.
        """

        report_path = Path(cfg_helper.base_reports_dir) / run_name
        report_path.mkdir(parents=True, exist_ok=True)
        with open(report_path / "metrics.yaml", "w") as file:
            yaml.dump(self.__dict__, file)

    def __str__(self):
        return (
            f"Metrics:\n"
            f"  Accuracy:  {self.accuracy:.4f}\n"
            f"  Precision: {self.precision:.4f}\n"
            f"  Recall:    {self.recall:.4f}\n"
            f"  F1 Score:  {self.f1_score:.4f}\n"
        )


def train_model(
    config: Config, dataset: Dataset
) -> LogisticRegression | DecisionTreeClassifier | RandomForestClassifier:
    """Train the model based on the configuration and dataset.

    Parameters
    ----------
    config : Config
        Configuration object.
    dataset : Dataset
        Dataset object.

    Returns
    -------
    LogisticRegression | DecisionTreeClassifier | RandomForestClassifier
        Trained model.

    Raises
    ------
    ValueError
        If the model type is unknown
    """
    model_type = config.ml_model_params.ml_model_type
    if model_type == ModelType.LOG_REG:
        model = LogisticRegression(
            C=config.ml_model_params.C, random_state=config.ml_model_params.random_state
        )
    elif model_type == ModelType.DECISION_TREE:
        model = DecisionTreeClassifier(
            max_depth=config.ml_model_params.max_depth,
            random_state=config.ml_model_params.random_state,
        )
    elif model_type == ModelType.RANDOM_FOREST:
        model = RandomForestClassifier(
            max_depth=config.ml_model_params.max_depth,
            n_estimators=config.ml_model_params.n_estimators,
            random_state=config.ml_model_params.random_state,
        )
    else:
        raise ValueError(f"Unknown model type: {model_type}")

    print(":gear: [bold green]Training model...[/bold green]")
    model.fit(dataset.X_train, dataset.y_train)

    run_name = config.ml_model_params.run_name
    model_path = Path(config.base_models_dir) / run_name
    model_path.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path / f"{model_type.value}_model.pkl")

    print(
        f":floppy_disk: [bold blue]Model saved to {model_path / f'{model_type.value}_model.pkl'}[/bold blue]"
    )

    return model


def validate_model(
    model: LogisticRegression | DecisionTreeClassifier | RandomForestClassifier,
    dataset: Dataset,
    run_name: str,
) -> Metrics:
    """Validate the model based on the dataset and save the metrics.

    Parameters
    ----------
    model : LogisticRegression | DecisionTreeClassifier | RandomForestClassifier
        Trained model.
    dataset : Dataset
        Dataset object.
    run_name : str
        Name of the run.

    Returns
    -------
    Metrics
        Metrics object.
    """
    print(":mag: [bold green]Validating model...[/bold green]")
    y_pred = model.predict(dataset.X_test)
    metrics = Metrics(
        accuracy=accuracy_score(dataset.y_test, y_pred),
        precision=precision_score(dataset.y_test, y_pred, average="weighted").item(),
        recall=recall_score(dataset.y_test, y_pred, average="weighted").item(),
        f1_score=f1_score(dataset.y_test, y_pred, average="weighted").item(),
    )

    metrics.save(run_name)
    print(f":floppy_disk: [bold blue]Metrics saved to reports/{run_name}/metrics.yaml[/bold blue]")
    return metrics


def predict_run(
    config: Config,
    X: np.ndarray,
) -> np.ndarray:
    model_path = (
        Path(config.base_models_dir)
        / config.ml_model_params.run_name
        / f"{config.ml_model_params.ml_model_type.value}_model.pkl"
    )

    try:
        model_path.resolve(strict=True)
    except ValueError as e:
        print(e)

    model = joblib.load(model_path)
    return model.predict(X)


@app.command()
def run():
    dataset_name = cfg_helper.data_params.dataset_name

    if not Path(f"data/processed/{dataset_name}").exists():
        print(":warning: [bold yellow]Dataset not found, generating...[/bold yellow]")
        loaded_dataset = generate_dataset(cfg_helper)
    else:
        print(":open_file_folder: [bold green]Loading dataset...[/bold green]")
        loaded_dataset = Dataset.load("data/processed", dataset_name)
    trained_model = train_model(cfg_helper, loaded_dataset)

    if cfg_helper.ml_model_params.validate_model:
        model_metrics = validate_model(
            trained_model, loaded_dataset, cfg_helper.ml_model_params.run_name
        )
        print(str(model_metrics))


if __name__ == "__main__":
    app()
