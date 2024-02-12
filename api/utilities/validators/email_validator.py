""" Module with email validator. """
import re

from marshmallow import ValidationError
from ..messages.error_messages import serialization_errors

EMAIL_REGEX = re.compile(
    r"^[\-a-zA-Z0-9_]+(\.[\-a-zA-Z0-9_]+)*@andela\.com\Z", re.I | re.UNICODE)


def email_validator(data):
    """
    Checks if given string is at least 1 character and only contains characters
    that make a valid andela email.
    """

    data = data.lower()

    # Check if email pattern is matched
    if not EMAIL_REGEX.match(data):
        raise ValidationError(
            serialization_errors['email_syntax'])
