
import pytest
from unittest import mock

from sanic import response

from fyndiq_helpers.decorators import validate_payload, check_required_params


class TestViewDecorators:

    def setup_method(self):
        self.mocked_request = mock.MagicMock()

    def test_validate_payload_success(self):
        self.mocked_request.json = {"field": "value"}

        schema = {
            'field': {'type': 'string'}
        }

        @validate_payload(schema)
        def view(request, payload):
            return response.json({}, status=200)

        request_response = view(self.mocked_request)

        assert request_response.status == 200

    def test_validate_payload_incorrect_type(self):
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
                         b':{"code":400,"message":{"field":["must be of string type"]}}}'
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
                         b'"description":"Following request params are required: [\'required_param\']."}'
        assert request_response.body == expected_error

    def test_check_required_params_missing_multiple_params(self):
        self.mocked_request.args = {}

        @check_required_params(['required_param', 'another_required_param'])
        def view(request):
            return response.json({}, status=200)

        request_response = view(self.mocked_request)

        assert request_response.status == 400
        expected_error = b'{"status":"ERROR",'\
                         b'"description":"Following request params are required: '\
                         b'[\'required_param\', \'another_required_param\']."}'
        assert request_response.body == expected_error
