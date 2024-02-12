# Third party validate_schema
from marshmallow import fields
from marshmallow_enum import EnumField
from marshmallow import fields, post_load, pre_load
from flask import request

# Helpers
from ..utilities.helpers.schemas import common_args

# Schemas
from .request_type import RequestTypeSchema
from .base_schemas import AuditableBaseSchema
from .user import UserSchema
from .comment import CommentSchema

# Enums
from ..utilities.enums import RequestStatusEnum

# Custom errors
from ..utilities.messages.error_messages import serialization_errors

# Custom validators
from ..utilities.validators.name_validator import name_validator
from ..utilities.validators.string_length_validators import string_length_validator, empty_string_validator
from ..utilities.validators.validate_id import id_validator
from ..utilities.validators.resource_exists_validator import (resource_exists,
                                                    request_type_exists)
from ..utilities.validators.request_validators import (
    validate_requester_and_request_type_as_member_of_center,
    check_requester_id_exists, validate_requester_is_not_responder,
    remove_whitespaces)
from ..utilities.constants import USER_SCHEMA_FIELDS

# Utilities
from ..utilities.json_parse_objects import json_parse_objects
from api.utilities.helpers.schemas import common_args

from ..utilities.enums import RequestStatusEnum


class RequestSchema(AuditableBaseSchema):
    """ Schema for request model"""

    serial_number = fields.Integer(dump_to="serialNumber")

    subject = fields.String(**common_args(validate=[
        string_length_validator(60), empty_string_validator, name_validator
    ]))

    request_type_id = fields.String(
        load_only=True,
        load_from="requestTypeId",
        **common_args(validate=[id_validator, request_type_exists]))

    request_type = fields.Nested(
        RequestTypeSchema,
        only=[
            'id', 'title', 'center_id', 'assignee', 'response_time',
            'resolution_time', 'closure_time'
        ],
        dump_only=True,
        dump_to="requestType")

    center_id = fields.String(
        **common_args(validate=resource_exists),
        dump_to="centerId",
        load_from="centerId")

    description = fields.String(**common_args(
        validate=[string_length_validator(1000), empty_string_validator]))

    attachments = fields.Method('json_load_attachments', )

    requester_id = fields.String(
        **common_args(validate=[id_validator, check_requester_id_exists]),
        load_from="requesterId",
        load_only=True)

    assignee_id = fields.String(
        load_from="assigneeId", validate=id_validator, load_only=True)

    requester = fields.Nested(
        UserSchema, only=USER_SCHEMA_FIELDS, dump_only=True)

    responder = fields.Nested(
        UserSchema, only=USER_SCHEMA_FIELDS, dump_only=True)

    assignee = fields.Nested(
        UserSchema, only=USER_SCHEMA_FIELDS, dump_only=True)

    status = EnumField(
        RequestStatusEnum,
        load_by=EnumField.VALUE,
        dump_by=EnumField.VALUE,
        error='Please provide one of {values}')

    closed_by_system = fields.Boolean(dump_to="closedBySystem")

    in_progress_at = fields.DateTime(dump_to="inProgressAt")

    completed_at = fields.DateTime(dump_to="completedAt")

    closed_at = fields.DateTime(dump_to="closedAt")

    due_by = fields.DateTime(dump_to="dueBy")

    def json_load_attachments(self, obj):
        if obj.attachments is None:
            obj.attachments = []
        return json_parse_objects(obj.attachments, 'loads')

    @pre_load
    def pre_load_validator(self, data):
        """Validates fields before loading
        Args:
            data (dict): The data to be validated
        """
        remove_whitespaces(data)

    @post_load
    def validator(self, data):
        """Validates that the requester is a member of the specified center

        Args:
            data (dict): The request data
        """
        if request.method == 'POST':
            validate_requester_and_request_type_as_member_of_center(data)
            validate_requester_is_not_responder(data)


class EagerLoadRequestSchema(RequestSchema):
    """Schema for Request with eager loaded comments"""

    comments = fields.Method('get_comments')

    def get_comments(self, obj):
        """Get serialized eager loaded comments

        Args:
             obj (class): an instance of the request class
        Returns:
             (dict): the comments of a request
        """

        return CommentSchema(many=True).dump(obj.comments).data
