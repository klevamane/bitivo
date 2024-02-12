""" Module for assets repair log model schema. """
# Third party libraries
from marshmallow import fields

# Models
from marshmallow_enum import EnumField

from .asset import AssetSchema
from .base_schemas import AuditableBaseSchema
from .user import UserSchema
# Helpers
from ..utilities.constants import USER_SCHEMA_FIELDS, EXCLUDED_FIELDS
from ..utilities.enums import RepairLogStatusEnum
from ..utilities.helpers.schemas import common_args

# Validators
from ..utilities.validators.allocation_validators import (
    validate_assignee_id, validate_complainant_id)
from ..utilities.validators.asset_validator import validate_asset_id
from ..utilities.validators.string_length_validators import (
    string_length_validator, empty_string_validator, min_length_validator)

# Error Messages
from ..utilities.messages.error_messages import serialization_errors


class AssetRepairLogSchema(AuditableBaseSchema):
    """Schema for AssetsRepairLog model"""

    issue_description = fields.String(
        load_from='issueDescription',
        dump_to='issueDescription',
        **common_args(validate=[
            empty_string_validator, min_length_validator,
            string_length_validator(1000)
        ]))
    repairer = fields.String(
        load_from='repairer',
        dump_to='repairer',
        **common_args(
            validate=[empty_string_validator,
                      string_length_validator(50)]))
    asset_id = fields.String(
        load_from="assetId",
        load_only=True,
        **common_args(validate=[
            empty_string_validator,
            string_length_validator(60), validate_asset_id
        ]))
    date_reported = fields.Date(
        error_messages={'required': serialization_errors['field_required']},
        required=True,
        load_from='dateReported',
        dump_to='dateReported')
    expected_return_date = fields.Date(
        required=True,
        error_messages={'required': serialization_errors['field_required']},
        load_from='expectedReturnDate',
        dump_to='expectedReturnDate')

    defect_type = fields.String(
        dump_to='defectType',
        load_from='defectType',
        **common_args(
            validate=[empty_string_validator,
                      string_length_validator(100)]))

    status = EnumField(
        RepairLogStatusEnum,
        load_by=EnumField.VALUE,
        dump_by=EnumField.VALUE,
        error=serialization_errors['invalid_enum_value'])
    asset = fields.Nested(AssetSchema, exclude=EXCLUDED_FIELDS, dump_only=True)
