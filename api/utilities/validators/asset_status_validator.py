"""Module for validating that a valid asset status was sent"""
# Exception handlers
from marshmallow import ValidationError

# Enums
from api.utilities.enums import AssetStatus

# Messages
from ..messages.error_messages import serialization_errors


def validate_asset_status(status):
    """Check that the supplied status is one of the accepted types

    Args:
        status (string): The status to validate
    Raises:
        ValidationError: When the status supplied is not a valid status
    Returns:
        string: Validated status converted to lowercase
    """
    valid_status = AssetStatus.get_all()
    if status.lower() not in valid_status:
        raise ValidationError(serialization_errors['asset_status'].format(
            asset_status=str(valid_status)))
    return status.lower()
