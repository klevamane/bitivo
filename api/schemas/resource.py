""" Module for the resource model schema """
# Third party libraries
from marshmallow import fields, post_load

# Models
from api.models.resource import Resource

# Schema
from .base_schemas import BaseSchema

# Validators
from ..utilities.validators.name_validator import name_validator
from ..utilities.validators.string_length_validators import string_length_validator
from ..utilities.validators.duplicate_validator import validate_duplicate

# Helpers
from ..utilities.helpers.schemas import common_args


class ResourceSchema(BaseSchema):
    """Resource model schema"""
    id = fields.String()
    name = fields.String(**common_args(
        validate=(string_length_validator(60), name_validator)))

    @post_load
    def validate_resource(self, data):
        """Validate resource name is not a duplicate"""
        if data.get('name'):
            validate_duplicate(
                Resource, name=data.get('name'), id=data.get('id'))
