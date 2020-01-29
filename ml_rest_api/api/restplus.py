"""Module that creates the Api object and declares default error handler."""
from logging import Logger, getLogger
from http import HTTPStatus
from typing import Tuple, Iterable
from jsonschema import FormatChecker
from flask_restplus import Api
from ml_rest_api.settings import get_value

FlaskApiReturnType = Tuple[Iterable, HTTPStatus]

log: Logger = getLogger(__name__)

api = Api(  # pylint: disable=invalid-name
    version="0.1",
    title="Machine Learning REST API",
    description="A RESTful API to return predictions from a trained ML model, \
          built with Python 3 and Flask-RESTplus",
    format_checker=FormatChecker(formats=("date-time", "date",)),
    default="health",
    default_label="Basic health check methods",
)


@api.errorhandler
def default_error_handler(exception) -> FlaskApiReturnType:
    """Default error handler that returns HTTP 500 error."""
    log.exception(exception.message)
    if get_value("FLASK_DEBUG"):
        return {"message": exception.message}, HTTPStatus.INTERNAL_SERVER_ERROR
    return (
        {"message": "An unhandled exception occurred."},
        HTTPStatus.INTERNAL_SERVER_ERROR,
    )
