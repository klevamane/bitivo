"""Module to check if a resource exists for marshmallow validation."""

from api.models import Center, RequestType
from .validate_id import is_valid_id
from ..error import raise_error


def resource_exists(resource_id, resource_type=None):
    """Validator to check whether a resource id is valid and exists

    Args:
        resource_id (str): The resource id to verify
        resource_type (str): The type of resource out of 'center'
         and 'request type' to be verified
    Raises:
        ValidationError: If the resource_id is invalid or does not exist
    """
    if not is_valid_id(resource_id):
        raise_error('invalid_id_field')

    the_resource = RequestType if resource_type == 'request type' else Center
    resource_name = 'Request type' if resource_type == 'request type' else 'Center'

    if not the_resource.exists(resource_id):
        raise_error('not_found', resource_name)


def request_type_exists(resource_id):
    return resource_exists(resource_id, 'request type')
