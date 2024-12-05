import os
from unittest.mock import patch
import pytest
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from mlops7sem_hw2.config import MODELS_DIR, PROCESSED_DATA_DIR
from mlops7sem_hw2.dataset import generate_train_dataset, make_train_test_split
from mlops7sem_hw2.modeling.train import (
    save_model,
    train_process,
    main,
)

from mlops7sem_hw2.modeling.predict import make_prediction


def test_generate_train_dataset():
    dataset = generate_train_dataset()
    assert isinstance(dataset, tuple)
    assert isinstance(dataset[0], pd.DataFrame)
    assert isinstance(dataset[1], pd.DataFrame)
    assert len(dataset[0]) == 1000
    assert len(dataset[1]) == 1000
    assert dataset[1].nunique()[0] == 2


def test_make_train_test_split():
    X_test, y_test = generate_train_dataset()
    split = make_train_test_split(X_test, y_test)
    assert isinstance(split, list)
    assert isinstance(split[0], pd.DataFrame)
    assert isinstance(split[1], pd.DataFrame)
    assert isinstance(split[2], pd.DataFrame)
    assert isinstance(split[3], pd.DataFrame)


def test_train_process():
    X_test, y_test = generate_train_dataset()
    assert (
        train_process("logistic_regression", X_test, y_test, {"C": 1.0, "penalty": "l2"})
        is not None
    )

    X, y = generate_train_dataset()

    model = train_process("logistic_regression", X, y, {})
    assert isinstance(model, LogisticRegression)

    model = train_process("decision_tree", X, y, {})
    assert isinstance(model, DecisionTreeClassifier)

    model = train_process("random_forest", X, y, {})
    assert isinstance(model, RandomForestClassifier)

    with pytest.raises(ValueError):
        train_process("invalid_model", X, y, {})


def test_save_model():
    X_test, y_test = generate_train_dataset()
    assert (
        save_model(
            "logistic_regression",
            X_test,
            y_test,
            MODELS_DIR / "model.pkl",
            {},
        )
        is None
    )


# def test_logistic_regression():
#     dataset = generate_train_dataset()
#     x_train, x_test, y_train, y_test = make_train_test_split(dataset[0], dataset[1])
#     model = train_process(
#         "logistic_regression",
#         x_train,
#         y_train,
#         model_parameters={"C": 1.0, "penalty": "l2"},
#     )
#     y_pred = model.predict(x_test)

#     assert round(accuracy_score(y_test, y_pred), 3) == 0.605
#     assert round(f1_score(y_test, y_pred, average="binary"), 3) == 0.588
#     assert round(precision_score(y_test, y_pred, average="binary"), 3) == 0.614
#     assert round(recall_score(y_test, y_pred, average="binary"), 3) == 0.605


# def test_decision_tree():
#     dataset = generate_train_dataset()
#     x_train, x_test, y_train, y_test = make_train_test_split(dataset[0], dataset[1])
#     model = train_process(
#         "decision_tree",
#         x_train,
#         y_train,
#         model_parameters={
#             "max_depth": None,
#             "min_samples_split": 2,
#             "min_samples_leaf": 1,
#             "random_state": 42,
#         },
#     )
#     y_pred = model.predict(x_test)

#     assert round(accuracy_score(y_test, y_pred), 3) == 0.855
#     assert round(f1_score(y_test, y_pred, average="binary"), 3) == 0.856
#     assert round(precision_score(y_test, y_pred, average="binary"), 3) == 0.861
#     assert round(recall_score(y_test, y_pred, average="binary"), 3) == 0.855


# def test_random_forest():
#     dataset = generate_train_dataset()
#     x_train, x_test, y_train, y_test = make_train_test_split(dataset[0], dataset[1])
#     model = train_process(
#         "random_forest",
#         x_train,
#         y_train,
#         model_parameters={
#             "n_estimators": 100,
#             "min_samples_split": 2,
#             "min_samples_leaf": 1,
#             "random_state": 42,
#         },
#     )
#     y_pred = model.predict(x_test)

#     assert round(accuracy_score(y_test, y_pred), 3) == 0.855
#     assert round(f1_score(y_test, y_pred, average="binary"), 3) == 0.855
#     assert round(precision_score(y_test, y_pred, average="binary"), 3) == 0.866
#     assert round(recall_score(y_test, y_pred, average="binary"), 3) == 0.855


def test_train_process_model():
    dataset = generate_train_dataset()
    assert isinstance(
        train_process("logistic_regression", dataset[0], dataset[1], {}),
        type(LogisticRegression()),
    )
    assert isinstance(
        train_process("random_forest", dataset[0], dataset[1], {}),
        type(RandomForestClassifier()),
    )
    assert isinstance(
        train_process("decision_tree", dataset[0], dataset[1], {}),
        type(DecisionTreeClassifier()),
    )
    with pytest.raises(ValueError, match="Incorrect model name"):
        train_process("invalid_model", dataset[0], dataset[1], {})


def test_save_model_files():
    dataset = generate_train_dataset()
    save_path = PROCESSED_DATA_DIR / "config_test_1.json"
    save_model(
        "logistic_regression",
        dataset[0],
        dataset[1],
        save_path,
        {"C": 1.0, "penalty": "l2"},
    )
    assert os.path.isfile(PROCESSED_DATA_DIR / "config_test_1.json")
    assert save_path.is_file()

    save_path = PROCESSED_DATA_DIR / "config_test_2.json"
    save_model(
        "decision_tree",
        dataset[0],
        dataset[1],
        PROCESSED_DATA_DIR / "config_test_2.json",
        {
            "max_depth": None,
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "random_state": 42,
        },
    )
    assert os.path.isfile(PROCESSED_DATA_DIR / "config_test_2.json")
    assert save_path.is_file()

    save_path = PROCESSED_DATA_DIR / "config_test_3.json"
    save_model(
        "random_forest",
        dataset[0],
        dataset[1],
        save_path,
        {
            "n_estimators": 100,
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "random_state": 42,
        },
    )
    assert os.path.isfile(PROCESSED_DATA_DIR / "config_test_3.json")
    assert save_path.is_file()


def test_make_prediction():
    dataset = generate_train_dataset()
    assert (
        make_prediction(
            2,
            dataset[1],
            dataset[1].to_numpy(),
            "mlops7sem_hw2/metrics.json",
        )
        is None
    )


def test_make_prediction_print():
    n_classes = 2
    y_test = pd.DataFrame([0, 1, 1, 0, 1])
    y_pred = np.array([0, 1, 0, 0, 1])
    expected_accuracy = round(accuracy_score(y_test, y_pred), 3)
    expected_f1 = round(f1_score(y_test, y_pred, average="binary"), 3)
    expected_precision = round(precision_score(y_test, y_pred, average="binary"), 3)
    expected_recall = round(recall_score(y_test, y_pred, average="binary"), 3)

    with patch("builtins.print") as mock_print:
        make_prediction(n_classes, y_test, y_pred, "mlops7sem_hw2/metrics.json")

        mock_print.assert_any_call(f"Accuracy score: {expected_accuracy}")
        mock_print.assert_any_call(f"F1-score: {expected_f1}")
        mock_print.assert_any_call(f"Presicion score: {expected_precision}")
        mock_print.assert_any_call(f"Recall score: {expected_recall}")


def test_main_invalid_model():
    with pytest.raises(ValueError, match="Invalid name of model"):
        main("invalid_model", "mlops7sem_hw2/params.yaml")


def test_open_yaml_file():
    with pytest.raises(ValueError, match="yaml file incorrect_yaml_file not exists"):
        main("invalid_model", "incorrect_yaml_file")


def test_open_yaml_file_1():
    with pytest.raises(ValueError, match="incorrect format of yaml file"):
        main("invalid_model", "mlops7sem_hw2/features.py")


if __name__ == "__main__":
    pytest.main()
