import os
import yaml

from pydantic import Field
from pydantic.dataclasses import dataclass

from .train_params import TrainParams
from .data_params import DataParams
from .validate_params import ValidateParams


@dataclass
class PipelineParams:
    train_params: TrainParams
    data_params: DataParams
    validate_params: ValidateParams
    random_state: int = Field(default=42)


def read_pipeline_params(path: str | os.PathLike) -> PipelineParams:
    with open(path, "r") as input_stream:
        return PipelineParams(**yaml.safe_load(input_stream))
