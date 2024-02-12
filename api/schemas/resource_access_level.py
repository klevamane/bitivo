""" Module for the resources access level model schema """

# Third party
from marshmallow import (fields, post_load, pre_load, ValidationError,
                         validates_schema, validates)

# Models
from api.models import ResourceAccessLevel, Permission

# Schemas
from .base_schemas import BaseSchema

# Error messages
from ..utilities.messages.error_messages import serialization_errors

# Validators
from ..utilities.validators.validate_id import id_validator
from ..utilities.validators.permission_validator import validate_permission
from ..utilities.validators.resource_role_validator import validate_resource_exists
from ..utilities.validators.duplicate_validator import validate_duplicate

# Helpers
from ..utilities.helpers.schemas import common_args


class ResourceAccessLevelSchema(BaseSchema):
    """Resource model schema"""

    id = fields.String()

    resource_id = fields.String(
        **common_args(validate=id_validator),
        load_from='resourceId',
        load_only=True)

    resource = fields.Nested(
        'ResourceSchema',
        only=['id', 'name'],
    )

    permissions = fields.Nested(
        'PermissionSchema', only=['id', 'type'], many=True)

    role_id = fields.String(
        load_from='roleId',
        load_only=True,
        error_messages={'required': serialization_errors['field_required']},
        validate=id_validator)

    permission_ids = fields.List(
        fields.Str(), load_from='permissionIds', load_only=True)

    @pre_load
    def validate_input_data(self, resource_access_level):
        """
        This function validates that the input to the schema is an dictionary or an object

        Args:
            resource_access_level (dict): A python dictionary

        Raises:
            ValidationError if resource_access_level is not a dictionary
        """
        if not isinstance(resource_access_level, dict):
            raise ValidationError(
                serialization_errors['invalid_resource_access_levels'],
                {'resourceAccessLevels': str(resource_access_level)})

    @validates_schema
    def validate_resource_exists(self, data):
        """Validates schema

        Args:
            self (ResourceAccessLevelSchema): instance of access level schema
            data (dict): partially cleaned data from the schema
        """

        validate_resource_exists(data,
                                 self.context.get('resource_ids_set', set()))

    @post_load
    def validate_resources_access_level(self, data):
        """
        Validate that you are not duplicating an access level
        for a resource on a given role

        Args:
            self (ResourceAccessLevelSchema): instance of access level schema
            data (dict): partially cleaned data from the schema
        """
        if data.get('role_id') and data.get('resource_id'):
            validate_duplicate(
                ResourceAccessLevel,
                role_id=data.get('role_id'),
                resource_id=data.get('resource_id'),
            )

    @post_load
    def add_no_access_to_empty_permission_list(self, data):
        """
        Add a No Access permission id to an empty permission id list

        Args:
            self (ResourceAccessLevelSchema): instance of access level schema
            data (dict): partially cleaned data from the schema
        """
        permission_ids = data.get('permission_ids')
        if permission_ids == []:
            no_access_permission_id = Permission.query.filter_by(
                type='No Access').first().id
            data['permission_ids'].append(no_access_permission_id)

    @validates('permission_ids')
    def permission_validator(self, permission_ids_list):
        """
        Function to call permission validator with context 

        Args:
            permission_ids_list (list): A list containing permission ids.

        """
        request = self.context.get('request')
        method = request.method if request else None
        validate_permission(permission_ids_list, method)
