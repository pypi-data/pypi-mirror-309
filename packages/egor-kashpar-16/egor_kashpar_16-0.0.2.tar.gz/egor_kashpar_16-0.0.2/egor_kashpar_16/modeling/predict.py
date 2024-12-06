from pathlib import Path

import typer
from loguru import logger

import pickle
import pandas as pd
import numpy as np

app = typer.Typer()


@app.command()
def predict(
    features_path: Path,
    model_path: Path,
    predictions_path: Path,
):
    logger.info("Performing inference for model...")

    logger.info(f"Reading features from {features_path}...")
    inference_data = pd.read_csv(features_path)

    logger.info(f"Loading model from {model_path}...")
    with open(model_path, "rb") as fp:
        model = pickle.load(fp)

    logger.info(f"Saving predictions to {predictions_path}")
    predictions = model.predict_proba(inference_data[model.feature_names_in_])
    np.savez(predictions_path, predictions=predictions)

    logger.success("Inference complete")


if __name__ == "__main__":
    app()
