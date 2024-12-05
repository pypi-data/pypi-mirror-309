import typing as t
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

import yaml
from marshmallow import fields
from marshmallow_dataclass import class_schema
from marshmallow_enum import EnumField

project_root = Path("")


class ModelType(Enum):
    LOGISTIC_REGRESSION = "logistic_regression"
    RANDOM_FOREST = "random_forest"
    DECISION_TREE = "decision_tree"


@dataclass
class MakeDatasetParams:
    n_samples: int
    n_features: int
    n_classes: int
    n_informative: int
    n_redundant: int
    shuffle: bool
    test_data_size: float
    target_column_name: str
    full_data_path: str
    train_data_path: str
    test_data_path: str


@dataclass
class LogisticRegressionParams:
    multi_class: str
    solver: str
    max_iter: int


@dataclass
class RandomForestParams:
    n_estimators: int
    max_depth: t.Optional[int]


@dataclass
class DecisionTreeParams:
    criterion: str
    max_depth: t.Optional[int]


@dataclass
class TrainParams:
    model_type: ModelType
    logistic_regression: t.Optional[LogisticRegressionParams] = field(default=None)
    random_forest: t.Optional[RandomForestParams] = field(default=None)
    decision_tree: t.Optional[DecisionTreeParams] = field(default=None)


@dataclass
class Params:
    make_dataset: MakeDatasetParams
    train_params: TrainParams
    report_path: str
    models_path: str
    predictions_path: str
    random_state: int


BaseParamsSchema = class_schema(Params)


class TrainParamsSchema(class_schema(TrainParams)):
    model_type = EnumField(ModelType, by_value=True)


class ParamsSchema(BaseParamsSchema):
    train_params = fields.Nested(TrainParamsSchema)


def read_params_from_yaml(path: Path) -> Params:
    """
    Load yaml params with schema
    """
    full_path = project_root / path
    with open(full_path, "r") as input_stream:
        schema = ParamsSchema()
        return schema.load(yaml.safe_load(input_stream))
