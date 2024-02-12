"""Module for space schema"""

# Third party libraries
from marshmallow import fields, pre_load, pre_dump

# Schemas
from .space_type import SpaceTypeSchema
from .base_schemas import AuditableBaseSchema

# Validators
from ..utilities.validators.name_validator import name_validator
from ..utilities.validators.string_length_validators import string_length_validator
from ..utilities.validators.validate_id import id_validator

# Messages
from ..utilities.messages.error_messages import serialization_errors

# Helpers
from ..utilities.helpers.schemas import common_args


class SpaceSchema(AuditableBaseSchema):
    """
    Space model schema
    """
    name = fields.String(**common_args(
        validate=(string_length_validator(60), name_validator)))

    parent_id = fields.String(
        load_from='parentId',
        dump_to='parentId',
        validate=id_validator,
        error_messages={'required': serialization_errors['field_required']})

    space_type_id = fields.String(
        load_from='spaceTypeId',
        load_only=True,
        **common_args(validate=id_validator))

    center_id = fields.String(
        load_from='centerId',
        dump_to='centerId',
        **common_args(validate=id_validator))

    space_type = fields.Nested(
        SpaceTypeSchema,
        dump_only=True,
        dump_to="spaceType",
        only=['id', 'type', 'color'])

    children_count = fields.Integer(dump_only=True, dump_to='childrenCount')

    @pre_load
    def strip_and_capitalize_name(self, data):
        """Strip and capitalize all lower case name

        Args:
            data (dict): the request data
        """

        if 'name' not in data:
            return

        name = data['name'].strip()

        if name.islower():
            name = name.title()

        data['name'] = name
