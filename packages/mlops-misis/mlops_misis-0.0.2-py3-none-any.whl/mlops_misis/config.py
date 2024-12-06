from enum import Enum
from typing import Any, Optional

import yaml
from pydantic import BaseModel, Field, model_validator


class ModelType(Enum):
    """Enum class for model types."""

    LOG_REG: str = "LogisticRegression"
    DECISION_TREE: str = "DecisionTreeClassifier"
    RANDOM_FOREST: str = "RandomForestClassifier"


class ModelConfig(BaseModel):
    """Model configuration class."""

    ml_model_type: ModelType

    validate_model: Optional[bool] = Field(
        default=True,
        description="Whether to validate the model after training",
    )

    run_name: Optional[str] = Field(
        default="run",
        description="Name of the training run",
    )

    max_depth: Optional[int] = Field(
        None,
        description="Maximum Depths of the tree/trees.",
        ge=1,
        le=10,
    )

    n_estimators: Optional[int] = Field(
        None,
        description="The number of trees in the forest",
        ge=5,
        le=1000,
    )

    random_state: Optional[int] = Field(
        default=42, description="Random state for reproducibility", ge=0
    )
    C: Optional[float] = Field(None, description="Responsible for regularization strength", gt=0.0)


class DataConfig(BaseModel):
    """Data configuration class."""

    dataset_name: str = Field(description="Name of the dataset")

    n_features: int = Field(
        description="Number of features in the synthetic dataset",
        ge=1,
        default=10,
    )

    n_samples: int = Field(
        description="Number of samples in the synthetic dataset",
        ge=1,
        default=1000,
    )

    train_size: float = Field(
        description="Train size for the synthetic dataset",
        gt=0.0,
        lt=1.0,
        default=0.8,
    )


class Config(BaseModel):
    """Main configuration class."""

    ml_model_params: ModelConfig
    data_params: DataConfig
    base_data_dir: str = Field(default="data/processed", description="Path to store datasets")
    base_models_dir: str = Field(default="models", description="Path to store models")
    base_reports_dir: str = Field(default="reports", description="Path to store")

    @classmethod
    def load_yaml(cls, file_path: str) -> "Config":
        """Load configuration from a YAML file.

        Parameters
        ----------
        file_path : str
            Path to the YAML file.

        Returns
        -------
        Config
            Configuration object.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            yaml_data = yaml.safe_load(file)

        return cls(**yaml_data)

    @model_validator(mode="before")
    @classmethod
    def check_cfg_before(cls, values: dict) -> Any:
        """Check configuration before loading.

        Parameters
        ----------
        values : dict
            Configuration values.

        Returns
        -------
        Any

        Raises
        ------
        ValueError
            If the configuration is invalid.
        """
        ml_model_params = values.get("ml_model_params")

        ml_model_type = ml_model_params.get("ml_model_type")
        max_depth = ml_model_params.get("max_depth")
        n_estimators = ml_model_params.get("n_estimators")
        C = ml_model_params.get("C")

        if ml_model_type == ModelType.LOG_REG and C is None:
            raise ValueError("C must be provided for logistic regression model.")
        if ml_model_type == ModelType.DECISION_TREE and max_depth is None:
            raise ValueError("max_depth must be provided for decision tree model.")
        if ml_model_type == ModelType.RANDOM_FOREST:
            if max_depth is None:
                raise ValueError("max_depth must be provided for random forest model.")
            if n_estimators is None:
                raise ValueError("n_estimators must be provided for random forest model.")

        return values


cfg_helper = Config.load_yaml("params.yaml")
