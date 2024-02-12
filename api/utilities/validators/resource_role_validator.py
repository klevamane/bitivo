# Models
from ...models import Resource

# Middlewares
from marshmallow import ValidationError

# Messages
from ..messages.error_messages import database_errors, serialization_errors

# Validators
from .duplicate_validator import validate_input_duplicate


def validate_resource_duplicate(permission, resource_ids_set):
    """
    This function validates that resource is not duplicated

    Args:
        permission (dict): A dictionary containing the resource id and permission ids
        resource_ids_set (set): Contains a set of resource ids

    Raises:
        ValidationError: If resource_id is duplicated in the request body.
    """

    validate_input_duplicate(permission, resource_ids_set, 'resource_id')


def validate_resource_exists(data, resource_ids_set):
    """
    Helper function to validate that a the resource exists for a given role

    Args:
        data (list): A list of permission ids

    Raises:
        ValidationError if any of the supplied resource Ids does not exist in the database

    """
    validate_resource_duplicate(data, resource_ids_set)
    if 'resource_id' in data and not Resource.get(data.get('resource_id')):
        raise ValidationError(
            database_errors['non_existing'].format("Resource"), 'resourceId')
