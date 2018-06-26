import logging
from http import HTTPStatus
from flask_restplus import Api
from ml_rest_api.settings import settings

log = logging.getLogger(__name__)

api = Api(version='1.0', 
          title='Godel ML Predictor API',
          description='A simple demonstration of a Flask-RESTPlus powered service to make predictions using a ML model',
          default='health',
          default_label='Basic health check methods',)


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings['FLASK_DEBUG']:
        return {'message': message}, HTTPStatus.INTERNAL_SERVER_ERROR

