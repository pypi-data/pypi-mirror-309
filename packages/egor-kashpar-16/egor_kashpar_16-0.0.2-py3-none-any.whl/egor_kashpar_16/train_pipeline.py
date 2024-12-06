from pathlib import Path

import typer
from loguru import logger

from egor_kashpar_16.dataset import generate_data
from egor_kashpar_16.features import scale_data
from egor_kashpar_16.modeling.train import train
from egor_kashpar_16.modeling.validate import validate

app = typer.Typer()


@app.command()
def main(params_path: Path):
    logger.info("Starting train pipeline...")

    generate_data(
        params_path=params_path,
    )

    scale_data(
        params_path=params_path,
    )

    train(
        params_path=params_path,
    )

    validate(
        params_path=params_path,
    )

    logger.success("Train pipeline complete")


if __name__ == "__main__":
    app()
