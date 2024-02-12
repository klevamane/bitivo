from api.utilities.validators.maintenance_category_validators import validate_title_exists
from ..utilities.constants import EXCLUDED_FIELDS
"""Module to Serialize and Deserialize Maintenance Categories"""
# Third party libraries
from marshmallow import fields, post_load, pre_load

# Utilities
from api.utilities.helpers.schemas import common_args
from api.utilities.constants import EXCLUDED_FIELDS

# work order model
from api.models import MaintenanceCategory
from api.models import WorkOrder

# Utilities
from api.utilities.helpers.schemas import common_args

# Messages
from ..utilities.messages.error_messages import serialization_errors

# Validators
from ..utilities.validators.asset_category_exists import asset_category_exists
from ..utilities.validators.name_validator import name_validator
from ..utilities.validators.resource_exists_validator import resource_exists
from ..utilities.validators.string_length_validators import string_length_validator

# Schemas
from .asset_category import AssetCategorySchema
from .base_schemas import AuditableBaseSchema
from .center import CenterSchema
EXCLUDED = EXCLUDED_FIELDS.copy()
EXCLUDED.append('maintenance_category_id')
exclude = ['center', 'maintenance_category_id']
EXCLUDED.extend(exclude)


class MaintenanceCategorySchema(AuditableBaseSchema):
    """Schema for maintenance category model"""

    title = fields.String(**common_args(
        validate=[string_length_validator(60), name_validator]))

    asset_category_id = fields.String(
        load_only=True,
        load_from="assetCategoryId",
        **common_args(validate=asset_category_exists))

    center_id = fields.String(
        load_only=False,
        load_from="centerId",
        dump_to="centerId",
        **common_args(validate=resource_exists))

    asset_category = fields.Nested(
        AssetCategorySchema,
        only=['id', 'name'],
        dump_only=True,
        dump_to="assetCategory")

    center = fields.Nested(
        CenterSchema,
        dump_only=True,
        only=['id', 'image', 'name'],
        dump_to="center")

    work_orders = fields.Nested(
        "WorkOrderSchema",
        many=True,
        exclude=EXCLUDED,
        load_from="workOrders",
        dump_to="workOrders")
    work_order_count = fields.Integer(dump_to='workOrderCount', dump_only=True)

    @post_load
    def validate_title(self, data):
        """This functions validates the work order title at the schema before it is
        saved to the datatbase
        Args:
             data (dict): This is a dictionary object of the work order data
        """

        validate_title_exists(MaintenanceCategory, data)
