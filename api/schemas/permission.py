"""Module for permission schema"""
# Third-party libraries
from marshmallow import fields, post_load

# Models
from api.models.permission import Permission

# Schema
from .base_schemas import AuditableBaseSchema

# Validators
from ..utilities.validators.name_validator import name_validator
from ..utilities.validators.string_length_validators import string_length_validator
from ..utilities.validators.duplicate_validator import validate_duplicate

# Helpers
from ..utilities.helpers.schemas import common_args


class PermissionSchema(AuditableBaseSchema):
    """
    Permission model schema
    """
    type = fields.String(**common_args(validate=[string_length_validator(60), name_validator]))

    @post_load
    def validate_type(self, data):
        """
        Validate duplicate permission
        """
        if data.get('type'):
            data['type'] = data['type'].title()
            validate_duplicate(Permission, type=data.get('type'))
