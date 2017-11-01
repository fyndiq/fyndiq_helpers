
from unittest import mock, TestCase

from sanic import response

from fyndiq_helpers.decorators import validate_payload, check_required_params


class ViewDecoratorsTest(TestCase):

    def setUp(self):
        self.mocked_request = mock.MagicMock()

    def test_validate_payload_success(self):
        self.mocked_request.json = {"field": "value"}

        schema = {
            'field': {'type': 'string'}
        }

        @validate_payload(schema)
        def view(request):
            return response.json({}, status=200)

        request_response = view(self.mocked_request)

        self.assertEqual(200, request_response.status)

    def test_validate_payload_missing_schema_decorator_argument(self):
        with self.assertRaises(AssertionError):
            @validate_payload([])
            def view(request):
                return response.json({}, status=200)

    def test_validate_payload_incorrect_type(self):
        self.mocked_request.json = {"field": 12345}

        schema = {
            'field': {'type': 'string'}
        }

        @validate_payload(schema)
        def view(request):
            return response.json({}, status=200)

        request_response = view(self.mocked_request)

        self.assertEqual(400, request_response.status)
        expected_error = b'{"field":["must be of string type"]}'
        self.assertEqual(expected_error, request_response.body)

    def test_check_required_params_success(self):
        self.mocked_request.args = {"required_param": "value"}

        @check_required_params(['required_param', ])
        def view(request):
            return response.json({}, status=200)

        request_response = view(self.mocked_request)

        self.assertEqual(200, request_response.status)

    def test_check_required_params_missing_decorator_argument(self):
        with self.assertRaises(AssertionError):
            @check_required_params([])
            def view(request):
                return response.json({}, status=200)

    def test_check_required_params_missing_param(self):
        self.mocked_request.args = {}

        @check_required_params(['required_param', ])
        def view(request):
            return response.json({}, status=200)

        request_response = view(self.mocked_request)

        self.assertEqual(400, request_response.status)
        expected_error = b'{"status":"ERROR",'\
                         b'"description":"Following request params are required: [\'required_param\']."}'
        self.assertEqual(expected_error, request_response.body)

    def test_check_required_params_missing_multiple_params(self):
        self.mocked_request.args = {}

        @check_required_params(['required_param', 'another_required_param'])
        def view(request):
            return response.json({}, status=200)

        request_response = view(self.mocked_request)

        self.assertEqual(400, request_response.status)
        expected_error = b'{"status":"ERROR",'\
                         b'"description":"Following request params are required: '\
                         b'[\'required_param\', \'another_required_param\']."}'
        self.assertEqual(expected_error, request_response.body)
