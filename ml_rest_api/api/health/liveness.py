"""This module implements the HealthLiveness class."""
from flask_restx import Resource
from ml_rest_api.api.restx import api, FlaskApiReturnType


@api.default_namespace.route("/liveness")
class HealthLiveness(Resource):
    """Implements the /liveness GET method."""

    @staticmethod
    @api.doc(
        responses={
            200: "Success",
        }
    )
    def get() -> FlaskApiReturnType:
        """
        Returns liveness status.
        """
        return "Alive", 200
