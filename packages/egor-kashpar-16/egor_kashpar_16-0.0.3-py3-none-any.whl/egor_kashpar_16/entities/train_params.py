from pathlib import Path

from typing import Literal, Optional, Union
from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass
class TrainParamsLR:
    classifier_type: Literal["LogisticRegression"]
    penalty: Optional[Literal["l2", "l1", "elasticnet"]] = Field(default="l2")


@dataclass
class TrainParamsDTC:
    classifier_type: Literal["DecisionTreeClassifier"]
    max_depth: Optional[int] = Field(default=None, gt=0)


@dataclass
class TrainParamsGBC:
    classifier_type: Literal["GradientBoostingClassifier"]
    max_depth: Optional[int] = Field(default=3, gt=0)
    n_estimators: Optional[int] = Field(default=100, gt=0)
    learning_rate: Optional[float] = Field(default=0.1, gt=0)


@dataclass
class TrainParams:
    classifier_params: Union[TrainParamsLR, TrainParamsDTC, TrainParamsGBC]
    classifier_path: Path
    n_jobs: Optional[int] = Field(default=-1)
