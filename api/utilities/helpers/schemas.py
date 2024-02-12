"""Helper functions for schemas"""

# Messages
from ..messages.error_messages import serialization_errors
from api.utilities.error import raises


def date_args(**kwargs):
    """ marshmallow fields for date validation in schema.
        Args:
            kwargs: key word arguments use in fields
            ie validate=some_function

        Returns:
            dict: Resultant fields to be passed to a schema

        """
    return {
        "required": True,
        "error_messages": {
            'invalid':
            serialization_errors['invalid_date_time'].format(
                kwargs.get('value')),
            'required':
            serialization_errors['field_required']
        }
    }


def common_args(**kwargs):
    """ Returns the common arguments used in marshmallow fields.
    Args:
        kwargs: key word arguments use in fields
        ie validate=some_function

    Returns:
        dict: Resultant fields to be passed to a schema

    """

    return {
        "required": True,
        "validate": kwargs.get('validate'),
        "error_messages": {
            'required': serialization_errors['field_required']
        }
    }


def validate_repeat_days(data):

    days = [
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
        'Sunday'
    ]
    for key in data:
        if key not in days:
            raises(
                'invalid_enum_value',
                status_code=400,
                values=
                "Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday in repeat days"
            )


def validate_ends_field(data):
    """ Allows only single kwargs to be passed on the ends field.
    Args:
        data: dictionary containing ends with kwargs

    Returns:
        None

    """
    if len(data) > 1:
        raises(
            'invalid_enum_value',
            400,
            values='on, never or after in ends field')
