from dataclasses import dataclass
from pathlib import Path

import numpy as np
import typer
from rich import print
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

from mlops_misis.config import Config, cfg_helper

app = typer.Typer()


@dataclass
class Dataset:
    """Dataset class."""

    X_train: np.ndarray
    X_test: np.ndarray
    y_train: np.ndarray
    y_test: np.ndarray

    def save(self, path: Path, dataset_name: str) -> None:
        """Save the dataset to the specified path (path/dataset_name).

        Parameters
        ----------
        path : Path
            Path to save the dataset.
        dataset_name : str
            Name of the dataset.
        """
        save_path = path / dataset_name
        save_path.mkdir(parents=True, exist_ok=True)

        np.save(save_path / "X_train.npy", self.X_train)
        np.save(save_path / "X_test.npy", self.X_test)
        np.save(save_path / "y_train.npy", self.y_train)
        np.save(save_path / "y_test.npy", self.y_test)

    @staticmethod
    def load(path: Path | str, dataset_name: str) -> "Dataset":
        """Load the dataset from the specified path (path/dataset_name).

        Parameters
        ----------
        path : Path | str
            Path to load the dataset.
        dataset_name : str
            Name of the dataset.

        Returns
        -------
        Dataset
            Loaded dataset object.
        """
        if isinstance(path, str):
            path = Path(path)
        load_path = path / dataset_name

        X_train = np.load(load_path / "X_train.npy")
        X_test = np.load(load_path / "X_test.npy")
        y_train = np.load(load_path / "y_train.npy")
        y_test = np.load(load_path / "y_test.npy")

        return Dataset(X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test)


def generate_dataset(config: Config) -> Dataset:
    """Generate a synthetic dataset.

    Parameters
    ----------
    config : Config
        Configuration object.

    Returns
    -------
    Dataset
        Generated dataset.
    """
    print(":gear: [bold green]Generating dataset...[/bold green]")
    n_features = config.data_params.n_features
    train_size = config.data_params.train_size
    n_samples = config.data_params.n_samples

    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=n_features - 1,
        n_redundant=1,
        random_state=42,
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=train_size, random_state=42
    )

    dataset = Dataset(X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test)
    save_path = Path(cfg_helper.base_data_dir)
    save_path.mkdir(parents=True, exist_ok=True)
    dataset.save(save_path, config.data_params.dataset_name)

    print(
        f":floppy_disk: [bold blue]Dataset saved to {save_path / config.data_params.dataset_name}[/bold blue]"
    )

    return dataset


@app.command()
def run():
    generate_dataset(cfg_helper)


if __name__ == "__main__":
    app()
