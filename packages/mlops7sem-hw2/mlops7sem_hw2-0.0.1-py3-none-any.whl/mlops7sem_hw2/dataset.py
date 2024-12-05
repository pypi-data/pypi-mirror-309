from typing import List, Tuple

import pandas as pd
import typer
import yaml
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from typing_extensions import Annotated

app = typer.Typer()


def generate_train_dataset(
    n_samples: int = 1000,
    n_features: int = 2,
    n_classes: int = 2,
    n_redundant: int = 0,
    n_informative: int = 2,
    random_state: int = 42,
) -> Tuple[
    pd.DataFrame,
    pd.DataFrame,
]:

    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_classes=n_classes,
        n_redundant=n_redundant,
        n_informative=n_informative,
        random_state=random_state,
    )
    X, y = map(pd.DataFrame, [X, y])
    return X, y


def make_train_test_split(
    X: pd.DataFrame,
    y: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42,
) -> List[pd.DataFrame]:

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
    )
    return [X_train, X_test, y_train, y_test]


@app.command()
def main(params_yaml_path: Annotated[str, typer.Argument()]):

    config = None
    with open(params_yaml_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    if config is None:
        raise ValueError("yaml not exists")

    if config["n_redundant"] >= config["n_features"]:
        raise ValueError(
            "Number of informative, redundant and repeated features must sum to less than the number of total features"
        )
    if config["n_informative"] > config["n_features"]:
        raise ValueError(
            "Number of informative, redundant and repeated features must sum to less than the number of total features"
        )

    X, y = generate_train_dataset(
        config["n_samples"],
        config["n_features"],
        config["n_classes"],
        config["n_redundant"],
        config["n_informative"],
        config["random_state"],
    )

    X_train, X_test, y_train, y_test = make_train_test_split(
        X,
        y,
        config["test_size"],
        config["random_state"],
    )

    X_test, y_test = map(pd.DataFrame, [X_test, y_test])

    X_test.to_csv(config["x_test"], index=False)
    y_test.to_csv(config["y_test"], index=False)
    X_train.to_csv(config["x_train"], index=False)
    y_train.to_csv(config["y_train"], index=False)


if __name__ == "__main__":
    app()
