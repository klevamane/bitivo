"""
A module for raising errors
"""
from api.middlewares.base_validator import ValidationError
from marshmallow import ValidationError as MarshmallowError
from .messages.error_messages import serialization_errors


def raises(error_key, status_code, *args, **kwargs):
    """
    Raises a serialization error

    Parameters:
        error_key (str): the key for accessing the correct error message
        args (*): variable number of arguments
        kwargs (**): variable number of keyword arguments
    """

    raise ValidationError(
        {
            'message': serialization_errors[error_key].format(*args, **kwargs)
        }, status_code)


def raise_exception(error_message_mapper, error_key, status_code, *args):
    """Raises validation error

    Args:
        error_message_mapper (dict): maps key to error message
        error_key (str): the key that maps to relevant error message
        status_code (int): the error status code
        args (*): variable number of arguments

    Raises:
        ValidationError
    """

    raise ValidationError(
        {
            'message': error_message_mapper[error_key].format(*args)
        }, status_code)


def raise_error(error_key, *args, **kwargs):
    """Raises a Marshmallow validation error

    Args:
        error_key (str): The key for accessing the correct error message
        *args: Arguments taken by the serialization error message
        **kwargs:
            fields (list): The fields where the error will appear

    Raises:
        ValidationError: Marshmallow validation error
    """
    raise MarshmallowError(serialization_errors[error_key].format(*args),
                           kwargs.get('fields'))


def raise_error_helper(should_raise_error, error_mapper, error_key, *args):
    """Raises validator error when should_raise_error parameter is True

    Args:
        should_raise_error(bool): Determines whether to raise error or not
        error_mapper (dict): maps key to error message
        error_key (str): the key that maps to relevant error message
        args (*): variable number of arguments

    Raises:
        ValidationError: if the is_invalid parameter is True
    """
    status_code = 400
    if should_raise_error:
        raise_exception(error_mapper, error_key, status_code, *args)
