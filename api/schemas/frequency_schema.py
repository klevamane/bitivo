"""Module for custom occureence field schema"""
import json
# Third party libraries
from marshmallow import fields, validate, Schema, ValidationError
from marshmallow_enum import EnumField

# Utilities
from api.utilities.helpers.schemas import common_args, validate_ends_field

# Schemas
from .base_schemas import BaseSchema

# Enums
from ..utilities.enums import CustomFrequencyEnum

# Common validators
from ..utilities.helpers.schemas import validate_repeat_days


class CustomOccurrence(fields.Field):
    """ Custom Occurrence fileds that deserializes to a Custom Occurrence Object."""

    def _deserialize(self, value, *args, **kwargs):
        """ Deserialize custom occurence schema value passed. """
        custom_schema = CustomOccurrenceSchema()
        if custom_schema.load(value).errors:
            raise ValidationError(custom_schema.load(value).errors)
        return value


class EndsSchema(BaseSchema):
    """ Schema for end field field in custom occurrence."""
    on = fields.Date()
    never = fields.Bool()
    after = fields.Integer(
        validate=[validate.Range(min=1, error="Value must be greater than 0")])


class CustomOccurrenceSchema(Schema):
    """ Schema for Custom Occurrence fields. """
    repeat_days = fields.List(
        fields.String(), required=True, validate=validate_repeat_days)
    repeat_units = fields.Integer(
        validate=[validate.Range(min=1, error="Value must be greater than 0")])
    repeat_frequency = EnumField(
        CustomFrequencyEnum,
        load_by=EnumField.VALUE,
        dump_by=EnumField.VALUE,
        error='Please provide one of {values}',
        required=True)
    ends = fields.Nested(EndsSchema, validate=validate_ends_field)
