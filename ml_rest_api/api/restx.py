"""Module that creates the Api object and declares default error handler."""
from logging import Logger, getLogger
from typing import Tuple, Dict
from jsonschema import FormatChecker
from flask import Blueprint
from flask_restx import Api
from ml_rest_api.settings import get_value


class MLRestAPIException(Exception):
    """Base ML Rest API Exception"""


class MLRestAPINotReadyException(MLRestAPIException):
    """Base ML Rest API NOT READY Exception"""


FlaskApiReturnType = Tuple[Dict, int]

log: Logger = getLogger(__name__)

blueprint = Blueprint("api", __name__, url_prefix="/api")

api = Api(  # pylint: disable=invalid-name
    blueprint,
    version="0.1",
    title="Machine Learning REST API",
    description="A RESTful API to return predictions from a trained ML model, \
          built with Python 3 and Flask-RESTX",
    format_checker=FormatChecker(
        formats=(
            "date-time",
            "date",
        )
    ),
    default="health",
    default_label="Basic health check methods",
)


@api.errorhandler(MLRestAPINotReadyException)
def not_ready_error_handler() -> FlaskApiReturnType:
    """NOT READY error handler that returns HTTP 503 error."""
    log.exception("Server Not Ready")
    return {"message": "Server Not Ready"}, 503


@api.errorhandler
def default_error_handler(exception) -> FlaskApiReturnType:
    """Default error handler that returns HTTP 500 error."""
    log.exception(exception.message)
    if get_value("FLASK_DEBUG"):
        error_msg = exception.message
    else:
        error_msg = "An unhandled exception occurred"
    return {"message": error_msg}, 500
