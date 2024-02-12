""" Module with url validator. """
import re

from marshmallow import ValidationError
from ..messages.error_messages import serialization_errors

URL_REGEX = re.compile(r"^(http(s)?:\/\/)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)$")

def url_validator(data):
    """
    Checks if given string is at least 1 character and only contains characters
    that make a valid url.
    Raises validation error otherwise.
    """

    # Check if string is empty
    if not len(data) > 0:
        raise ValidationError(serialization_errors['url_syntax'].format(data))
    # Otherwise check if url pattern is matched
    elif not re.match(URL_REGEX, data):
        raise ValidationError(serialization_errors['url_syntax'].format(data))

