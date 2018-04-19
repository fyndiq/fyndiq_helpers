from functools import wraps
from typing import Any, Callable

import structlog

import cerberus
from sanic import response

logger = structlog.get_logger(__name__)


class check_required_params:
    """
    This will return 400 from a view if a required param/params are missing.
    """

    def __init__(self, required_params: list) -> None:
        assert required_params
        self.required_params = required_params

    def __call__(self, function: Callable) -> Callable:
        @wraps(function)
        def wrapped_view_function(*args, **kwargs) -> Any:
            request = args[0]
            request_args = request.args

            missing_params = [
                param for param in self.required_params
                if not request_args.get(param)
            ]

            if missing_params:
                return response.json({
                    'status': 'ERROR',
                    'description': f'Following request params are required: {missing_params}.'  # noqa
                }, status=400)
            return function(request, **kwargs)

        return wrapped_view_function


class validate_payload:
    """
    Class based decorator for validating data in views.

    The validation is done by Cerberus lib against view-specific schemas.
    """

    def __init__(self, schema: dict,
                 allow_unknown_fields: bool = False) -> None:
        self.schema = schema
        self.allow_unknown_fields = allow_unknown_fields

    def __call__(self, view: Callable) -> Callable:
        @wraps(view)
        def wrapped_function(request, *args, **kwargs) -> Any:

            if 'application/json' not in request.content_type:
                return response.json(
                    {
                        'description': 'Unsupported Media Type',
                        'content': {
                            'code': 415,
                            'message': 'Expected application/json'
                        }
                    },
                    415
                )

            payload = request.json or {}
            validator = cerberus.Validator(
                self.schema,
                allow_unknown=self.allow_unknown_fields
            )
            if not validator.validate(payload):
                errors = validator.errors
                description = 'Invalid payload'
                logger.warning(description, payload=payload, errors=errors)
                desc = {
                    'description': description,
                    'content': {
                        'code': 400,
                        'message': errors
                    }
                }
                return response.json(desc, 400)

            return view(request, payload, *args, **kwargs)

        return wrapped_function


class in_state:
    """
    Check if the event aggregate is in allowed state.

    TODO: maybe this should raise some InvalidStateException.
    """

    def __init__(self, allowed_states: list) -> None:
        self.allowed_states = allowed_states

    def __call__(self, function: Callable) -> Callable:
        @wraps(function)
        def wrapped_function(*args, **kwargs) -> Any:
            instance, _ = args

            if instance.state in self.allowed_states:
                return function(*args, **kwargs)
            logger.warning(
                'Invalid aggregate state', method=function.__name__,
                current_state=instance.state,
                allowed_states=[state for state in self.allowed_states]
            )

        return wrapped_function
