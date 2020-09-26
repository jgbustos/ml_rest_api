"""Module that creates the Api object and declares default error handler."""
from logging import Logger, getLogger
from typing import Tuple, Iterable
from jsonschema import FormatChecker
from flask_restx import Api
from ml_rest_api.settings import get_value

FlaskApiReturnType = Tuple[Iterable, int]

log: Logger = getLogger(__name__)

api = Api(  # pylint: disable=invalid-name
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


@api.errorhandler
def default_error_handler(exception) -> FlaskApiReturnType:
    """Default error handler that returns HTTP 500 error."""
    log.exception(exception.message)
    if get_value("FLASK_DEBUG"):
        error_msg = exception.message
    else:
        error_msg = "An unhandled exception occurred"
    return {"message": error_msg}, 500
