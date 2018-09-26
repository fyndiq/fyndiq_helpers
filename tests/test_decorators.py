
import pytest
from unittest import mock

from sanic import response

from fyndiq_helpers.decorators import (
    validate_payload, check_required_params, validate_data)
from fyndiq_helpers.exceptions import ValidationFailedException


class TestViewDecorators:

    def setup_method(self):
        self.mocked_request = mock.MagicMock()

    def test_validate_payload_success(self):
        self.mocked_request.content_type = 'application/json'
        self.mocked_request.json = {"field": "value"}

        schema = {
            'field': {'type': 'string'}
        }

        @validate_payload(schema)
        def view(request, payload):
            return response.json({}, status=200)

        request_response = view(self.mocked_request)

        assert request_response.status == 200

    def test_validate_content_type_with_parameters(self):
        self.mocked_request.content_type = 'application/json; charset=UTF8'
        self.mocked_request.json = {"field": "value"}

        schema = {
            'field': {'type': 'string'}
        }

        @validate_payload(schema)
        def view(request, payload):
            return response.json({}, status=200)

        request_response = view(self.mocked_request)

        assert request_response.status == 200

    def test_validate_payload_incorrect_content_type(self):
        self.mocked_request.content_type = 'application/octet-stream'
        self.mocked_request.json = {"field": 12345}

        schema = {
            'field': {'type': 'string'}
        }

        @validate_payload(schema)
        def view(request, payload):
            return response.json({}, status=200)

        request_response = view(self.mocked_request)

        assert request_response.status == 415
        assert request_response.body == b'{"description":' \
                                        b'"Unsupported Media Type",' \
                                        b'"content":{"code":415,"message":' \
                                        b'"Expected application\\/json"}}'

    def test_validate_payload_incorrect_type(self):
        self.mocked_request.content_type = 'application/json'
        self.mocked_request.json = {"field": 12345}

        schema = {
            'field': {'type': 'string'}
        }

        @validate_payload(schema)
        def view(request, payload):
            return response.json({}, status=200)

        request_response = view(self.mocked_request)

        assert request_response.status == 400
        expected_error = b'{"description":"Invalid payload","content"' \
                         b':{"code":400,"message":{"field":["must be of string type"]}}}'  # noqa
        assert request_response.body == expected_error

    def test_validate_payload_should_ignore_extra_fields(self):
        self.mocked_request.content_type = 'application/json'
        self.mocked_request.json = {
            'field': 'aaaaa',
            'extra_field': 33333,
        }

        schema = {
            'field': {'type': 'string'}
        }

        @validate_payload(schema, allow_unknown_fields=True)
        def view(request, payload):
            return response.json({}, status=200)

        request_response = view(self.mocked_request)

        assert request_response.status == 200

    def test_validate_payload_ignore_should_complain_about_fields(self):
        self.mocked_request.content_type = 'application/json'
        self.mocked_request.json = {
            'field': 'aaaaa',
            'extra_field': 33333,
        }

        schema = {
            'field': {'type': 'string'}
        }

        @validate_payload(schema)
        def view(request, payload):
            return response.json({}, status=200)

        request_response = view(self.mocked_request)

        assert request_response.status == 400
        expected_error = b'{"description":"Invalid payload","content"' \
                         b':{"code":400,"message":{"extra_field":["unknown field"]}}}'  # noqa
        print(request_response.body)
        assert request_response.body == expected_error

    def test_check_required_params_success(self):
        self.mocked_request.args = {"required_param": "value"}

        @check_required_params(['required_param', ])
        def view(request):
            return response.json({}, status=200)

        request_response = view(self.mocked_request)

        assert request_response.status == 200

    def test_check_required_params_missing_decorator_argument(self):
        with pytest.raises(AssertionError):
            @check_required_params([])
            def view(request, payload):
                return response.json({}, status=200)

    def test_check_required_params_missing_param(self):
        self.mocked_request.args = {}

        @check_required_params(['required_param', ])
        def view(request):
            return response.json({}, status=200)

        request_response = view(self.mocked_request)

        assert request_response.status == 400
        expected_error = b'{"status":"ERROR",'\
                         b'"description":"Following request params are required: [\'required_param\']."}'   # noqa
        assert request_response.body == expected_error

    def test_check_required_params_missing_multiple_params(self):
        self.mocked_request.args = {}

        @check_required_params(['required_param', 'another_required_param'])
        def view(request):
            return response.json({}, status=200)

        request_response = view(self.mocked_request)

        assert request_response.status == 400
        expected_error = b'{"status":"ERROR",'\
                         b'"description":' \
                         b'"Following request params are required: '\
                         b'[\'required_param\', \'another_required_param\']."}'
        assert request_response.body == expected_error

    @pytest.mark.parametrize('schema, indata, expected_result', [
        ({'field': {'type': 'string'}}, {'field': 'a'}, True),
        ({'field': {'type': 'string'}}, {'field': 1}, False),
        ({'field': {'type': 'string'}}, {'field2': 'a'}, False),
    ])
    def test_validate_data_raises_exception_on_faulty_data(
        self, schema, indata, expected_result
    ):
        @validate_data(schema)
        def test_method(field):
            pass

        if expected_result is True:
            test_method(**indata)
        else:
            with pytest.raises(ValidationFailedException):
                test_method(**indata)
