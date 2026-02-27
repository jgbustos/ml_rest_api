"""This module is the RESTful service entry point."""

import os
import warnings
from logging import Logger, getLogger
from flask import Flask
from flask_wtf import CSRFProtect  # pylint: disable=unused-import  # type: ignore
from ml_rest_api.logging_setup import setup_logging
from ml_rest_api.settings import get_value
from ml_rest_api.ml_trained_model.wrapper import trained_model_wrapper
from ml_rest_api.api.restx import blueprint
import ml_rest_api.api.health.liveness  # pylint: disable=unused-import  # pyright: ignore[reportUnusedImport]
import ml_rest_api.api.health.readiness  # pylint: disable=unused-import  # pyright: ignore[reportUnusedImport]
import ml_rest_api.api.model.predict  # pylint: disable=unused-import  # pyright: ignore[reportUnusedImport]

IN_UWSGI: bool = True  # pylint: disable=invalid-name
try:
    import uwsgi  # pylint: disable=unused-import  # type: ignore
except ImportError:
    IN_UWSGI = False  # pylint: disable=invalid-name


def configure_app(flask_app: Flask) -> None:
    """Configures the app."""
    flask_settings_to_apply: list[str] = [
        #'FLASK_SERVER_NAME',
        "SWAGGER_UI_DOC_EXPANSION",
        "RESTX_VALIDATE",
        "RESTX_MASK_SWAGGER",
        "SWAGGER_UI_JSONEDITOR",
        "ERROR_404_HELP",
        "WTF_CSRF_ENABLED",
    ]
    for key in flask_settings_to_apply:
        flask_app.config[key] = get_value(key)
    flask_app.config["SECRET_KEY"] = os.urandom(32)


def initialize_app(flask_app: Flask) -> None:
    """Initialises the app."""
    configure_app(flask_app)
    with warnings.catch_warnings():
        # Temporarily suppressing a warning during registration of the Flask blueprint
        warnings.filterwarnings(
            "ignore", message="The setup method", category=UserWarning
        )
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
    APP.run(
        debug=get_value("FLASK_DEBUG"),
        port=get_value("FLASK_PORT"),
        host=get_value("FLASK_HOST"),
    )


APP = Flask(__name__)
setup_logging()
log: Logger = getLogger(__name__)
initialize_app(APP)

if __name__ == "__main__":
    main()
