"""This module implements the HealthReadiness class."""
from http import HTTPStatus
from flask_restplus import Resource
from ml_rest_api.api.restplus import api
from ml_rest_api.ml_trained_model.wrapper import trained_model_wrapper

@api.default_namespace.route('/readiness')
class HealthReadiness(Resource):
    """Implements the /readiness GET method."""

    @staticmethod
    @api.doc(responses={
        HTTPStatus.OK: 'Success',
        HTTPStatus.INTERNAL_SERVER_ERROR: 'Server Not Ready',
    })
    def get():
        """
        Returns readiness status
        """
        if trained_model_wrapper.ready():
            return 'Ready', HTTPStatus.OK
        return 'Not Ready', HTTPStatus.INTERNAL_SERVER_ERROR
