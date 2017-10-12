from functools import wraps
from typing import Callable

import structlog

import cerberus
from sanic import response

logger = structlog.get_logger(__name__)


class ValidateRequest:
    def __init__(self, validator_schema: dict) -> None:
        self.validator_schema = validator_schema

    def __call__(self, view_function: Callable) -> None:

        @wraps(view_function)
        def wrapped_view_function(*args, **kwargs):
            request = args[0]
            payload = request.json or {}

            validator = cerberus.Validator(self.validator_schema)
            if not validator.validate(payload):
                logger.info(
                    "Received data is not valid!",
                    payload=payload, errors=validator.errors
                )
                return response.json(validator.errors, 400)

            return view_function(request, **kwargs)

        return wrapped_view_function


def in_state(allowed_states):
    def wrapper(func):
        @wraps(func)
        def _in_state(*args, **kwargs):
            instance, _ = args
            if instance.state in allowed_states:
                return func(*args, **kwargs)
            logger.warning(
                "Invalid aggregate state", method=func.__name__,
                current_state=instance.state,
                allowed_states=[e for e in allowed_states]
            )
        return _in_state
    return wrapper
