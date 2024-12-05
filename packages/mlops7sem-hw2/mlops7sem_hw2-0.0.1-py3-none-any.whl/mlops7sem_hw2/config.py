import json
from enum import StrEnum
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
from loguru import logger
from pydantic import Field
from pydantic_settings import BaseSettings

# Load environment variables from .env file if it exists
load_dotenv()

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]
logger.info(f"PROJ_ROOT path is: {PROJ_ROOT}")

DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

MODELS_DIR = PROJ_ROOT / "models"

REPORTS_DIR = PROJ_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
CONFIG_PATH = PROCESSED_DATA_DIR / "config.json"

# If tqdm is installed, configure loguru with tqdm.write
# https://github.com/Delgan/loguru/issues/135
try:
    from tqdm import tqdm

    logger.remove(0)
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    pass


def load_config(config_path: Path | str = CONFIG_PATH):
    with open(config_path, "r", encoding="utf-8") as j:
        config = json.loads(j.read())
    return config


class Model(StrEnum):
    logistic_regression = "logistic_regression"
    decision_tree = "decision_tree"
    random_forest = "random_forest"


class Config(BaseSettings):

    model: str | None = None
    parameters: Dict | None = None

    # Dataset
    n_samples: int = Field(default=1000, gt=10)
    n_features: int = Field(default=3, ge=2)
    n_classes: int = Field(default=3, ge=2)
    n_redundant: int = Field(default=0, ge=0)
    n_informative: int = Field(default=3, gt=0)
    random_state: int = 42

    # Training
    test_size: float = Field(default=0.2, gt=0, lt=1)
    random_state: int = Field(default=42, ge=0)

    # Save model
    save_path: str | Path = MODELS_DIR / "model.pkl"


class Penalty(StrEnum):
    l1 = "l1"
    l2 = "l2"
    elasticnet = "elasticnet"


class LogisticRegressionConfig(Config):
    C: float = Field(default=1.0, gt=0.0)
    penalty: Penalty | None = Penalty.l2

    def get_model_parameters(self) -> Dict[str, Any]:
        return {"C": self.C, "penalty": self.penalty}


class DecisionTreeConfig(Config):
    max_depth: int | None = Field(default=None, gt=0)
    min_samples_split: int | float = Field(default=2, gt=0.0)
    min_samples_leaf: int | float = Field(default=1, ge=1)
    random_state: int = 42

    def get_model_parameters(self) -> Dict[str, Any]:
        return {
            "max_depth": self.max_depth,
            "min_samples_split": self.min_samples_split,
            "min_samples_leaf": self.min_samples_leaf,
            "random_state": self.random_state,
        }


class RandomForestClassifierConfig(Config):
    n_estimators: int = Field(default=100, ge=1)
    min_samples_split: int | float = Field(default=2, gt=0.0)
    min_samples_leaf: int | float = Field(default=1, ge=1)
    random_state: int = 42

    def get_model_parameters(self) -> Dict[str, Any]:
        return {
            "n_estimators": self.n_estimators,
            "min_samples_split": self.min_samples_split,
            "min_samples_leaf": self.min_samples_leaf,
            "random_state": self.random_state,
        }
