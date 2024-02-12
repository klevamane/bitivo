# Third party libraries
from marshmallow import fields
from marshmallow_enum import EnumField

# Schemas
from .base_schemas import AuditableBaseSchema
from .user import UserSchema
from .comment import CommentSchema
from .work_order import WorkOrderSchema

# Utilities
from api.utilities.helpers.schemas import common_args
from ..utilities.json_parse_objects import json_parse_objects

# Enum
from ..utilities.enums import ScheduleStatusEnum

# Custom validators
from ..utilities.validators.allocation_validators import validate_assignee_id
from ..utilities.constants import USER_SCHEMA_FIELDS

# Messages
from ..utilities.messages.error_messages import serialization_errors


class ScheduleSchema(AuditableBaseSchema):
    """
    Schema for schedule model
    """

    assignee_id = fields.String(
        load_from="assigneeId", validate=validate_assignee_id, load_only=True)

    assignee = fields.Nested(
        UserSchema, only=USER_SCHEMA_FIELDS, dump_only=True)

    status = EnumField(
        ScheduleStatusEnum,
        load_by=EnumField.VALUE,
        dump_by=EnumField.VALUE,
        error=serialization_errors['invalid_enum_value'],
        **common_args())
    attachments = fields.Method('load_json_attachments', )

    work_order_id = fields.String(dump_only=True, dump_to="workOrderId")
    work_order = fields.Nested(
        WorkOrderSchema,
        only=[
            'created_by', 'maintenance_category', 'description',
            'custom_occurrence', 'title', 'frequency', 'id', 'status',
            'assignee'
        ],
        dump_only=True,
        dump_to="workOrder")

    due_date = fields.DateTime(dump_to="dueDate")

    def load_json_attachments(self, obj):
        if obj.attachments is None:
            obj.attachments = []
        return json_parse_objects(obj.attachments, 'loads')


class EagerLoadScheduleSchema(ScheduleSchema):
    """Schema for Schedule with eager loaded comments"""

    comments = fields.Method('get_comments')

    def get_comments(self, obj):
        """Get serialized eager loaded comments

        Args:
             obj (class): an instance of the schedule class
        Returns:
             (dict): the comments of a schedule
        """

        return CommentSchema(many=True).dump(obj.comments).data