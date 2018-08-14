"""Settings file."""
import os

def get_value(key):
    """Returns a value from the corresponding env var or from settings if env var doesn't exist."""
    settings = {
        # Flask settings
        'FLASK_SERVER_NAME': 'localhost:8888',
        'FLASK_HOST': '0.0.0.0',
        'FLASK_PORT': 8888,
        'FLASK_DEBUG': True,  # Do not use debug mode in production

        # Flask-Restplus settings
        'SWAGGER_UI_DOC_EXPANSION': 'list',
        'RESTPLUS_VALIDATE': True,
        'RESTPLUS_MASK_SWAGGER': False,
        'ERROR_404_HELP': False,
        'SWAGGER_UI_JSONEDITOR': True,

        # Trained ML/AI model settings
        'TRAINED_MODEL_MODULE_NAME': 'ml_trained_model',
    }
    return os.environ[key] if key in os.environ else settings[key]
