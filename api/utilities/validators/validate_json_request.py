"""Module to validate for json content type in request"""

from functools import wraps

from flask import request

from api.utilities.messages.error_messages import serialization_error
from ..messages.error_messages import serialization_errors
from ...middlewares.base_validator import ValidationError


def validate_json_request(func):
    """Decorator function to check for json content type in request"""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            raise ValidationError(
                {
                    'status': 'error',
                    'message': serialization_errors['json_type_required']
                }, 400)
        return func(*args, **kwargs)

    return decorated_function


def validate_bulk_assets_json(func):
    """Validates if json user has passed is list of dicts
    Args:
        func(function) Function with assets
    Returns:
          function: Returns function if no errors
    Raises:
        ValidationError: If assets is non, or empty, or not a list
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        assets = request.get_json()
        error = {"status": "error"}
        if not assets or not isinstance(assets, dict):
            raise ValidationError({
                "message":
                    serialization_error.error_dict["data_type"].format(
                        "Assets", "dictionary"), **error
            }, 400)
        if not assets.get("assets"):
            raise ValidationError({
                "message":
                    serialization_error.error_dict["required_field"].format(
                        "Assets payload"),
                **error
            }, 400)
        return func(*args, **kwargs)

    return decorated_function


def validate_assets_type(func):
    """Decorator function to check for json content type in request"""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        assets = request.get_json()
        if not isinstance(assets.get("assets"), list):
            raise ValidationError({
                "message":
                    serialization_error.error_dict["data_type"].format(
                        "Assets", "list"),
                "status": "error"
            }, 400)
        return func(*args, **kwargs)

    return decorated_function


def validate_reason(func):
    """Validates if json reason in request
    Args:
        func(function) Function with reason
    Returns:
          function: Returns function if no errors
    Raises:
        ValidationError: if json reason not in request
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        result = request.get_json()
        reason = result.get('reason')
        if not reason:
            raise ValidationError({
                "message":
                    serialization_error.error_dict["select_reason"].format(
                        "cancellation reason"),
                "status": "error"
            }, 400)
        kwargs = {"reason": reason, "hot_desk_id": kwargs.get('hot_desk_id')}
        return func(*args, **kwargs)

    return decorated_function


def validate_resource_access_level_field(func):
    """Validates if json user has passed contains the resourceAccessLevels
    field
    Args:
        func(function) Function with assets
    Returns:
          function: Returns function if no errors
    Raises:
        ValidationError: If the resourceAccessLevels is not present
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        role = request.get_json()
        error = {"status": "error"}
        if 'resourceAccessLevels' not in role.keys():
            raise ValidationError({
                "message":
                    serialization_error.error_dict["required_field"].format(
                        "resourceAccessLevels payload"),
                **error
            }, 400)
        return func(*args, **kwargs)

    return decorated_function
