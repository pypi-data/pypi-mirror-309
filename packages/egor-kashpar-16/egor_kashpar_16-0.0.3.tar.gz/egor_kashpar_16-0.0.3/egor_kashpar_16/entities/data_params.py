from pathlib import Path

from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass
class DataParams:
    train_data_path: Path
    test_data_path: Path
    train_data_processed_path: Path
    test_data_processed_path: Path
    n_samples: int = Field(default=100, gt=0)
    n_features: int = Field(default=20, gt=0)
    n_classes: int = Field(default=2, gt=1)
    n_informative: int = Field(default=2, gt=1)
    test_size: float = Field(default=0.2, gt=0, lt=1)
