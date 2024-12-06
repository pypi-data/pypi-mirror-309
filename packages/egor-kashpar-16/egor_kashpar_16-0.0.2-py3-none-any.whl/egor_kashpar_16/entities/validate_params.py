from pathlib import Path

from typing import List, Literal
from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass
class ValidateParams:
    predictions_path: Path
    metrics: List[str] = Field(default=["roc_auc_score"])
    metrics_average: Literal["micro", "macro", "binary"] = Field(default=["binary"])
