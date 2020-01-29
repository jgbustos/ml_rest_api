# coding: utf-8
"""Module that does all the ML trained model prediction heavy lifting."""
from logging import Logger, getLogger
from datetime import datetime, date
from os.path import normpath, join, dirname
from typing import Any, Iterable, Dict
import numpy as np
import pandas as pd
import joblib  # pylint: disable=unused-import

log: Logger = getLogger(__name__)


def full_path(filename: str) -> str:
    """Returns the full normalised path of a file in the same folder as this module."""
    return normpath(join(dirname(__file__), filename))


MODEL: Any = None


def init() -> None:
    """Loads the ML trained model (plus ancillary files) from file."""
    log.debug("Initialise model from file %s", full_path("model.pkl"))

    # deserialise the ML model (and possibly other objects such as feature_list,
    # feature_selector) from pickle file(s):
    #  global MODEL
    #  MODEL = joblib.load(full_path('model.pkl'))
    #  feature_list = joblib.load(full_path('feature_list.pkl'))
    #  feature_selector = joblib.load(full_path('feature_selector.pkl'))


def run(input_data: Iterable) -> Iterable:
    """Makes a prediction using the trained ML model."""
    log.info("input_data:%s", input_data)
    data: pd.DataFrame = (
        input_data
        if isinstance(input_data, pd.DataFrame)
        else pd.DataFrame(input_data, index=[0])
    )

    # make the necessary transformations using pickled objects, e.g.
    #  data = pd.get_dummies(data)
    #  data = data.reindex(columns=feature_list, fill_value=0)
    #  data = feature_selector.transform(data)

    # then make (or mock) a prediction
    #  prediction = MODEL.predict(data)

    prediction: Iterable = np.asarray(["mock_prediction"])
    if isinstance(prediction, np.ndarray):
        prediction = prediction.tolist()
    log.info("data:%s - prediction:%s", data.values[0], prediction)
    return prediction


def sample() -> Dict:
    """Returns a sample input vector as a dictionary."""
    return {
        "int_param": 10,
        "string_param": "foobar",
        "float_param": 0.1,
        "bool_param": True,
        "datetime_param": datetime.now().isoformat() + "Z",
        "date_param": date.today().isoformat(),
    }


if __name__ == "__main__":
    init()
    print(sample())
    print(run(sample()))
