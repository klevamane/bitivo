# Third party
from marshmallow import ValidationError

# Models
from ...models.permission import Permission

# Middlewares
from ...middlewares.base_validator import ValidationError as BaseValidationError

# Validators
from .validate_id import id_validator

# Messages
from ..messages.error_messages import database_errors, serialization_errors


def validate_permission(permission_ids_list, method):
    """
    Helper function to validate permission id

    Args:
        permission_ids_list (list): A list containing permission ids.

    Raises:
        ValidationError if: 1) the permission ids are invalid. 2) Duplicated
        permission ids are found in the list. 3) Full access permission is
        supplied with any other extra permission(s)
    """
    permissions_set = set(permission_ids_list)
    if method == 'POST':
        validate_empty_list(permissions_set)

    for permission_id in permissions_set:
        id_validator(permission_id)

        permission_obj = Permission.get(permission_id)

        if not permission_obj:
            raise ValidationError(
                database_errors['non_existing'].format('Permission'))

        validate_full_access_single_list(permission_obj, permission_ids_list)


def validate_full_access_single_list(permission_obj, permissions_list):
    """
    Validates that when a full access permission is supplied, it's the only
    permission in the list

    Args:
        permission_obj (Permission): An instance of Permission class
        permissions_list (list): A list containing permission Ids

    Raises:
        ValidationError if the permission_object type is Full Access the length
        of permissions_list is more than one.

    """

    if permission_obj.type == 'Full Access' and len(permissions_list) > 1:
        raise ValidationError(serialization_errors['single_permission'].format(
            permission_obj.type))


def validate_empty_list(permission_set):
    """
     Validates if the permission list is empty

    Args:
        permission_set(set): set created from the permision list
    """
    if not permission_set:
        raise ValidationError(
            serialization_errors["cannot_be_empty"].format("permissions"))
