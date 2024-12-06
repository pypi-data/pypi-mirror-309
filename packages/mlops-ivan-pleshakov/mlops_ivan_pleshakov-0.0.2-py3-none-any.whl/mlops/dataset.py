"""Create dataset."""

import pandas as pd
import typer
from loguru import logger
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

from mlops.config import GLOBAL_PARAMS_PATH
from mlops.params.read_global_params import load_pipeline_params

app = typer.Typer()

app.command()


@app.command()
def create_train_test_dataset(global_params_path: str = GLOBAL_PARAMS_PATH) -> None:
    """Train test split."""

    global_params = load_pipeline_params(global_params_path)
    logger.info(global_params)

    x_data, y_data = make_classification(
        random_state=global_params.random_state,
        n_samples=global_params.data_params.n_samples,
        n_features=global_params.data_params.n_features,
        n_classes=global_params.data_params.n_classes,
    )

    x_train, x_test, y_train, y_test = train_test_split(
        x_data,
        y_data,
        test_size=global_params.data_params.test_size,
        random_state=global_params.random_state,
    )
    train_dataset = pd.DataFrame(x_train)
    train_dataset["target"] = y_train
    test_dataset = pd.DataFrame(x_test)
    test_dataset["target"] = y_test

    train_dataset.to_csv(global_params.data_params.train_data_path, index=False)
    test_dataset.to_csv(global_params.data_params.test_data_path, index=False)

    logger.info(f"Train data successfully saved {global_params.data_params.train_data_path}")
    logger.info(f"Test data successfully saved {global_params.data_params.test_data_path}")

    return None


if __name__ == "__main__":
    create_train_test_dataset()
