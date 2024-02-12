from datetime import date

# Third party validate_schema
from marshmallow import fields
from marshmallow_enum import EnumField
from marshmallow import fields

# Helpers
from api.schemas.asset import AssetSchema
from api.utilities.validators.asset_validator import validate_asset_id

# Schemas
from .base_schemas import AuditableBaseSchema

# Custom validators
from ..utilities.validators.name_validator import name_validator
from ..utilities.validators.string_length_validators import string_length_validator, empty_string_validator
from ..utilities.validators.validate_id import id_validator
from ..utilities.constants import EXCLUDED_FIELDS

# Utilities
from api.utilities.helpers.schemas import common_args


class AssetInsuranceSchema(AuditableBaseSchema):
    """ Schema for asset insurance model"""
    company = fields.String(**common_args(validate=[
        string_length_validator(250), empty_string_validator, name_validator
    ]))
    start_date = fields.Date(
        **common_args(), dump_to="startDate", load_from="startDate")
    end_date = fields.Date(
        **common_args(), dump_to="endDate", load_from="endDate")
    asset_id = fields.String(
        load_only=True,
        load_from="assetId",
        **common_args(validate=[id_validator, validate_asset_id]))
    asset = fields.Nested(AssetSchema(exclude=EXCLUDED_FIELDS))
    status = fields.Function(lambda obj: 'active'
                             if obj.end_date >= date.today() else 'expired')
