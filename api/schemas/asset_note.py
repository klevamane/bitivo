"""Module for Asset Note model schema"""

# Third party libraries
from marshmallow import fields

# Schemas
from .user import UserSchema
from .base_schemas import AuditableBaseSchema
from .asset import AssetSchema

# Models
from ..models import User

# Helpers
from ..utilities.helpers.schemas import common_args
from ..utilities.constants import EXCLUDED_FIELDS


# Validators
from ..utilities.validators.string_length_validators import string_length_validator, empty_string_validator
from ..utilities.validators.name_validator import name_validator
from ..utilities.validators.asset_validator import validate_asset_id


class AssetNoteSchema(AuditableBaseSchema):
    """ Schema for asset note schema """

    title = fields.String(
        **common_args(validate=(string_length_validator(100), name_validator)))
    body = fields.String(
        **common_args(validate=empty_string_validator))
    asset_id = fields.String(
        load_from='assetId',
        dump_to='assetId',
        load_only=True,
        **common_args(validate=[empty_string_validator, validate_asset_id])
    )
    asset = fields.Nested(AssetSchema(exclude=EXCLUDED_FIELDS))
    creator = fields.Method(
        'get_creator',
        dump_only=True)

    def get_creator(self, obj):
        excluded_user_attributes = [
            'deleted', 'center.user_count', 'role.resource_access_levels',
            'created_at', 'updated_at'
        ]
        excluded_user_attributes.extend(EXCLUDED_FIELDS)
        return UserSchema(
            exclude=excluded_user_attributes).dump(
            User.get_or_404(obj.created_by)).data
