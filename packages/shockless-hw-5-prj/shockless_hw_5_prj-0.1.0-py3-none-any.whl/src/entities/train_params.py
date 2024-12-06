from pydantic import BaseModel


class TrainParams(BaseModel):
    """
    Training parameters
    """
    train_model_path: str
    metrics_path: str
    train_model_parameters: dict
