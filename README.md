# ml_rest_api
A RESTful API to return predictions from a trained ML model, built with Python 3 and Flask-RESTplus

## First run instructions

First, open a command line interface and clone the GitHub repo in your workspace
```
> cd $WORKSPACE_PATH$
> git clone https://github.com/jgbustos/ml_rest_api
> cd ml_rest_api
```
Create and activate a Python virtual environment, then install the required Python packages using pip
```
> virtualenv venv
> venv\scripts\activate.bat
(venv) > pip install -r requirements.txt
```
Once dependencies are installed installed, set up the project for development
```
(venv) > python setup.py develop
```
Finally, run the project:
```
(venv) > python ml_rest_api\app.py
```
Open the URL http://localhost:8888/api/ with your browser and see the sample Swagger documentation

## Setting up the model

TODO

## Acknowledgements
This projects borrows heavily from the work done by Michał Karzyński:
  * https://github.com/postrational/rest_api_demo
  * http://michal.karzynski.pl/blog/2016/06/19/building-beautiful-restful-apis-using-flask-swagger-ui-flask-restplus/
 
