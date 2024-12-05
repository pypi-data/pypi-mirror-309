import json
import warnings

import joblib
import numpy as np
import pandas as pd
import typer
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from typing_extensions import Annotated

from mlops7sem_hw2.config import load_config
from mlops7sem_hw2.modeling.train import open_yaml_file

warnings.filterwarnings("ignore")

app = typer.Typer()


def make_prediction(
    n_classes: int,
    y_test: pd.DataFrame,
    y_pred: np.array,
    metrics_path: str,
) -> None:

    if n_classes > 2:
        average = "weighted"
    else:
        average = "binary"

    accuracy = round(accuracy_score(y_test, y_pred), 3)
    presicion = round(precision_score(y_test, y_pred, average=average), 3)
    recall = round(recall_score(y_test, y_pred, average=average), 3)
    f1 = round(f1_score(y_test, y_pred, average=average), 3)

    print(f"Accuracy score: {accuracy}")
    print(f"F1-score: {f1}")
    print(f"Presicion score: {presicion}")
    print(f"Recall score: {recall}")

    with open(metrics_path, "w", encoding="utf-8") as j:
        json.dump(
            {"Accuracy": accuracy, "F1-score": f1, "Presicion": presicion, "Recall": recall}, j
        )


@app.command()
def main(params_yaml_path: Annotated[str, typer.Argument()]):

    config = open_yaml_file(params_yaml_path)
    config = load_config(config["data_path"] + config["config_path"])

    model = joblib.load(config["save_path"])
    X_test, y_test = pd.read_csv(config["x_test"]), pd.read_csv(
        config["y_test"]
    )

    print(config["model"].upper())

    make_prediction(
        config["n_classes"],
        y_test,
        model.predict(X_test),
        config["catalog_name"] + config["metrics_path"],
    )


if __name__ == "__main__":
    app()
