from dataclasses import dataclass

import yaml
from marshmallow_dataclass import class_schema

from .data_params import DataParams
from .train_params import TrainParams


@dataclass()
class PipelineParams:
    train_params: TrainParams
    data_params: DataParams
    random_state: int


PipelineParamsSchema = class_schema(PipelineParams)


def read_pipeline_params(path: str) -> PipelineParams:
    with open(path, "r", encoding="utf-8") as input_stream:
        schema = PipelineParamsSchema()
        return schema.load(yaml.safe_load(input_stream))

