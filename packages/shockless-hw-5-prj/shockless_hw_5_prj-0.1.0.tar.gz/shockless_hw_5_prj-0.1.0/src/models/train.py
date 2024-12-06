import os
from enum import Enum
import json
import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import roc_auc_score

import click
import pandas as pd
from dvclive import Live

from loguru import logger
from src.entities.params import read_pipeline_params


class ModelsEnum(Enum):
    """
    Enum with models
    """
    RANDOM_FOREST = RandomForestClassifier
    DECISION_TREE = DecisionTreeClassifier
    LINEAR_REGRESSION = LinearRegression


@click.command()
@click.argument("params_path", type=click.Path(exists=True))
def train(params_path: str = None):
    """
    Train and validate model
    :param params_path: str
    :return: None
    """
    params = read_pipeline_params(params_path)
    train_df = pd.read_csv(params.data_params.train_data_path)
    x_train = train_df.drop("target", axis=1)
    y_train = train_df["target"].values.reshape(-1, 1)

    test = pd.read_csv(params.data_params.test_data_path)
    x_test = test.drop("target", axis=1)
    y_test = test["target"].values.reshape(-1, 1)
    model = eval(params.predictor_model_type).value(**params.train_params.train_model_parameters)
    model.fit(x_train, y_train)
    logger.info(f"Learn model {model}")

    try:
        y_test_pred = model.predict_proba(x_test)[:, 1]
    except AttributeError:
        y_test_pred = model.predict(x_test)
    roc_auc = roc_auc_score(y_test, y_test_pred)
    logger.info(f"Got ROC-AUC {roc_auc:.3f}")

    metrics = {"roc-auc": roc_auc}

    os.makedirs(os.path.dirname(params.train_params.train_model_path), exist_ok=True)
    with open(params.train_params.train_model_path, "wb") as fin:
        pickle.dump(model, fin)
    logger.info(f"Saved model to path {params.train_params.train_model_path}")

    os.makedirs(os.path.dirname(params.train_params.metrics_path), exist_ok=True)
    with open(params.train_params.metrics_path, "w") as fin:
        json.dump(metrics, fin)
    logger.info(f"Saved metrics to path {params.train_params.metrics_path}")
    with Live(save_dvc_exp=True) as live:
        live.log_artifact(params.train_params.metrics_path)
        live.log_artifact(params.train_params.train_model_path)
        for key, value in metrics.items():
            live.log_metric(key, value)


if __name__ == "__main__":
    train()
