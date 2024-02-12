"""Module for role schema"""

# Third party
from marshmallow import fields, post_load, pre_load, ValidationError

# Models
from ..models import Role

# Helpers
from ..utilities.helpers.role_endpoint import update_resource_access_levels
from ..utilities.helpers.schemas import common_args

# Schemas
from .base_schemas import AuditableBaseSchema
from ..schemas.resource_access_level import ResourceAccessLevelSchema

# Validators
from ..utilities.validators.name_validator import name_validator
from ..utilities.validators.string_length_validators import string_length_validator
from ..utilities.validators.duplicate_validator import validate_duplicate, title_case_and_validate

# Error messages
from ..utilities.messages.error_messages import serialization_errors


class RoleSchema(AuditableBaseSchema):
    """
    Role model schema
    """
    input_data = None

    id = fields.String()

    title = fields.String(**common_args(
        validate=[string_length_validator(60), name_validator]))

    description = fields.String(**common_args(
        validate=[string_length_validator(250), name_validator]))

    resource_access_levels = fields.Nested(
        'ResourceAccessLevelSchema',
        dump_to='resourceAccessLevels',
        only=['resource', 'permissions'],
        dump_only=True,
        many=True)

    user_count = fields.Integer(dump_to='userCount', dump_only=True)
    super_user = fields.Boolean(
        dump_to='SuperUser', load_from='SuperUser', required=False)

    @pre_load
    def format_input_data(self, data):
        RoleSchema.input_data = data

    @post_load
    def validate_output_data(self, data):
        """
        Check if a role with the specified title already exists in the Database
        and validate the resourceAccessLevels data

        Args:
            data (dict): partially cleaned data from the schema
        """
        title_case_and_validate(Role, 'title', data)
        self.create_resource_access_levels(data)

    def create_resource_access_levels(self, data):
        """Create resource access access levels
        
        Args:
            data (dict): partially cleaned data from the schema
        """
        input_data = RoleSchema.input_data
        RoleSchema.validated_resource_access_levels = []

        is_resource_access_levels_present = lambda: 'resourceAccessLevels' in input_data
        resource_access_levels = input_data.get('resourceAccessLevels')

        is_resource_access_levels_not_a_list = is_resource_access_levels_present(
        ) and not isinstance(resource_access_levels, list)

        validate_resource_access_levels_is_list(
            is_resource_access_levels_not_a_list)

        if is_resource_access_levels_present() and resource_access_levels:
            resource_access_levels = ResourceAccessLevelSchema(
                many=True,
                context={
                    'resource_ids_set': set(
                    ),  # passing set() to the schema to store unique resource id for validation
                    'request': self.context.get('request')
                }).load_object_into_schema(input_data['resourceAccessLevels'])

            if data.get('id'):
                update_resource_access_levels(data['id'],
                                              resource_access_levels)

            RoleSchema.validated_resource_access_levels = resource_access_levels

        elif is_resource_access_levels_present(
        ) and not resource_access_levels:
            raise ValidationError(serialization_errors['not_empty'],
                                  'resourceAccessLevels')


def validate_resource_access_levels_is_list(
        is_resource_access_levels_not_a_list):
    """Check that if the resource_access_level provided is a list.

    Args:
        is_resource_access_levels_not_a_list (bool): value to check if list

    Raises:
        ValidationError (Exception): A marshmallow exception
    """
    if is_resource_access_levels_not_a_list:
        raise ValidationError(
            serialization_errors['invalid_resource_access_levels_list'],
            'resourceAccessLevels')
