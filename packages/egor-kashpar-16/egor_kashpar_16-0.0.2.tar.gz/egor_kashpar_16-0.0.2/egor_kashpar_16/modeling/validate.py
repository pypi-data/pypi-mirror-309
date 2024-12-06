from pathlib import Path

import typer
from loguru import logger

import pandas as pd
import numpy as np

from egor_kashpar_16.entities.params import read_pipeline_params
from egor_kashpar_16.modeling.predict import predict
from egor_kashpar_16.config import metric_mapper

app = typer.Typer()


@app.command()
def validate(
    params_path: Path,
):
    logger.info("Validating model...")

    params = read_pipeline_params(params_path)

    predict(
        features_path=params.data_params.test_data_processed_path,
        model_path=params.train_params.classifier_path,
        predictions_path=params.validate_params.predictions_path,
    )

    validate_data = pd.read_csv(params.data_params.test_data_processed_path)

    predictions = np.load(params.validate_params.predictions_path)["predictions"]
    predictions_argmax = np.argmax(predictions, axis=-1)
    for metric in params.validate_params.metrics:
        if metric == "roc_auc_score":
            assert predictions.shape[-1] == 2, "roc_auc_score does not support multiclass yet"
            metric_value = metric_mapper[metric](
                validate_data['target'].to_numpy(),
                predictions[:, 1],
                average="macro" if params.validate_params.metrics_average == "binary" else params.validate_params.metrics_average
            )
        elif metric == "accuracy_score":
            metric_value = metric_mapper[metric](
                validate_data['target'].to_numpy(),
                predictions_argmax,
            )
        else:
            metric_value = metric_mapper[metric](
                validate_data['target'].to_numpy(),
                predictions_argmax,
                average=params.validate_params.metrics_average,
            )
        logger.info(f"{metric}: {metric_value}")

    logger.success("Validating complete")


if __name__ == "__main__":
    app()
