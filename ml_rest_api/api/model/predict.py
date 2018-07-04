"""This module implements the ModelPredict class."""
import logging
from http import HTTPStatus
from aniso8601 import parse_date, parse_datetime
from flask import request
from flask_restplus import Resource, fields
from ml_rest_api.api.restplus import api
from ml_rest_api.ml_trained_model.wrapper import trained_model_wrapper

log = logging.getLogger(__name__)

fields_classes = {
    'str': fields.String,
    'int': fields.Integer,
    'float': fields.Float,
    'bool': fields.Boolean,
    'datetime': fields.DateTime,
    'date': fields.Date,
}
data_point_dict = {}
data_sample = trained_model_wrapper.sample()
if data_sample is not None:
    for key, value in data_sample.items():
        fields_class = fields_classes.get(type(value).__name__, fields.String)
        if type(value).__name__ == 'str':
            try:
                parse_date(value)
                fields_class = fields.Date
            except ValueError:
                pass
            try:
                parse_datetime(value)
                fields_class = fields.DateTime
            except ValueError:
                pass
        data_point_dict[key] = fields_class(example=value, readonly=True, required=True)
data_point = api.model('data_point', data_point_dict)

ns = api.namespace('model', description='Methods supported by our ML model',
                   validate=(data_sample is not None))

@ns.route('/predict')
class ModelPredict(Resource):
    """Implements the /model/predict POST method."""

    @staticmethod
    @api.expect(data_point)
    @api.doc(responses={
        HTTPStatus.OK: 'Success',
        HTTPStatus.BAD_REQUEST: 'Input Validation Error',
        HTTPStatus.INTERNAL_SERVER_ERROR: 'Server Not Ready',
    })
    def post():
        """
        Returns a prediction using the model.
        """
        if trained_model_wrapper.ready():
            data = dict(request.json)
            ret = trained_model_wrapper.run(data)
            return ret, HTTPStatus.OK
        return 'Not Ready', HTTPStatus.INTERNAL_SERVER_ERROR
