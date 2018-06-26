from http import HTTPStatus
from flask_restplus import Resource
from ml_rest_api.api.restplus import api
from ml_rest_api.ml_trained_model.wrapper import trained_model_wrapper

ns = api.default_namespace

@ns.route('/readiness')
class HealthReadiness(Resource):

    @api.doc(responses={
        HTTPStatus.OK: 'Success',
        HTTPStatus.INTERNAL_SERVER_ERROR: 'Server Not Ready',
    })
    def get(self):
        """
        Returns readiness status
        """
        if trained_model_wrapper.ready():
            return 'Ready', HTTPStatus.OK
        else:
            return 'Not Ready', HTTPStatus.INTERNAL_SERVER_ERROR
