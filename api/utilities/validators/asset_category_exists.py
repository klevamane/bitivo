"""Module for asset category exists marshmallow validator."""
from flask import g

from api.models.asset_category import AssetCategory, Priority
from .validate_id import is_valid_id
from .validate_category import validate_category_exists

from ..error import raise_error


def asset_category_exists(category_id):
    """Marshmallow function to verify an asset category exists in the db.

    :param category_id: The asset category id to verify
    :type request: string

    :raises: Marshmallow Validation error if the asset category doesn't exist.
    """
    validate_category_exists(AssetCategory, category_id)


def validate_priority(priority):
    """Check whether the priority is a valid enum type

    Args:
       priority (str): The asset category's priority

    Raises:
        ValidationError: If the priority has an invalid value
    """
    if priority.lower() not in {priority.name for priority in Priority}:
        raise_error('invalid_priority', priority)
