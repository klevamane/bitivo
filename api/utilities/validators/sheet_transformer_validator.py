"""Module for validating that a valid asset status was sent"""

from humps.camel import case

# Exception handlers
from marshmallow import ValidationError

# Enums


# Messages
from ..messages.error_messages import serialization_errors


def validate_doc_name(doc_name):
    """Check that the supplied docname is one of the accepted types

    Args:
        doc_name (string): The doc_name to validate
    Raises:
        ValidationError: When the status supplied is not a valid status
    Returns:
        string: Validated status converted to lowercase
    """
    from api.views.sheet_transformer import transformer_mapper

    valid_keys = list(transformer_mapper.keys())
    if doc_name.lower() not in valid_keys:
        raise ValidationError(serialization_errors['invalid_doc_name'].format(str(valid_keys)))
    return doc_name
