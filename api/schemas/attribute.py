""" Module for Attribute model serialization schema. """

# Third party libraries
from marshmallow import (fields, post_load, post_dump,
                         validates_schema)
from humps.camel import case

# Models
from api.models.attribute import Attribute

# Schema
from .base_schemas import BaseSchema

# Validators
from ..utilities.validators.validate_id import id_validator
from ..utilities.validators.name_validator import name_validator
from ..utilities.validators.string_length_validators import string_length_validator
from ..utilities.validators.input_control_validator import input_control_validation
from ..utilities.validators.attributes_validator import (
    validate_choices, validate_choices_after_dump)

# Helpers
from  ..utilities.helpers.schemas import common_args

# Messages
from ..utilities.messages.error_messages import serialization_errors


class AttributeSchema(BaseSchema):
    """Attribute model schema"""

    _key = fields.String(load_from='label', dump_to='key')
    id = fields.String(validate=id_validator)

    label = fields.String(**common_args(validate=(string_length_validator(60), name_validator)))
    is_required = fields.Boolean(
        required=True,
        load_from='isRequired',
        dump_to='isRequired',
        error_messages={'required': serialization_errors['field_required']})
    input_control = fields.String(
        **common_args(validate=(string_length_validator(60), name_validator,
                                input_control_validation)),
        load_from='inputControl',
        dump_to='inputControl')
    choices = fields.List(fields.String(validate=string_length_validator(60)))
    default = fields.Boolean(required=False)

    @validates_schema
    def validate_choice_decorator(self, data):
        return validate_choices(data)

    @post_load
    def create_attribute(self, data):
        """Return attribute object after successful loading into schema"""

        # When updating, `label` may not be provided in request's body.
        if data.get('_key'):
            data['_key'] = case(data['_key'])

        if not data.get('id'):
            return Attribute(**data)
        return data

    @post_dump
    def dump_attribute(self, data):
        """
        Return attribute object after successful dumping as array of strings
        """
        return validate_choices_after_dump(data)
