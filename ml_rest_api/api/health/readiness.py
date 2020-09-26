"""This module implements the HealthReadiness class."""
from flask_restx import Resource
from ml_rest_api.api.restx import api, FlaskApiReturnType
from ml_rest_api.ml_trained_model.wrapper import trained_model_wrapper


@api.default_namespace.route("/readiness")
class HealthReadiness(Resource):
    """Implements the /readiness GET method."""

    @staticmethod
    @api.doc(
        responses={
            200: "Success",
            500: "Server Not Ready",
        }
    )
    def get() -> FlaskApiReturnType:
        """
        Returns readiness status
        """
        if trained_model_wrapper.ready():
            return "Ready", 200
        return "Not Ready", 500
