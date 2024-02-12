""" Module for permission schema. """

# Third party Libraries
from marshmallow import fields
from marshmallow_enum import EnumField

# Enums
from ..utilities.enums import ParentType

# Helpers
from ..utilities.helpers.schemas import common_args

# Error messages
from ..utilities.messages.error_messages import serialization_errors

# Validators
from ..utilities.validators.allocation_validators import validate_assignee_id
from ..utilities.validators.string_length_validators import empty_string_validator
from ..utilities.validators.validate_id import id_validator

# Schema
from .base_schemas import AuditableBaseSchema
from .user import UserSchema


class CommentSchema(AuditableBaseSchema):
    """ Comment model schema."""

    body = fields.String(**common_args(validate=empty_string_validator))
    parent_id = fields.String(
        **common_args(validate=(id_validator)),
        dump_to="parentId",
        load_from='parentId')
    parent_type = EnumField(
        ParentType,
        load_by=EnumField.VALUE,
        dump_by=EnumField.VALUE,
        load_from='parentType',
        dump_to='parentType',
        error='Please provide one of {values}')
    author_id = fields.String(
        **common_args(validate=validate_assignee_id),
        load_from='authorId',
        load_only=True)
    deleted = fields.Boolean(dump_to="deleted", dump_only=True)
    author = fields.Nested(
        UserSchema,
        only=[
            'email', 'name', 'token_id', 'role.id', 'role.title',
            'role.description', 'image_url'
        ],
        dump_only=True)
