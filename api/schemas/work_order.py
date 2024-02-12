"""Module for work_order model schema"""

# Third party libraries
import json

from marshmallow import fields, pre_load, post_load
from marshmallow_enum import EnumField

# Utilities
from api.utilities.helpers.schemas import common_args, date_args
from ..utilities.messages.error_messages import serialization_errors

# work order model
from api.models import WorkOrder

# Schemas
from api.schemas.maintenance_categories import MaintenanceCategorySchema
from .base_schemas import AuditableBaseSchema, BaseSchema
from .user import UserSchema
from ..schemas.frequency_schema import CustomOccurrence

# Enums
from ..utilities.enums import FrequencyEnum, StatusEnum

# Custom validators
from ..utilities.validators.string_length_validators import string_length_validator, empty_string_validator
from ..utilities.validators.validate_id import id_validator
from ..utilities.validators.name_validator import name_validator
from ..utilities.validators.allocation_validators import validate_assignee_id
from ..utilities.validators.work_order_validators import (
    validate_title_duplicate, validate_work_order_dates,
    maintenance_category_exists)

# Helpers
from ..utilities.helpers.remove_whitespace import remove_whitespace

# constants
from ..utilities.constants import USER_SCHEMA_FIELDS


class WorkOrderSchema(AuditableBaseSchema):
    """Schema for work_order model"""

    title = fields.String(**common_args(
        validate=[string_length_validator(60), name_validator]))

    description = fields.String(
        **common_args(validate=empty_string_validator, ))

    assignee = fields.Nested(
        UserSchema, only=USER_SCHEMA_FIELDS, dump_only=True)

    maintenance_category = fields.Nested(
        MaintenanceCategorySchema,
        dump_only=True,
        only=['id', 'title', 'asset_category', 'center'],
        dump_to="maintenanceCategory")

    maintenance_category_id = fields.String(
        load_from="maintenanceCategoryId",
        dump_to="maintenanceCategoryId",
        load_only=True,
        **common_args(validate=[id_validator, maintenance_category_exists]))

    assignee_id = fields.String(
        load_from="assigneeId",
        load_only=True,
        **common_args(validate=validate_assignee_id))

    custom_occurrence = CustomOccurrence(
        load_from="customOccurrence", dump_to="customOccurrence")
    frequency = EnumField(
        FrequencyEnum,
        load_by=EnumField.VALUE,
        dump_by=EnumField.VALUE,
        error='Please provide one of {values}',
        load_from="frequency",
        dump_to="frequency",
        **common_args())

    status = EnumField(
        StatusEnum,
        load_from="status",
        dump_to="status",
        error='Please provide {values}')

    start_date = fields.DateTime(
        dump_to="startDate",
        load_from="startDate",
        **date_args(value="startDate"))

    end_date = fields.DateTime(
        dump_to="endDate", load_from="endDate", **date_args(value="endDate"))

    class Meta:
        """Make the output ordered"""

        ordered = True

    @pre_load
    def cleanup_data_field(self, data):
        """Remove whitespaces in data fields

        Args:
            data(json): the data to be deserialized
        """
        remove_whitespace(data, 'title', data.get('title'))
        remove_whitespace(data, 'description', data.get('description'))

    @pre_load
    def date_validation(self, data):
        """Validates the dates with desired time of the work order recieved

        Args:
            data (dict): This is a dictionary object of the work order data
            containing the start and end dates along with desired time.
        """
        start_date = data.get("startDate", self.context.get('start_date'))
        end_date = data.get("endDate", self.context.get('end_date'))
        if start_date and end_date:
            validate_work_order_dates(data, start_date, end_date)

    @post_load
    def validator_title(self, data):
        """This functions validates the work order title at the schema before it is
        saved to the datatbase

        Args:
            data (dict): This is a dictionary object of the work order data
        """
        work_order_id = self.context.get('work_order_id')

        validate_title_duplicate(WorkOrder, data, work_order_id)


class WorkOrderListSchema(BaseSchema):
    work_orders = fields.List(
        fields.Nested(WorkOrderSchema, exclude=['maintenance_category_id']),
        load_only=True)
