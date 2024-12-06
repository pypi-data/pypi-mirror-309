"""Train model."""

import json
import pickle

import pandas as pd
import typer
from loguru import logger
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

from mlops.config import GLOBAL_PARAMS_PATH, MODELS_PARAMS_PATH
from mlops.params.read_global_params import load_pipeline_params
from mlops.params.read_models_params import ModelsParams, load_models_params

app = typer.Typer()


def initialize_model(model_type: str, random_state: int, models_params: ModelsParams):
    """Initialize model with model type."""
    if model_type == "logistic_regression_params":
        logreg_params = models_params.logistic_regression_params
        model = LogisticRegression(
            random_state=random_state,
            penalty=logreg_params.penalty,
            max_iter=logreg_params.max_iter,
            C=logreg_params.C,
        )

    elif model_type == "random_forest_classifier_params":
        rfc_params = models_params.random_forest_classifier_params
        model = RandomForestClassifier(
            random_state=random_state,
            n_estimators=rfc_params.n_estimators,
            criterion=rfc_params.criterion,
            max_depth=rfc_params.max_depth,
            min_samples_leaf=rfc_params.min_samples_leaf,
        )

    elif model_type == "decision_tree_classifier_params":
        dtc_params = models_params.decision_tree_classifier_params
        model = DecisionTreeClassifier(
            random_state=random_state,
            criterion=dtc_params.criterion,
            max_depth=dtc_params.max_depth,
            min_samples_leaf=dtc_params.min_samples_leaf,
        )

    return model


@app.command()
def main():
    """Running"""
    models_params = load_models_params(MODELS_PARAMS_PATH)
    logger.info(models_params)

    global_params = load_pipeline_params(GLOBAL_PARAMS_PATH)
    logger.info(global_params)

    train_dataset = pd.read_csv(global_params.data_params.train_data_path)
    x_train, y_train = train_dataset.drop(columns=["target"]), train_dataset["target"]
    test_dataset = pd.read_csv(global_params.data_params.test_data_path)
    x_test, y_test = test_dataset.drop(columns=["target"]), test_dataset["target"]

    model = initialize_model(
        model_type=global_params.train_params.model_type,
        random_state=global_params.random_state,
        models_params=models_params,
    )

    model.fit(x_train, y_train)
    with open(global_params.train_params.model_path, "wb") as f:
        pickle.dump(model, f)

    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_true=y_test, y_pred=y_pred)
    metrics = {"Accuracy": accuracy}
    with open(global_params.train_params.metrics_path, "w") as fp:
        json.dump(metrics, fp)

    logger.info(f"Accuracy = {accuracy}")

    return accuracy


if __name__ == "__main__":
    app()
