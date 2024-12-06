import yaml
from pydantic import BaseModel

from .train_params import TrainParams
from .data_params import DataParams


class PipelineParams(BaseModel):
    """
    Pipeline parameters
    """
    train_params: TrainParams
    data_params: DataParams
    random_state: int = 1
    predictor_model_type: str  # Will be used later to determine the model type via eval function


def read_pipeline_params(path: str) -> PipelineParams:
    """
    Function to read pipeline parameters
    :param path: str
    :return: PipelineParams
    """
    with open(path) as f:
        json_data = yaml.safe_load(f)
    return PipelineParams.model_validate(json_data)
