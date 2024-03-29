""" Module with string generic validator. """
import re

from marshmallow import ValidationError
from ..messages.error_messages import serialization_errors

string_regex = re.compile(r"^[a-zA-Z0-9]+(([' .-][a-zA-Z0-9])?[a-zA-Z0-9]*)*$")


def name_validator(data):
    """
    Checks if given string is at least 1 character and only contains letters,
    numbers and non consecutive fullstops, hyphens, spaces and apostrophes.
    Raises validation error otherwise.
    """

    if not data:
        raise ValidationError(serialization_errors['not_empty'])
    else:
        if not re.match(string_regex, data):
            raise ValidationError(serialization_errors['string_characters'])
