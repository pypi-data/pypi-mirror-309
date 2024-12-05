import json
import warnings
import os
from pathlib import Path
from typing import Any, Dict

import joblib
import pandas as pd
import typer
import yaml
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from typing_extensions import Annotated

from mlops7sem_hw2.config import Model

warnings.filterwarnings("ignore")

app = typer.Typer()


def train_process(
    model_name: str,
    X_train: pd.DataFrame,
    y_train: pd.DataFrame,
    model_parameters: Dict[str, Any],
) -> Any:

    model = None
    if model_name == "logistic_regression":
        model = LogisticRegression(**model_parameters)
    if model_name == "decision_tree":
        model = DecisionTreeClassifier(**model_parameters)
    if model_name == "random_forest":
        model = RandomForestClassifier(**model_parameters)

    if model is None:
        raise ValueError("Incorrect model name")

    model.fit(X_train, y_train)
    return model


def save_model(
    model_name: str,
    X_train: pd.DataFrame,
    y_train: pd.DataFrame,
    save_path: str,
    model_parameters: Dict[str, Any],
) -> None:

    trained_model = train_process(
        model_name,
        X_train,
        y_train,
        model_parameters,
    )
    joblib.dump(trained_model, save_path)


def open_yaml_file(path: str | Path):
    yaml_file = None
    if not os.path.exists(path):
        raise ValueError(f"yaml file {str(path)} not exists")
    if not path.endswith(".yaml"):
        raise ValueError("incorrect format of yaml file")
    with open(path, "r", encoding="utf-8") as file:
        yaml_file = yaml.safe_load(file)
    return yaml_file


@app.command()
def main(
    model_name: Annotated[str, typer.Argument()],
    params_yaml_path: Annotated[str, typer.Argument()],
):

    config = None
    config = open_yaml_file(params_yaml_path)

    config_model = None
    if model_name == Model.logistic_regression.name:
        config_model = open_yaml_file(config["catalog_name"] + config["logreg_path"])
    if model_name == Model.random_forest.name:
        config_model = open_yaml_file(config["catalog_name"] + config["randomforest_path"])
    if model_name == Model.decision_tree.name:
        config_model = open_yaml_file(config["catalog_name"] + config["decisiontree_path"])
    if not config_model:
        # raise ValueError("params model yaml not exists")
        raise ValueError("Invalid name of model")

    config["model_parameters"] = config_model
    config["model"] = model_name
    config["save_path"] = str(config["save_path"])
    config["config_path"] = str(config["data_path"] + config["config_path"])
    with open(config["config_path"], "w", encoding="utf-8") as f:
        json.dump(config, f)

    X_train, y_train = pd.read_csv(config["x_train"]), pd.read_csv(config["y_train"])

    save_model(
        model_name,
        X_train,
        y_train,
        config["save_path"],
        config["model_parameters"],
    )


if __name__ == "__main__":
    app()
