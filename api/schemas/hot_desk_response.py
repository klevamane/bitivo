""" Module for hot desk response schema """

# Third party libraries
from marshmallow import fields
from marshmallow_enum import EnumField

# Utilities
from api.utilities.helpers.schemas import common_args
from ..utilities.messages.error_messages import serialization_errors
from api.models import HotDeskRequest, User

# Validators
from ..utilities.validators.status_validator import validate_hot_desk_status
from ..utilities.validators.allocation_validators import validate_assignee_id
from ..utilities.validators.validate_id import id_validator
from ..utilities.constants import USER_SCHEMA_FIELDS

# Schemas
from .base_schemas import AuditableBaseSchema
from ..schemas.hot_desk import HotDeskRequestSchema
from ..schemas.user import UserSchema

# Enum
from ..utilities.enums import HotDeskResponseStatusEnum


class HotDeskResponseSchema(AuditableBaseSchema):
    """ Schema fro hot desk response model """

    status = EnumField(
        HotDeskResponseStatusEnum,
        load_by=EnumField.VALUE,
        dump_by=EnumField.VALUE,
        error=serialization_errors['invalid_hot_desk_status'],
        **common_args(validate=validate_hot_desk_status))
    assignee_id = fields.String(
        load_from='assigneeId', **common_args(validate=validate_assignee_id))
    hot_desk_request_id = fields.String(
        load_from='hotDeskRequestId', **common_args(validate=id_validator))
    seat_number = fields.Method('get_seat_number', dump_to='seatNumber')
    requester = fields.Method('get_requester')

    def get_seat_number(self, obj):
        """ Method to dump hot desk number in HotDeskResponseSchema
            args:
                (obj): Query row object
            returns:
                Seat number dumped into the HotDeskResponseSchema
        """
        hot_desk = HotDeskRequest.query_().filter_by(
            id=obj.hot_desk_request_id).first()
        return HotDeskRequestSchema(
            only=['hot_desk_ref_no']).dump(hot_desk).data['hotDeskRefNo']

    def get_requester(self, obj):
        """ Method to dump hot desk requester in HotDeskResponseSchema
            args:
                (obj): Query row object
            returns:
                requester details dumped into  the HotDeskResponseSchema
        """
        hot_desk = HotDeskRequest.query_().filter_by(
            id=obj.hot_desk_request_id).first()
        user = User.get(hot_desk.requester_id)
        return UserSchema(only=USER_SCHEMA_FIELDS).dump(user).data
