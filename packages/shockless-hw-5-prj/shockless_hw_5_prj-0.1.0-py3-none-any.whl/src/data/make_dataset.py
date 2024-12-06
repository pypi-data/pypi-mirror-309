# -*- coding: utf-8 -*-
import click
import sklearn.datasets
import sklearn.model_selection
import sklearn
import pandas as pd
import numpy as np
from loguru import logger
from src.entities.params import read_pipeline_params


@click.command()
@click.argument('params_path', type=click.Path(exists=True), )
def make_dataset(params_path: str):
    """
    Function to generate dataset
    """
    params = read_pipeline_params(params_path)
    x, y = sklearn.datasets.make_classification(
        n_samples=params.data_params.n_samples, n_features=params.data_params.n_features,
        random_state=params.random_state
    )
    data = pd.DataFrame(np.hstack([x, y.reshape(-1, 1)]))
    data.columns = [f"feat_{i}" for i in range(data.shape[-1])]
    data = data.rename({f"feat_{data.shape[-1] - 1}": "target"}, axis=1)
    logger.info(f"Got data with shape: {data.shape}")

    assert data.shape[0] > 0, 'number of samples should be more than 0'
    assert data.shape[1] > 0, 'number of features should be more than 0'

    assert params.data_params.test_size > 0.0, 'test set should not be empty'

    train, test = sklearn.model_selection.train_test_split(
        data, test_size=params.data_params.test_size, random_state=params.random_state
    )
    logger.info(f"Split data into train ({train.shape}) and test ({test.shape})")

    train.to_csv(params.data_params.train_data_path, index=False)
    logger.info(f"Save train sample to the path: {params.data_params.train_data_path}")

    test.to_csv(params.data_params.test_data_path, index=False)
    logger.info(f"Save test sample to the path: {params.data_params.test_data_path}")


if __name__ == "__main__":
    make_dataset(None)
