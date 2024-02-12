# Third party libraries
from marshmallow import fields, post_load, pre_load

# models
from ..models.user import User

# Schemas
from .base_schemas import AuditableBaseSchema
from .user import UserSchema

# Custom error messages
# Custom errors
from ..utilities.messages.error_messages import serialization_errors

# Custom validators
from ..utilities.validators.name_validator import name_validator
from ..utilities.validators.string_length_validators import string_length_validator
from ..utilities.validators.allocation_validators import validate_assignee_id
from ..utilities.validators.resource_exists_validator import resource_exists
from ..utilities.validators.validate_id import id_validator
from ..utilities.validators.request_types_validator import (
    validate_request_types_date, validate_user_a_member_of_center,
    validate_request_type_exist_in_center)
from ..utilities.constants import USER_SCHEMA_FIELDS, REQUEST_TYPE_TIME_FIELDS


class RequestTypeSchema(AuditableBaseSchema):
    """ Schema for request type model"""

    title = fields.String(
        required=True,
        validate=[string_length_validator(60), name_validator],
        error_messages={'required': serialization_errors['field_required']})

    center_id = fields.String(
        required=True,
        dump_to="centerId",
        load_from="centerId",
        validate=[id_validator, resource_exists],
        error_messages={'required': serialization_errors['field_required']})

    response_time = fields.Dict(
        required=True,
        dump_to="responseTime",
        error_messages={'required': serialization_errors['field_required']},
        load_from="responseTime")

    resolution_time = fields.Dict(
        load_from="resolutionTime",
        required=True,
        dump_to="resolutionTime",
        error_messages={'required': serialization_errors['field_required']})

    closure_time = fields.Dict(
        dump_to="closureTime",
        required=True,
        error_messages={'required': serialization_errors['field_required']},
        load_from="closureTime")

    assignee_id = fields.String(
        error_messages={'required': serialization_errors['field_required']},
        load_from="assigneeId",
        validate=validate_assignee_id,
        required=True,
        load_only=True)

    assignee = fields.Nested(
        UserSchema, only=USER_SCHEMA_FIELDS, dump_only=True)

    requests_count = fields.Integer(dump_to='requestsCount', dump_only=True)

    class Meta:
        ordered = True

    @pre_load
    def validate_time_field(self, data):
        """Validates closureTime, responseTime and resolutionTime fields

        Args:
            data (dict): The request data
        """

        for key in REQUEST_TYPE_TIME_FIELDS:
            new_value = validate_request_types_date(data.get(key), key)
            if new_value:
                data[key] = new_value

        return data

    @pre_load
    def remove_whitespaces(self, data):
        if data.get('title'):
            data['title'] = " ".join(data['title'].split())
            return data

    @post_load
    def validate(self, data):
        """Validates that the user is a member of the specified center

        Check if the request type exist in the specified center

        Args:
            data (dict): The request data
        """
        validate_user_a_member_of_center(data)
        validate_request_type_exist_in_center(
            data, self.context.get('request_type_id'))
