# coding: utf-8
"""Module that does all the ML trained model prediction heavy lifting."""
import logging
from datetime import datetime, date
from os.path import normpath, join, dirname
import numpy as np
import pandas as pd
#from sklearn.externals import joblib

log = logging.getLogger(__name__)

def full_path(filename):
    """Returns the full normalised path of a file in the same folder as this module."""
    return normpath(join(dirname(__file__), filename))

MODEL_FILE = full_path('model.pkl')

model = None

def ready():
    """Returns whether the ML trained model has been loaded from file correctly."""
    return model is not None # and xxx is not None...

def init():
    """Loads the ML trained model (plus ancillary files) from file."""
    global model
    if not ready():
        log.debug('Initialise model from file %s', MODEL_FILE)
        # deserialise the model from the pickled file
        model = False
        # model = joblib.load(MODEL_FILE)
        # deserialise other pickled objects e.g. feature_list, feature_selector

def run(data):
    """Makes a prediction using the trained ML model."""
    test = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data, index=[0])
    test = pd.get_dummies(test)

    # make the necessary transformations from other pickled objects, e.g.
    #     test = pd.get_dummies(test)
    #     test.reindex(columns=feature_list, fill_value=0)
    #     test = feature_selector.transform(test)

    # make (or mock) a prediction
    prediction = np.asarray(['test_prediction'])
    # prediction = model.predict(test)
    if isinstance(prediction, np.ndarray):
        prediction = prediction.tolist()
    log.info('Data:%s - Prediction:%s', data, prediction)
    return prediction

def sample():
    """Returns a sample input vector as a dictionary."""
    return {"int_param":10,
            "string_param":"foobar",
            "float_param":0.1,
            "bool_param":True,
            "datetime_param":datetime.now().isoformat(),
            "date_param":date.today().isoformat(),}

if __name__ == "__main__":
    init()
    print(sample())
    print(run(sample()))
