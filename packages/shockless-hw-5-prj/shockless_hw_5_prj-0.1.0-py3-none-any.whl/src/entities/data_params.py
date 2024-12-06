from pydantic import BaseModel, PositiveInt, PositiveFloat


class DataParams(BaseModel):
    """
    Data parameters
    """
    train_data_path: str
    test_data_path: str
    n_samples: PositiveInt = 100
    n_features: PositiveInt = 10
    test_size: PositiveFloat = 0.3
