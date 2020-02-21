"""This module implements the ModelPredict class."""
from typing import Dict
from aniso8601 import parse_date, parse_datetime
from flask import request
from flask_restx import Resource, Model, fields
from ml_rest_api.api.restx import api, FlaskApiReturnType
from ml_rest_api.ml_trained_model.wrapper import trained_model_wrapper


def build_api_model() -> Model:
    """
    Returns a Flask-RESTX Api Model based on the sample dict returned by the trained model wrapper.
    This will be used to validate input and automatically generate the Swagger prototype.
    """
    fields_classes_map: Dict = {
        "str": fields.String,
        "int": fields.Integer,
        "float": fields.Float,
        "bool": fields.Boolean,
        "datetime": fields.DateTime,
        "date": fields.Date,
    }
    model_dict: Dict = {}
    model_sample: Dict = trained_model_wrapper.sample()
    if model_sample:
        for key, value in model_sample.items():
            fields_class: fields.Raw = fields_classes_map.get(
                type(value).__name__, fields.String
            )
            if type(value).__name__ == "str":
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
            model_dict[key] = fields_class(example=value, readonly=True, required=True)
    return api.model("input_vector", model_dict)


ns = api.namespace(  # pylint: disable=invalid-name
    "model",
    description="Methods supported by our ML model",
    validate=bool(trained_model_wrapper.sample()),
)


@ns.route("/predict")
class ModelPredict(Resource):
    """Implements the /model/predict POST method."""

    @staticmethod
    @api.expect(build_api_model())
    @api.doc(
        responses={
            200: "Success",
            400: "Input Validation Error",
            500: "Server Not Ready",
        }
    )
    def post() -> FlaskApiReturnType:
        """
        Returns a prediction using the model.
        """
        if trained_model_wrapper.ready():
            data = dict(request.json)
            ret = trained_model_wrapper.run(data)
            return ret, 200
        return "Not Ready", 500
