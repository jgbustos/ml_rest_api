"""This module implements the HealthLiveness class."""
from http import HTTPStatus
from flask_restplus import Resource
from ml_rest_api.api.restplus import api

ns = api.default_namespace

@ns.route('/liveness')
class HealthLiveness(Resource):
    """Implements the /liveness GET method."""

    @staticmethod
    @api.doc(responses={
        HTTPStatus.OK: 'Success',
    })
    def get():
        """
        Returns liveness status.
        """
        return 'Alive', HTTPStatus.OK
