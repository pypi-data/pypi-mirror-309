import os
from pathlib import Path

import typer
from loguru import logger

import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

from egor_kashpar_16.entities.params import read_pipeline_params

app = typer.Typer()


@app.command()
def generate_data(
    params_path: Path,
):
    logger.info("Creating dataset...")

    params = read_pipeline_params(params_path)
    data_params = params.data_params

    X, y = make_classification(
        n_samples=data_params.n_samples,
        n_features=data_params.n_features,
        n_classes=data_params.n_classes,
        n_informative=data_params.n_informative,
        random_state=params.random_state,
    )

    data = pd.DataFrame(np.hstack([X, y.reshape(-1, 1)]))
    data.columns = [f"feature_{i}" for i in range(data.shape[-1])]
    data = data.rename({f"feature_{data.shape[-1] - 1}": "target"}, axis=1)
    logger.info(f"Got data with shape: {data.shape}")

    train_data, test_data = train_test_split(
        data,
        test_size=data_params.test_size,
        random_state=params.random_state,
    )
    logger.info(f"Split data into train ({train_data.shape}) and test ({test_data.shape})")

    if not os.path.exists(os.path.dirname(data_params.train_data_path)):
        os.makedirs(os.path.dirname(data_params.train_data_path))
    train_data.to_csv(data_params.train_data_path, index=False)
    logger.info(f"Save train sample to the path: {data_params.train_data_path}")

    if not os.path.exists(os.path.dirname(data_params.test_data_path)):
        os.makedirs(os.path.dirname(data_params.test_data_path))
    test_data.to_csv(data_params.test_data_path, index=False)
    logger.info(f"Save test sample to the path: {data_params.test_data_path}")
    logger.success("Dataset created")


if __name__ == "__main__":
    app()
