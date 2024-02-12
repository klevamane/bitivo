""" Module for validating the status field of a user"""
from marshmallow import ValidationError
from ..messages.error_messages import serialization_errors


def validate_status(status):
    """
    Used to validate status field in user schema to be either
    'enabled' or 'disabled'

    Arguments:
        status (string): field to be validated

    Raises:
        ValidationError: Used to raise exception if status field is
        neither 'enabled' nor 'disabled'
    """

    if status.lower() not in ['enabled', 'disabled']:
        raise ValidationError(serialization_errors['invalid_status'])



def validate_hot_desk_status(status):
    """
    Used to validate status field in hot desk schema to be one of
    "pending", "approved" or "rejected"

    Arguments:
        status (string): field to be validated

    Raises:
        ValidationError: Used to raise exception if status field is
        not in ["pending", "approved", "rejected"]
    """

    if status.value.lower() not in ["pending", "approved", "rejected", "cancelled"]:
        raise ValidationError(serialization_errors['invalid_hot_desk_status'])
