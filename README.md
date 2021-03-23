# ml_rest_api

[![CircleCI](https://img.shields.io/circleci/build/github/jgbustos/ml_rest_api/master?logo=CircleCI&label=CircleCI%20build)](https://circleci.com/gh/jgbustos/ml_rest_api)
[![Docker Cloud Automated build](https://img.shields.io/docker/cloud/automated/jgbustos/ml-rest-api?logo=Docker&logoColor=white)](https://hub.docker.com/r/jgbustos/ml-rest-api/builds)
[![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/jgbustos/ml-rest-api?logo=Docker&logoColor=white)](https://hub.docker.com/r/jgbustos/ml-rest-api/builds)

A RESTful API to return predictions from a trained ML model, built with Python 3 and Flask-RESTX

## Development set-up instructions

First, open a command line interface and clone the GitHub repo in your workspace

```Powershell
PS > cd $WORKSPACE_PATH$
PS > git clone https://github.com/jgbustos/ml_rest_api
PS > cd ml_rest_api
```

Create and activate a Python virtual environment, then install the required Python packages using pip

```Powershell
PS > virtualenv venv
PS > venv\scripts\activate.ps1
(venv) PS > pip install -r requirements.txt
```

Once dependencies are installed, set up the project for development

```Powershell
(venv) PS > python setup.py develop
```

Finally, run the project:

```Powershell
(venv) PS > python ml_rest_api\app.py
```

Open the URL <http://localhost:8888/api/> with your browser and see the sample Swagger documentation

## Interfaces exposed

Swagger JSON available from URL <http://localhost:8888/api/swagger.json>

### Health

These two methods are meant to be used as the liveness and readiness probes in a Kubernetes deployment:

* GET <http://localhost:8888/api/liveness> returns 200/"Alive" if the service is up and running
* GET <http://localhost:8888/api/readiness> returns 200/"Ready" or 500/"Not Ready" depending on whether the ML model has been correctly initialised or not

### Model

* POST <http://localhost:8888/api/model/predict> will return a prediction using the ML model. The data_point structure shows the JSON argument that must be supplied, and example values for each of the fields. The service will validate that all the mandatory values are passed. Return values are:
  * 500/"Not Ready" if model is not correctly initialised
  * 400/Validation error if any mandatory parameter is missing or if any wrong data type (e.g. str, int, bool, datetime...) is supplied
  * 200/Predicted value based on JSON input

## Config settings

Configuration parameters are contained in the file **ml_rest_api/settings.py**, but they can also be overriden by setting env vars:

```python
settings = {
    # Flask settings
    'FLASK_SERVER_NAME': 'localhost:8888',
    'FLASK_HOST': '0.0.0.0',
    'FLASK_PORT': 8888,
    'FLASK_DEBUG': True,

    # Flask-RESTX settings
    'SWAGGER_UI_DOC_EXPANSION': 'list',
    'RESTX_VALIDATE': True,
    'RESTX_MASK_SWAGGER': False,
    'ERROR_404_HELP': False,
    'SWAGGER_UI_JSONEDITOR': True,

    # Trained ML/AI model settings
    'TRAINED_MODEL_MODULE_NAME': 'ml_trained_model',
}
```

| Parameter | Values | Details |
| --- | --- | --- |
| FLASK_SERVER_NAME | e.g.: localhost:8888 | Flask server name |
| FLASK_HOST | e.g.: 0.0.0.0 | Leave as 0.0.0.0 to avoid virtual host filtering |
| FLASK_PORT | e.g.: 8888 | Choose whatever suits you, go crazy |
| FLASK_DEBUG | False/True | Do not use debug mode in production |
| SWAGGER_UI_DOC_EXPANSION | 'none', 'list' or 'full' | Explained here: <https://flask-restx.readthedocs.io/en/stable/swagger.html#customization> |
| RESTX_VALIDATE | False/True | Explained here: <https://flask-restx.readthedocs.io/en/stable/swagger.html#the-api-expect-decorator> |
| RESTX_MASK_SWAGGER | False/True | Explained here: <https://flask-restx.readthedocs.io/en/stable/mask.html#usage> |
| ERROR_404_HELP | False/True | Explained here: <https://flask-restx.readthedocs.io/en/stable/quickstart.html#endpoints> |
| SWAGGER_UI_JSONEDITOR | False/True | Enable a JSON editor in the Swagger interface |
| TRAINED_MODEL_MODULE_NAME | e.g.: ml_trained_model | Name of the Python module that initialises the ML model and returns predictions (see [section below](#setting-up-the-model)) |

## Setting up the model

The trained ML model is meant to be initialised and invoked to make predictions in the context of a Python unit saved inside the directory **ml_rest_api/ml_trained_model**. The structure of this Python module is explained in [this document](ml_rest_api/ml_trained_model/module_structure.md)

## Build automation

This project is built into a Docker image using the Docker Hub automated build at <https://hub.docker.com/r/jgbustos/ml-rest-api/>

## Running the Docker container

```Powershell
> docker run -d -p8888:8888 jgbustos/ml-rest-api:latest
```

Open the URL <http://localhost:8888/api/> with your browser and see the sample Swagger documentation

## Acknowledgements

This projects borrows heavily from the work done by [Michał Karzyński](https://twitter.com/postrational):

* <https://github.com/postrational/rest_api_demo>
* <http://michal.karzynski.pl/blog/2016/06/19/building-beautiful-restful-apis-using-flask-swagger-ui-flask-restplus/>
