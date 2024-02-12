"""Module for Support Document schema"""

# Third party
from marshmallow import fields
from marshmallow_enum import EnumField

# Helpers
from ..utilities.helpers.schemas import common_args
from ..utilities.enums import AssetSupportingDocumentTypeEnum
from ..utilities.constants import EXCLUDED_FIELDS

# Models
from ..models import User

# Schemas
from .base_schemas import AuditableBaseSchema
from .user import UserSchema

# Validators
from ..utilities.validators.asset_validator import validate_asset_id
from ..utilities.validators.asset_supporting_document_validator import validate_supporting_document_type
from ..utilities.validators.string_length_validators import string_length_validator, empty_string_validator


class AssetSupportingDocumentSchema(AuditableBaseSchema):
    """
    AssetSupportingDocument model schema
    """
    document_name = fields.String(
        load_from='documentName',
        dump_to='documentName',
        **common_args(
        validate=[
            string_length_validator(60),
            empty_string_validator
        ]))
    asset_id = fields.String(
        load_from='assetId',
        dump_to='assetId',
        validate=validate_asset_id,
        load_only=True)
    document_type = EnumField(
        AssetSupportingDocumentTypeEnum,
        load_by=EnumField.VALUE,
        dump_by=EnumField.VALUE,
        load_from='documentType',
        dump_to='documentType',
        **common_args(validate=[validate_supporting_document_type]))
    document = fields.Dict(keys=fields.Str(), values=fields.Str())
    creator = fields.Method(
        'get_creator',
        dump_only=True)

    def get_creator(self, obj):
        """
        Method to get the user that uploaded the asset
        supporting document
        """
        excluded_user_attributes = [
            'deleted', 'center.user_count', 'role.resource_access_levels',
            'created_at', 'updated_at'
        ]
        excluded_user_attributes.extend(EXCLUDED_FIELDS)
        return UserSchema(
            exclude=excluded_user_attributes).dump(
            User.get_or_404(obj.created_by)).data
