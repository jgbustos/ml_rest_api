"""Basic pytest-based tests for ml_rest_api."""

from http import HTTPStatus
from json import loads
import requests
import pytest
from openapi_spec_validator import (
    validate,
    OpenAPIV2SpecValidator,
    OpenAPIV30SpecValidator,
)
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError


ROOT_URL = "http://localhost:8888/api/"
SWAGGER_JSON_PATH = "swagger.json"
LIVENESS_PATH = "liveness"
READINESS_PATH = "readiness"
MODEL_PREDICT_PATH = "model/predict"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}
GOOD_JSON_DICT = {
    "int_param": 12345,
    "string_param": "foobar",
    "float_param": 123.45,
    "bool_param": True,
    "datetime_param": "2021-11-30T14:37:04.150Z",
    "date_param": "2021-10-26",
}
REQUEST_TIMEOUT = 0.1  # 100 milliseconds, life is too short

NOT_A_DATETIME_MSG = "is not a 'date-time'"
NOT_A_DATE_MSG = "is not a 'date'"


def _get_request(url):
    response = requests.get(
        url,
        allow_redirects=True,
        timeout=REQUEST_TIMEOUT,
    )
    return response


def _post_request(url, headers=None, json=None):
    response = requests.post(
        url,
        headers=headers,
        json=json,
        allow_redirects=True,
        timeout=REQUEST_TIMEOUT,
    )
    return response


def _post_request_good_json_with_overrides(override_key=None, override_value=None):
    json_dict = GOOD_JSON_DICT
    if override_key is not None:
        if override_value is None:
            del json_dict[override_key]
        else:
            json_dict[override_key] = override_value
    response = _post_request(
        ROOT_URL + MODEL_PREDICT_PATH,
        headers=HEADERS,
        json=json_dict,
    )
    return response


def test_get_swagger_json_is_valid_openapi_v2():
    """Verify that /api/swagger.json file complies with OpenAPI v2."""
    response = _get_request(ROOT_URL + SWAGGER_JSON_PATH)
    spec_dict = loads(response.text)
    validate(spec_dict, cls=OpenAPIV2SpecValidator)
    assert response.status_code == HTTPStatus.OK


def test_get_swagger_json_is_not_valid_openapi_v3():
    """Verify that /api/swagger.json file does NOT comply with OpenAPI v3."""
    response = _get_request(ROOT_URL + SWAGGER_JSON_PATH)
    spec_dict = loads(response.text)
    with pytest.raises(OpenAPIValidationError):
        validate(spec_dict, cls=OpenAPIV30SpecValidator)
    assert response.status_code == HTTPStatus.OK


def test_get_liveness_status_code_equals_200():
    """Verify that /api/liveness succeeds with 200 "Alive"."""
    response = _get_request(ROOT_URL + LIVENESS_PATH)
    assert response.status_code == HTTPStatus.OK
    assert "Alive" in response.text and "true" in response.text


def test_get_readiness_status_code_equals_200():
    """Verify that /api/readiness succeeds with 200 "Ready"."""
    response = _get_request(ROOT_URL + READINESS_PATH)
    assert response.status_code == HTTPStatus.OK
    assert "Ready" in response.text and "true" in response.text


def test_post_model_predict_no_headers_no_payload_status_code_equals_415():
    """Verify that calling /api/model/predict with no headers and no payload fails with 415."""
    response = _post_request(ROOT_URL + MODEL_PREDICT_PATH)
    assert response.status_code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE


def test_post_model_predict_no_payload_status_code_equals_400():
    """Verify that calling /api/model/predict with no payload fails with 400."""
    response = _post_request(ROOT_URL + MODEL_PREDICT_PATH, headers=HEADERS)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_post_model_predict_empty_json_status_code_equals_400():
    """Verify that calling /api/model/predict with empty payload fails with 400 and flags all
    properties as required."""
    response = _post_request(ROOT_URL + MODEL_PREDICT_PATH, headers=HEADERS, json={})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "'int_param' is a required property" in response.text
    assert "'string_param' is a required property" in response.text
    assert "'float_param' is a required property" in response.text
    assert "'bool_param' is a required property" in response.text
    assert "'datetime_param' is a required property" in response.text
    assert "'date_param' is a required property" in response.text


def test_post_model_predict_good_json_status_code_equals_200():
    """Verify that calling /api/model/predict with good payload succeeds with 400 and returns
    "mock_prediction"."""
    response = _post_request_good_json_with_overrides()
    assert response.status_code == HTTPStatus.OK
    assert "mock_prediction" in response.text


def test_post_model_predict_int_param_missing_status_code_equals_400():
    """Verify that calling /api/model/predict with no int_param fails with 400 and flags missing
    properties as required."""
    response = _post_request_good_json_with_overrides("int_param", None)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "'int_param' is a required property" in response.text


def test_post_model_predict_string_param_missing_status_code_equals_400():
    """Verify that calling /api/model/predict with no string_param fails with 400 and flags missing
    properties as required."""
    response = _post_request_good_json_with_overrides("string_param", None)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "'string_param' is a required property" in response.text


def test_post_model_predict_float_param_missing_status_code_equals_400():
    """Verify that calling /api/model/predict with no float_param fails with 400 and flags missing
    properties as required."""
    response = _post_request_good_json_with_overrides("float_param", None)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "'float_param' is a required property" in response.text


def test_post_model_predict_bool_param_missing_status_code_equals_400():
    """Verify that calling /api/model/predict with no bool_param fails with 400 and flags missing
    properties as required."""
    response = _post_request_good_json_with_overrides("bool_param", None)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "'bool_param' is a required property" in response.text


def test_post_model_predict_datetime_param_missing_status_code_equals_400():
    """Verify that calling /api/model/predict with no datetime_param fails with 400 and flags
    missing properties as required."""
    response = _post_request_good_json_with_overrides("datetime_param", None)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "'datetime_param' is a required property" in response.text


def test_post_model_predict_date_param_missing_status_code_equals_400():
    """Verify that calling /api/model/predict with no date_param fails with 400 and flags missing
    properties as required."""
    response = _post_request_good_json_with_overrides("date_param", None)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "'date_param' is a required property" in response.text


def test_post_model_predict_int_param_string_status_code_equals_400():
    """Verify that calling /api/model/predict with string as int_param fails with 400 and flags
    wrong type."""
    response = _post_request_good_json_with_overrides("int_param", "a")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "is not of type 'integer'" in response.text


def test_post_model_predict_int_param_float_status_code_equals_400():
    """Verify that calling /api/model/predict with float as int_param fails with 400 and flags
    wrong type."""
    response = _post_request_good_json_with_overrides("int_param", 10.1)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "is not of type 'integer'" in response.text


def test_post_model_predict_string_param_float_status_code_equals_400():
    """Verify that calling /api/model/predict with float as string_param fails with 400 and flags
    wrong type."""
    response = _post_request_good_json_with_overrides("string_param", 9.1)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "is not of type 'string'" in response.text


def test_post_model_predict_float_param_string_status_code_equals_400():
    """Verify that calling /api/model/predict with string as float_param fails with 400 and flags
    wrong type."""
    response = _post_request_good_json_with_overrides("float_param", "a")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "is not of type 'number'" in response.text


def test_post_model_predict_bool_param_string_status_code_equals_400():
    """Verify that calling /api/model/predict with string as bool_param fails with 400 and flags
    wrong type."""
    response = _post_request_good_json_with_overrides("bool_param", "True")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "is not of type 'boolean'" in response.text


def test_post_model_predict_datetime_param_missing_z_status_code_equals_400():
    """Verify that calling /api/model/predict with bad datetime_param (missing ending Z) fails
    with 400 and flags wrong type."""
    response = _post_request_good_json_with_overrides(
        "datetime_param", "2021-11-30T14:37:04.15"
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert NOT_A_DATETIME_MSG in response.text


def test_post_model_predict_datetime_param_bad_day_status_code_equals_400():
    """Verify that calling /api/model/predict with bad datetime_param (impossible day number) fails
    with 400 and flags wrong type."""
    response = _post_request_good_json_with_overrides(
        "datetime_param", "2021-11-35T14:37:04.15Z"
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert NOT_A_DATETIME_MSG in response.text


def test_post_model_predict_datetime_param_bad_month_status_code_equals_400():
    """Verify that calling /api/model/predict with bad datetime_param (impossible month number)
    fails with 400 and flags wrong type."""
    response = _post_request_good_json_with_overrides(
        "datetime_param", "2021-13-30T14:37:04.15Z"
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert NOT_A_DATETIME_MSG in response.text


def test_post_model_predict_datetime_param_bad_year_status_code_equals_400():
    """Verify that calling /api/model/predict with bad datetime_param (impossible year number) fails
    with 400 and flags wrong type."""
    response = _post_request_good_json_with_overrides(
        "datetime_param", "999-11-30T14:37:04.15Z"
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert NOT_A_DATETIME_MSG in response.text


def test_post_model_predict_datetime_param_missing_hyphen_status_code_equals_400():
    """Verify that calling /api/model/predict with bad datetime_param (missing date hyphen) fails
    with 400 and flags wrong type."""
    response = _post_request_good_json_with_overrides(
        "datetime_param", "2021-1130T14:37:04.15Z"
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert NOT_A_DATETIME_MSG in response.text


def test_post_model_predict_datetime_param_missing_t_status_code_equals_400():
    """Verify that calling /api/model/predict with bad datetime_param (missing T between date and
    time) fails with 400 and flags wrong type."""
    response = _post_request_good_json_with_overrides(
        "datetime_param", "2021-11-3014:37:04.15Z"
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert NOT_A_DATETIME_MSG in response.text


def test_post_model_predict_datetime_param_missing_colon_status_code_equals_400():
    """Verify that calling /api/model/predict with bad datetime_param (missing time colon) fails
    with 400 and flags wrong type."""
    response = _post_request_good_json_with_overrides(
        "datetime_param", "2021-11-30T1437:04.15Z"
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert NOT_A_DATETIME_MSG in response.text


def test_post_model_predict_datetime_param_bad_hour_status_code_equals_400():
    """Verify that calling /api/model/predict with bad datetime_param (impossible hour number)
    fails with 400 and flags wrong type."""
    response = _post_request_good_json_with_overrides(
        "datetime_param", "2021-11-30T34:37:04.15Z"
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert NOT_A_DATETIME_MSG in response.text


def test_post_model_predict_datetime_param_bad_minute_status_code_equals_400():
    """Verify that calling /api/model/predict with bad datetime_param (impossible minute number)
    fails with 400 and flags wrong type."""
    response = _post_request_good_json_with_overrides(
        "datetime_param", "2021-11-30T14:77:04.15Z"
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert NOT_A_DATETIME_MSG in response.text


def test_post_model_predict_datetime_param_bad_second_status_code_equals_400():
    """Verify that calling /api/model/predict with bad datetime_param (impossible second number)
    fails with 400 and flags wrong type."""
    response = _post_request_good_json_with_overrides(
        "datetime_param", "2021-11-30T14:37:64.15Z"
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert NOT_A_DATETIME_MSG in response.text


def test_post_model_predict_date_param_bad_year_status_code_equals_400():
    """Verify that calling /api/model/predict with bad date_param (impossible year number) fails
    with 400 and flags wrong type."""
    response = _post_request_good_json_with_overrides("date_param", "999-10-26")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert NOT_A_DATE_MSG in response.text


def test_post_model_predict_date_param_bad_month_status_code_equals_400():
    """Verify that calling /api/model/predict with bad date_param (impossible month number) fails
    with 400 and flags wrong type."""
    response = _post_request_good_json_with_overrides("date_param", "2021-18-26")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert NOT_A_DATE_MSG in response.text


def test_post_model_predict_date_param_bad_day_status_code_equals_400():
    """Verify that calling /api/model/predict with bad date_param (impossible day number) fails
    with 400 and flags wrong type."""
    response = _post_request_good_json_with_overrides("date_param", "2021-10-51")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert NOT_A_DATE_MSG in response.text


def test_post_model_predict_date_param_missing_hyphen_status_code_equals_400():
    """Verify that calling /api/model/predict with bad date_param (missing date hyphen) fails with
    400 and flags wrong type."""
    response = _post_request_good_json_with_overrides("date_param", "2021-1026")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert NOT_A_DATE_MSG in response.text
