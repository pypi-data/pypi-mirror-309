from pathlib import Path

import typer
from loguru import logger

import dataclasses

import pandas as pd

import pickle

from egor_kashpar_16.config import model_mapper
from egor_kashpar_16.entities.params import read_pipeline_params

app = typer.Typer()


@app.command()
def train(
    params_path: Path,
):
    logger.info("Start training")
    params = read_pipeline_params(params_path)

    logger.info(f"Reading train data from {params.data_params.train_data_processed_path}...")
    train_data = pd.read_csv(params.data_params.train_data_processed_path)

    X_train = train_data.drop("target", axis=1)
    y_train = train_data["target"].to_numpy()

    model_kwargs = dataclasses.asdict(params.train_params.classifier_params)
    logger.info(f"Initialize model with params: {model_kwargs}")
    model = model_mapper[model_kwargs.pop("classifier_type")](random_state=params.random_state, **model_kwargs)

    logger.info("Train model...")
    model.fit(X_train, y_train)
    logger.info("Model has been trained")

    with open(params.train_params.classifier_path, "wb") as fp:
        pickle.dump(model, fp, protocol=5)
    logger.info(f"Save model to the path: {params.train_params.classifier_path}")

    logger.success("Modeling training complete")


if __name__ == "__main__":
    app()
