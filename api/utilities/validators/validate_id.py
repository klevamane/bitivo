"""Module to validate resource id from url parameters"""

import re
from functools import wraps
from marshmallow import ValidationError

from api.middlewares.base_validator import (ValidationError as
                                            CustomValidationError)
from ..messages.error_messages import serialization_errors


def is_valid_id(id_):
    """Check if id is valid"""
    return re.match(r'^[\-a-zA-Z0-9_]+\Z', id_)


def validate_id(func):
    """Decorator function for views to validate id"""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        """Function with decorated function mutations."""
        check_id_valid(**kwargs)
        return func(*args, **kwargs)

    return decorated_function


def id_validator(item_id):
    """
    Used to validate id within schema

    Arguments:
        item_id (string): id of the resource to validate

    Raises:
        ValidationError: Used to raise exception if id is not valid
    """
    if not is_valid_id(item_id):
        raise ValidationError(serialization_errors['invalid_id_field'])


def check_id_valid(**kwargs):
    """Check if id is valid"""
    for key in kwargs:
        if key.endswith('_id') and not is_valid_id(kwargs.get(key, None)):
            raise CustomValidationError(
                {
                    'status': 'error',
                    'message': serialization_errors['invalid_id']
                }, 400)


def bulk_ids_validate(id_list_not_existing):
    """
    Used to validate ids from the user request

    Arguments:
        id_list_not_existing (list): list ids not found in the db, hence needs validating

    Returns:
        a tuple of invalid ids and ids not found
    """

    not_found_list = []
    invalid_ids = []
    for id in id_list_not_existing:
        if not re.search(r'[\s]', id):
            not_found_list.append(id)

        elif re.search(r'[\s]', id):
            invalid_ids.append(id)
    return invalid_ids, not_found_list
