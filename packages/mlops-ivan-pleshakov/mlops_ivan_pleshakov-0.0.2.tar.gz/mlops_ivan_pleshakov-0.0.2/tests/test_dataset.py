"""Dataset creating test."""

import numpy as np
import pandas as pd
from loguru import logger

from mlops.dataset import create_train_test_dataset
from mlops.params.read_global_params import load_pipeline_params


def test_create_train_test_dataset(global_params_path: str):

    global_params = load_pipeline_params(global_params_path)
    create_train_test_dataset(global_params_path)

    train_dataset = pd.read_csv(global_params.data_params.train_data_path)
    x_train, y_train = train_dataset.drop(columns=["target"]), train_dataset["target"]
    test_dataset = pd.read_csv(global_params.data_params.test_data_path)
    x_test, y_test = test_dataset.drop(columns=["target"]), test_dataset["target"]
    logger.info(train_dataset.columns)
    logger.info(x_train.shape)
    assert len(x_train) + len(x_test) == global_params.data_params.n_samples
    assert len(y_train) + len(y_test) == global_params.data_params.n_samples
    assert round(len(x_test) / global_params.data_params.n_samples, 1) == global_params.data_params.test_size
    assert len(np.unique(y_train)) == global_params.data_params.n_classes
    assert x_train.shape[1] == global_params.data_params.n_features
