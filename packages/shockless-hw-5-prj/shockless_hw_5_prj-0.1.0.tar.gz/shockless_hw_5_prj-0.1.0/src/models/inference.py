import pickle

import pandas as pd


def inference_file(model_path: str, data_path: str, output_path: str):
    """
    Function to make predictions
    :param model_path: str
    :param data_path: str
    :param output_path: str
    :return: None
    """
    with open(model_path, "rb") as fin:
        model = pickle.load(fin)
    data = pd.read_csv(data_path)
    predictions = model.predict(data)
    predictions = pd.DataFrame(predictions, columns=["target"])
    predictions.to_csv(output_path, index=False)
    return None
