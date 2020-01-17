"""This module is the RESTful service entry point."""
import os
import sys
from logging import Logger, getLogger
import logging.config
from flask import Flask, Blueprint
from ml_rest_api.settings import get_value
from ml_rest_api.ml_trained_model.wrapper import trained_model_wrapper
from ml_rest_api.api.health.liveness import HealthLiveness
from ml_rest_api.api.health.readiness import HealthReadiness
import ml_rest_api.api.model.predict
from ml_rest_api.api.restplus import api
from typing import List

IN_UWSGI: bool = False
try:
    import uwsgi

    IN_UWSGI = True
except ImportError:
    None


def configure_app(flask_app: Flask) -> None:
    """Configures the app."""
    flask_settings_to_apply: List = [
        #'FLASK_SERVER_NAME',
        "SWAGGER_UI_DOC_EXPANSION",
        "RESTPLUS_VALIDATE",
        "RESTPLUS_MASK_SWAGGER",
        "SWAGGER_UI_JSONEDITOR",
        "ERROR_404_HELP",
    ]
    for key in flask_settings_to_apply:
        flask_app.config[key] = get_value(key)


def initialize_app(flask_app: Flask) -> None:
    """Initialises the app."""
    configure_app(flask_app)
    blueprint = Blueprint("api", __name__, url_prefix="/api")
    api.init_app(blueprint)
    flask_app.register_blueprint(blueprint)
    if get_value("MULTITHREADED_INIT") and not IN_UWSGI:
        trained_model_wrapper.multithreaded_init()
    else:
        trained_model_wrapper.init()


def main() -> None:
    """Main routine, executed only if running as stand-alone."""
    log.info(
        "***** Starting development server at http://%s/api/ *****",
        get_value("FLASK_SERVER_NAME"),
    )
    app.run(
        debug=get_value("FLASK_DEBUG"),
        port=get_value("FLASK_PORT"),
        host=get_value("FLASK_HOST"),
    )


app = Flask(__name__)
logging.config.fileConfig(
    os.path.normpath(os.path.join(os.path.dirname(__file__), "../logging.conf"))
)
log: Logger = getLogger(__name__)
initialize_app(app)

if __name__ == "__main__":
    main()
