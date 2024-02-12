"""Module for center schema"""
# Third-party libraries
from marshmallow import fields, post_load

# Models
from api.models.center import Center

# Schemas
from .base_schemas import AuditableBaseSchema
from .user import UserSchema
from .space import SpaceSchema

# Validators
from ..utilities.validators.name_validator import name_validator
from ..utilities.validators.string_length_validators import string_length_validator
from ..utilities.validators.duplicate_validator import title_case_and_validate

# Messages
from ..utilities.messages.error_messages import serialization_errors

# Helpers
from ..utilities.helpers.schemas import common_args


class CenterSchema(AuditableBaseSchema):
    """
    Center model schema
    """
    id = fields.String()
    name = fields.String(**common_args(validate=[string_length_validator(60), name_validator]))
    image = fields.Dict(
        required=True,
        error_messages={'required': serialization_errors['field_required']})
    users = fields.Nested(
        UserSchema,
        only=['name', 'image_url', 'role_id'],
        dump_to='people',
        many=True)
    spaces = fields.Nested(
        SpaceSchema,
        only=['name', 'parent_id', 'space_type_id', 'center_id'],
        many=True
    )
    user_count = fields.Method('get_user_count', dump_to='staffCount')

    @post_load
    def convert_name(self, data):
        """Convert center name with the first letter capitalized"""
        title_case_and_validate(Center, 'name', data)

    def get_user_count(self, obj):
        return obj.user_count
