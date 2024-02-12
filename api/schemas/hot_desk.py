"""Module for HotDeskRequest model schema"""

# Third party libraries
from marshmallow import fields, pre_load
from marshmallow_enum import EnumField

# Utilities
from api.utilities.helpers.schemas import common_args
from ..utilities.messages.error_messages import serialization_errors

# Schemas
from .base_schemas import AuditableBaseSchema
from ..schemas.user import UserSchema
from ..schemas.history import HistorySchema

# Validators
from ..utilities.validators.allocation_validators import validate_assignee_id, validate_requester_id
from ..utilities.validators.status_validator import validate_hot_desk_status
from ..utilities.validators.string_length_validators import empty_string_validator, string_length_validator, \
    min_length_validator
from ..utilities.validators.name_validator import name_validator

# Helpers
from ..utilities.helpers.remove_whitespace import remove_whitespace
from ..utilities.helpers.schemas import common_args

# Enum
from ..utilities.enums import HotDeskRequestStatusEnum
from ..utilities.constants import USER_SCHEMA_FIELDS

# model
from api.models import User
from ..models.history import History


class HotDeskRequestSchema(AuditableBaseSchema):
    """Schema for HotDeskRequest model"""
    requester_id = fields.String(**common_args(validate=validate_requester_id))
    status = EnumField(
        HotDeskRequestStatusEnum,
        load_by=EnumField.VALUE,
        dump_by=EnumField.VALUE,
        error=serialization_errors['invalid_hot_desk_status'],
        **common_args(validate=validate_hot_desk_status))
    hot_desk_ref_no = fields.String(
        **common_args(validate=empty_string_validator, ),
        dump_to='hotDeskRefNo')
    assignee_id = fields.String(
        load_from='assigneeId',
        **common_args(validate=validate_assignee_id),
        load_only=True)
    requester = fields.Method('get_requester')
    created_at = fields.Date(dump_to='lastRequestDate'),
    count = fields.Integer(dump_to='requestsCount')
    reason = fields.String(validate=(string_length_validator(100)))
    complaint = fields.String()
    complaint_created_at = fields.Date(dump_to='complaintCreatedAt')
    approver = fields.Method('get_approver')

    class Meta:
        """Make the output ordered"""
        ordered = True

    @pre_load
    def cleanup_data_field(self, data):
        """Remove whitespaces in data fields

        Args:
            data(json): the data to be deserialized

        """
        remove_whitespace(data, 'hot_desk_ref_no', data.get('hot_desk_ref_no'))

    def get_requester(self, obj):
        """Method that dumps the user schema into the hot_desk_schema
        Args (obj): The query row object
        Returns: Data to be dumped into the schema
        """
        user = User.get(obj.requester_id)
        return UserSchema(only=USER_SCHEMA_FIELDS).dump(user).data

    def get_approver(self, obj):
        """Method that dumps the approver data into the hot desk schema
        Args (obj): The query row object
        Returns: Data to be dumped into the schema
        """
        return UserSchema(only=USER_SCHEMA_FIELDS).dump(
            User.get(obj.assignee_id)).data


class UserHotDeskRequestSchema(HotDeskRequestSchema):
    """Schema extending HotDeskRequest schema for hot desk requests by a user"""
    updated_at = fields.Date(dump_to='updatedAt')

    class Meta:
        """Make the output ordered"""
        fields = ("id", "hot_desk_ref_no", "created_at", "updated_at",
                  "status")
        ordered = True


class HotDeskComplaintSchema(HotDeskRequestSchema):
    """Schema extending HotDeskRequestSchema schema for hot desk requests by a user"""

    complaint = fields.String(**common_args(validate=[
        string_length_validator(1000), min_length_validator,
        empty_string_validator
    ]))

class HotDeskRequestCancellationCountSchema(AuditableBaseSchema):
    """Schema for HotDeskRequest cancellation reasons counts"""
    change_my_mind_count = fields.Integer(dump_to='changeMyMind')
    leaving_early_count = fields.Integer(dump_to='leavingEarly')
    delayed_approval_count = fields.Integer(dump_to='delayedApproval')
    seat_changed_count = fields.Integer(dump_to='seatChanged')
    other_count = fields.Integer(dump_to='others')


class ResponderHotdeskCountSchema(HotDeskRequestSchema):
    """Schema for HotDeskRequest model to get assignee response counts"""
    approvals_count = fields.Integer(dump_to='approvalsCount')
    rejections_count = fields.Integer(dump_to='rejectionsCount')
    missed_count = fields.Integer(dump_to='missedCount')
    approver = fields.Method('get_approver', dump_to='assignee')


class CancelHotDeskRequestSchema(HotDeskRequestSchema):
    """Schema extending HotDeskRequest schema for hot desk requests by a user"""
    reason = fields.String(
        **common_args(validate=[string_length_validator(100), name_validator]))


class HotDeskRequestHistorySchema(HotDeskRequestSchema):
    """Schema extending HotDeskRequestSchema schema for getting hotdesk activity log"""
    history = fields.Method('get_activity')

    def get_activity(self, obj):
        """Method that dumps the activity log data for a hotdesk
        into the hot desk schema
        Args (obj): The query row object
        Returns: Data to be dumped into the schema
        """
        return HistorySchema(many=True).dump(History.query.filter_by(
            resource_id=obj.id).order_by(History.created_at.asc()).all()).data
