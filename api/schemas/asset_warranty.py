""" Module for assets repair log model schema. """
# Third party libraries
from marshmallow import fields

# Models
from marshmallow_enum import EnumField
from .asset import AssetSchema
from .base_schemas import AuditableBaseSchema

# Helpers
from ..utilities.enums import AssetWarrantyStatusEnum
from ..utilities.helpers.schemas import common_args, date_args
from ..utilities.constants import EXCLUDED_FIELDS

# Validators
from ..utilities.validators.allocation_validators import (
    validate_assignee_id, validate_complainant_id)
from ..utilities.validators.asset_validator import validate_asset_id
from ..utilities.validators.string_length_validators import (
    string_length_validator, empty_string_validator, min_length_validator)

# Error Messages
from ..utilities.messages.error_messages import serialization_errors


class AssetWarrantySchema(AuditableBaseSchema):
    """Schema for AssetsWarranty model"""

    asset_id = fields.String(
        load_only=True,
        load_from="assetId",
        **common_args(validate=[
            empty_string_validator,
            string_length_validator(60),
            validate_asset_id
        ])
    )
    status = EnumField(
        AssetWarrantyStatusEnum,
        load_by=EnumField.VALUE,
        dump_by=EnumField.VALUE,
        error=serialization_errors['invalid_enum_value'])
    start_date = fields.Date(
        dump_to="startDate",
        load_from="startDate",
        **date_args(value="startDate"))

    end_date = fields.Date(
        dump_to="endDate", load_from="endDate", **date_args(value="endDate"))
    asset = fields.Nested(AssetSchema(exclude=EXCLUDED_FIELDS))
