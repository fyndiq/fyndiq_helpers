from functools import wraps
from typing import Callable

import structlog

import cerberus
from sanic import response

logger = structlog.get_logger(__name__)


def validate_payload(schema):
    """
    Validate payload according given schema.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(request, *args, **kwargs):
            payload = request.json or {}
            validator = cerberus.Validator(schema)
            if not validator.validate(payload):
                logger.warning(
                    "Invalid payload", payload=payload, errors=validator.errors
                )
                return response.json(validator.errors, 400)
            return f(request, payload, *args, **kwargs)
        return decorated_function
    return decorator


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
