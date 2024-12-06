import os
from pathlib import Path

import typer
from loguru import logger

import pandas as pd
from sklearn.preprocessing import StandardScaler

from egor_kashpar_16.entities.params import read_pipeline_params

app = typer.Typer()


@app.command()
def scale_data(
    params_path: Path,
):
    logger.info("Scaling features from dataset...")

    params = read_pipeline_params(params_path)

    logger.info(f"Reading train data from {params.data_params.train_data_path}...")
    train_data = pd.read_csv(params.data_params.train_data_path)
    logger.info(f"Reading train data from {params.data_params.test_data_path}...")
    test_data = pd.read_csv(params.data_params.test_data_path)

    scaler = StandardScaler()
    scaler.fit(train_data.drop(columns=["target"]))

    train_data[train_data.columns.drop("target")] = scaler.transform(train_data.drop(columns=["target"]))
    test_data[test_data.columns.drop("target")] = scaler.transform(test_data.drop(columns=["target"]))

    if not os.path.exists(os.path.dirname(params.data_params.train_data_processed_path)):
        os.makedirs(os.path.dirname(params.data_params.train_data_processed_path))
    train_data.to_csv(params.data_params.train_data_processed_path, index=False)
    logger.info(f"Save train data to the path: {params.data_params.train_data_path}")

    if not os.path.exists(os.path.dirname(params.data_params.test_data_processed_path)):
        os.makedirs(os.path.dirname(params.data_params.test_data_processed_path))
    test_data.to_csv(params.data_params.test_data_processed_path, index=False)
    logger.info(f"Save test data to the path: {params.data_params.test_data_path}")

    logger.success("Features scale complete")


if __name__ == "__main__":
    app()
