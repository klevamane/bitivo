"""Module for asset category database model"""

# Third Party
from marshmallow import fields, post_load, validates_schema, post_dump
from sqlalchemy import text
from flask import request
# Models
from api.models.database import db
from api.models import AssetCategory, Asset, User, Attribute
# Schemas
from .attribute import AttributeSchema
from .base_schemas import BaseSchema

# Validators
from ..utilities.validators.name_validator import name_validator
from ..utilities.validators.string_length_validators import string_length_validator
from ..utilities.validators.asset_category_exists import validate_priority
from ..utilities.validators.duplicate_validator import validate_duplicate
from ..utilities.validators.image_validator import validate_image
from ..utilities.error import raise_error
from ..utilities.sql_queries import sql_queries
from ..utilities.helpers.check_user_role import is_super_user
from ..utilities.constants import EXCLUDED_FIELDS

# Helpers
from ..utilities.helpers.schemas import common_args

# Utilities
from ..utilities.title_case import title_case
from ..utilities.messages.error_messages import serialization_errors
from ..utilities.validators.validate_id import id_validator


class AssetCategorySchema(BaseSchema):
    """Asset category model schema"""
    id = fields.String()
    image = fields.Dict(
        required=True,
        error_messages={'required': serialization_errors['field_required']},
        validate=validate_image)
    name = fields.String(**common_args(
        validate=(string_length_validator(60), name_validator)))
    description = fields.String(validate=(string_length_validator(1000)))
    parent_id = fields.String(
        load_from='parentId', dump_to='parentId', validate=id_validator)

    running_low = fields.Integer(load_from='runningLow', dump_to='runningLow')
    low_in_stock = fields.Integer(load_from='lowInStock', dump_to='lowInStock')
    assets_count = fields.Method(
        'get_asset_counts',
        load_from='assetsCount',
        dump_to='assetsCount',
    )
    sub_category_count = fields.Method(
        'get_subcategory_count',
        dump_only=True,
        dump_to='subCategoryCount',
    )
    priority = fields.Function(
        lambda obj: obj.priority.value,
        deserialize=lambda value: '_'.join(value.strip().lower().split()),
        validate=validate_priority,
        load_from='priority',
        dump_to='priority')

    @validates_schema
    def validate_running_low(self, data):
        """Validates running_low value if supplied

        Args:
            data (dict): data supplied to the schema
        """

        if 'low_in_stock' in data or 'running_low' in data:
            self.validate_both_running_low_and_low_in_stock(data)

            if data.get('low_in_stock') >= data['running_low']:
                raise_error(
                    'comparison_error',
                    'runningLow',
                    'lowInStock',
                    fields='runningLow')

    @post_load
    def validate_asset_category(self, data):
        """Return asset category object after successful loading of data"""

        validate_duplicate(
            AssetCategory, name=data.get('name'), id=data.get('id'))

    @post_dump
    def convert_priority(self, data):
        """Return asset category object after successful loading of data

        Args:
            data (dict): data supplied to the schema
        """
        title_case('priority', data)

    def get_asset_counts(self, obj):
        """Returns the asset category assets count"""
        user = User.get_or_404(request.decoded_token['UserInfo']['id'])
        if is_super_user(user.token_id):
            return obj.assets_count
        return Asset.query_().filter_by(
            asset_category_id=obj.id,
            center_id=user.center_id, deleted=False).count()

    def get_subcategory_count(self, obj):
        """Returns the category subcategory count"""
        return obj.child_count()

    def validate_both_running_low_and_low_in_stock(self, data):
        """Validates that both running_low and low_in_stock values must be supplied, not just one of them

        Args:
            data (dict): data supplied to the schema
        """

        if not data.get('low_in_stock'):
            raise_error('missing_entry', 'lowInStock', fields='lowInStock')

        elif not data.get('running_low'):
            raise_error('missing_entry', 'runningLow', fields='runningLow')


class AssetCategoryWithAssetsSchema(AssetCategorySchema):
    assets = fields.Method(
        'get_assets',
        dump_to='assets',
    )

    def get_assets(self, obj):
        """Returns assets of an asset category

        Args:
            obj (class): an instance of the asset category class

        Returns:
            (list): the assets of an asset category
        """
        from api.schemas.asset import AssetSchema
        user = User.get_or_404(request.decoded_token['UserInfo']['id'])
        schema = AssetSchema(exclude=EXCLUDED_FIELDS, many=True)
        if is_super_user(user.token_id):
            return schema.dump(Asset.query_().filter_by(asset_category_id=obj.id).all()).data
        return schema.dump(Asset.query_().filter_by(asset_category_id=obj.id, center_id=user.center_id)).data


class EagerLoadAssetCategoryAttributesSchema(AssetCategorySchema):
    """Schema for Asset Category with eager loaded attributes"""

    custom_attributes = fields.Method(
        'get_eager_loaded_attributes',
        load_from='customAttributes',
        dump_to='customAttributes')

    def get_eager_loaded_attributes(self, obj):
        """Get serialized eager loaded attributes"""
        attributes = Attribute.query_().filter_by(asset_category_id=obj.id, deleted=False).all()
        attribute_schema = AttributeSchema(many=True, exclude=['deleted'])
        return attribute_schema.dump(attributes).data


class AssetSubCategorySchema(EagerLoadAssetCategoryAttributesSchema):
    """Asset subcategory model schema"""

    subCategories = fields.Method('get_subcategories')

    def get_subcategories(self, obj):
        """Returns subcategories of an asset category

        Args:
            obj (class): an instance of the asset category class

        Returns:
            (list): the subcategories of an asset category
        """

        subcategory_sql_query = sql_queries[
            'get_asset_category_subcategories'].format(obj.id)
        subcategories = db.engine.execute(text(subcategory_sql_query))
        sub_category_list = []

        for subcategory in subcategories:
            if not subcategory.deleted:
                single_category = AssetCategory.get_or_404(subcategory.id)
                sub_category_list.append({
                    'id':
                    subcategory.id,
                    'name':
                    subcategory.name,
                    'description':
                    subcategory.description,
                    'assetsCount':
                    AssetCategorySchema().dump(
                        single_category).data['assetsCount'],
                    'image':
                    subcategory.image
                })
        return sub_category_list


class AssetCategoryStatsSchema(AssetCategorySchema):
    """Schema for Asset Category with side loaded stats"""

    priority = fields.String()
    stats = fields.Method('get_stats')

    class Meta:
        fields = [
            'id', 'name', 'assets_count', 'priority', 'running_low',
            'low_in_stock', 'stats', 'image'
        ]
        ordered = True

    def get_stats(self, obj):
        """Returns stats for each asset in an asset category

        Args:
            obj (class): an instance of the asset category class

        Returns:
            (dict): the stats of an asset category
        """

        # total assets that have been assigned to people and spaces
        total_assigned = obj.space_assignee + obj.people_assignee

        # expected quantity of 'ok' assets in store
        expected_store_balance = obj.total_ok_assets - total_assigned

        return {
            'ok': {
                'totalAssets': obj.total_ok_assets,
                'assigned': {
                    'space': obj.space_assignee,
                    'people': obj.people_assignee,
                    'total': total_assigned
                },
                'stockCount': {
                    'expectedBalance': expected_store_balance,
                    'actualBalance': {
                        'date':
                        str(obj.stock_date) if obj.stock_date else None,
                        'count': obj.last_stock_count
                    },
                    'difference': obj.last_stock_count - expected_store_balance
                }
            },
            'notOk': {
                'totalAssets': self.get_asset_counts(obj) - obj.total_ok_assets,
                'assigned': {},
                'stockCount': {
                    'expectedBalance': None,
                    'actualBalance': {
                        'date': None,
                        'count': None,
                    },
                    'difference': None
                }
            }
        }


class AttributesAndStatsSchema(AssetCategoryStatsSchema):
    priority = fields.String()
    customAttributes = fields.Method('get_attributes')

    class Meta:
        fields = [
            'id', 'name', 'assets_count', 'priority', 'running_low',
            'low_in_stock', 'stats', 'customAttributes'
        ]
        ordered = True

    def get_attributes(self, obj):
        return obj.customAttributes


class AssetReconciliationStatsSchema(BaseSchema):
    """Asset Category schema with side loaded stats"""

    stockCount = fields.Method('unreconciled_asset')

    class Meta:
        fields = ['id', 'name', 'stockCount']
        ordered = True

    def unreconciled_asset(self, obj):
        """Field method for stockCount"""

        total_assigned = obj.space_assignee + obj.people_assignee

        expected_store_balance = obj.total_ok_assets - total_assigned
        count = obj.last_stock_count
        difference = obj.last_stock_count - expected_store_balance
        if (difference != 0):
            return {
                'expectedBalance': expected_store_balance,
                'actualBalance': {
                    'date': str(obj.stock_date),
                    'count': count
                },
                'difference': obj.last_stock_count - expected_store_balance
            }
