"""Module that creates the Api object and declares default error handler."""
import logging
from http import HTTPStatus
from flask_restplus import Api
from ml_rest_api.settings import get_value

log = logging.getLogger(__name__)

api = Api(version='0.1',
          title='Machine Learning REST API',
          description='A RESTful API to return predictions from a trained ML model, \
          built with Python 3 and Flask-RESTplus',
          default='health',
          default_label='Basic health check methods',)


@api.errorhandler
def default_error_handler(exception):
    """Default error handler that returns HTTP 500 error."""
    log.exception(exception.message)
    if get_value('FLASK_DEBUG'):
        return {'message': exception.message}, HTTPStatus.INTERNAL_SERVER_ERROR
    return {'message': 'An unhandled exception occurred.'}, HTTPStatus.INTERNAL_SERVER_ERROR
