# coding: utf-8

import logging
import numpy as np
import pandas as pd
from datetime import datetime, date
from os.path import normpath, join, dirname
from sklearn.externals import joblib

log = logging.getLogger(__name__)

def full_path(filename):    
    return normpath(join(dirname(__file__), filename))

MODEL_FILE = full_path('model.pkl')

model = None

def ready():
    return (model is not None) # and (xxx is not None)...

def init():    
    global model
    if not ready():
        log.debug('Initialise model from file {}'.format(MODEL_FILE))
        # deserialise the model from the pickled file
        model = False 
        # model = joblib.load(MODEL_FILE)
        # deserialise other pickled objects e.g. feature_list, feature_selector

def run(data):
    test = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data, index=[0])

    # make the necessary transformations from other pickled objects, e.g.
    #     test = pd.get_dummies(test)
    #     test.reindex(columns=feature_list, fill_value=0)
    #     test = feature_selector.transform(test)

    # make (or mock) a prediction
    prediction = ['test_prediction']
    # prediction = model.predict(test)
    if isinstance(prediction, np.ndarray):
        prediction = prediction.tolist()
    log.info('Data:{} - Prediction:{}'.format(data, prediction))
    
    return prediction

def sample():
    return {"int_param":10,
            "string_param":"foobar",
            "float_param":0.1,
            "bool_param":True,
            "datetime_param":datetime.now().isoformat(),
            "date_param":date.today().isoformat(),}

if __name__ == "__main__":
    init()
    test = sample()
    prediction = run(test)
    print(test)
    print(prediction)
