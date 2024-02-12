"""Module for asset category resource."""

# Flask
from flask_restplus import Resource
from flask import request, jsonify

from api.utilities.swagger.collections.asset import (
    asset_categories_namespace, asset_subcategories_namespace)
from api.utilities.swagger.swagger_models.asset import asset_categories_model
from api.utilities.swagger.constants import CATEGORY_REQUEST_PARAMS, SINGLE_ASSET_CATEGORY_REQUEST_PARAMS
# Model
from api.models import AssetCategory, Asset

# Decorator
from api.middlewares.token_required import token_required

# Schemas
from api.schemas.asset_category import (
    AssetCategorySchema, AssetSubCategorySchema, AssetCategoryWithAssetsSchema)
from api.schemas.attribute import AttributeSchema
from ..schemas.asset import AssetSchema

# Validators
from api.middlewares.base_validator import ValidationError
from api.utilities.validators.validate_id import validate_id
from ..utilities.validators.validate_json_request import validate_json_request

# utilities
from api.utilities.messages.error_messages import serialization_errors
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from ..utilities.constants import EXCLUDED_FIELDS, STATS
from ..utilities.helpers.asset_categories_endpoints import map_asset_categories_data
from ..utilities.attributes_data_parser import parse_attributes_data
from ..utilities.helpers.endpoint_response import get_success_responses_for_post_and_patch
from ..utilities.helpers.resource_manipulation_for_delete import delete_by_id
from ..utilities.helpers.asset_categories_endpoints import delete_asset_handler, sub_category_handler
from ..utilities.error import raises
from ..utilities.helpers.env_resource_adapter import adapt_resource_to_env
# Resourses
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required

# tasks
from ..tasks.cloudinary.cloudinary_file_handler import FileHandler


@asset_categories_namespace.route('/')
class AssetCategoryResource(Resource):
    """
    Resource class for performing crud on the asset categories
    """

    @token_required
    @permission_required(Resources.ASSET_CATEGORIES)
    @validate_json_request
    @asset_categories_namespace.expect(asset_categories_model)
    def post(self):
        """
        Creates asset categories and the corresponding attributes
        """

        request_data = request.get_json()
        asset_category_schema = AssetCategorySchema(exclude=EXCLUDED_FIELDS)
        asset_category_schema.load_object_into_schema(request_data)

        asset_category = asset_category_schema.load_object_into_schema(
            request_data)
        asset_category = AssetCategory(**asset_category)

        attributes_data = request_data.get('customAttributes')
        sub_categories = request_data.get('subCategories')

        if attributes_data:
            attributes_schema = AttributeSchema(
                many=True, exclude=['id', 'deleted'])
            attributes = attributes_schema.load_object_into_schema(
                attributes_data)
            asset_category.attributes = attributes
            attributes = attributes_schema.dump(attributes).data
        else:
            raise ValidationError(
                {'message': serialization_errors['provide_attributes']})

        asset_category = asset_category.save()
        asset_category_id = asset_category_schema.dump(
            asset_category).data['id']

        if sub_categories:
            for sub_category in sub_categories:
                asset_category_schema.load_object_into_schema(sub_category)

                parse_sub_category = asset_category_schema.load_object_into_schema(
                    sub_category)
                parsed_sub_category = AssetCategory(
                    **parse_sub_category, parent_id=asset_category_id)
                parsed_sub_category.save()

        response, status_code = get_success_responses_for_post_and_patch(
            asset_category,
            asset_category_schema,
            'Asset Category',
            status_code=201,
            message_key='created')
        response['data']['customAttributes'] = attributes
        response['data']['subCategories'] = sub_categories

        return response, status_code

    @token_required
    @permission_required(Resources.ASSET_CATEGORIES)
    @asset_categories_namespace.doc(params=CATEGORY_REQUEST_PARAMS)
    def get(self):
        """
        Gets list of asset categories and the corresponding asset count
        """
        url_include_query = sorted(request.args.getlist('include'))
        key = '_'.join(url_include_query).lower().strip()
        data, pagination_meta = map_asset_categories_data(key)()

        deleted = request.args.to_dict().get('include')

        data, pagination_meta = map_asset_categories_data(key)(include_deleted=True) \
            if deleted == 'deleted' else (data, pagination_meta)

        return {
            'status': 'success',
            'data': data,
            "meta": pagination_meta
        }, 200


@asset_categories_namespace.route('/stats')
class AssetCategoryStats(Resource):
    """
    Resource class for getting asset categories and
    their corresponding asset counts
    """

    @token_required
    @permission_required(Resources.ASSET_CATEGORIES)
    def get(self):
        """
        Gets asset categories and the corresponding asset count
        """
        asset_categories = AssetCategory.query_(request.args)
        deleted = request.args.to_dict().get('include')

        asset_categories = AssetCategory.query_(request.args, include_deleted=True) \
            if deleted == 'deleted' else asset_categories

        asset_category_schema = AssetCategorySchema(many=True) if deleted == 'deleted' \
            else AssetCategorySchema(many=True, exclude=['deleted'])

        return {
            'status': 'success',
            'data': asset_category_schema.dump(asset_categories).data
        }


@asset_categories_namespace.route('/<string:asset_category_id>')
class AssetCategoryListResource(Resource):
    """Asset category list resource"""

    @token_required
    @permission_required(Resources.ASSET_CATEGORIES)
    @validate_id
    @asset_categories_namespace.doc(
        params=SINGLE_ASSET_CATEGORY_REQUEST_PARAMS)
    def get(self, asset_category_id):
        """
        Get a single asset category
        """

        side_load_stats = request.args and request.args.get(
            'include', '').lower() == STATS

        single_category = AssetCategory.get_or_404(asset_category_id)

        data = AssetSubCategorySchema(
            exclude=['deleted']).dump(single_category).data

        if side_load_stats:
            single_stats = map_asset_categories_data('single_stats')
            stats = single_stats(asset_category_id)
            data.update(stats)

        return {'status': 'success', 'data': {**data}}, 200

    @token_required
    @permission_required(Resources.ASSET_CATEGORIES)
    @validate_json_request
    @validate_id
    @asset_categories_namespace.expect(asset_categories_model)
    def patch(self, asset_category_id):
        """
        Updates asset categories and the corresponding attributes
        """

        asset_category = AssetCategory.get_or_404(asset_category_id)
        request_data = request.get_json()
        request_data['id'] = asset_category_id

        asset_category_schema = AssetCategorySchema(exclude=EXCLUDED_FIELDS)

        asset_category_data = asset_category_schema.load_object_into_schema(
            request_data, partial=True)

        attributes_data = request_data.get('customAttributes')
        subcategory_data = request_data.get('subCategories')

        if subcategory_data:
            for sub_category in subcategory_data:
                sub_category_handler(sub_category, asset_category_id,
                                     asset_category_schema, AssetCategory)

        attributes_schema = AttributeSchema(many=True, exclude=['deleted'])

        if attributes_data:
            attributes_schema_data = attributes_schema.load_object_into_schema(
                attributes_data, partial=True)  # noqa

            parse_attributes_data(asset_category, attributes_schema_data,
                                  asset_category_id)

        asset_category.update_(**asset_category_data)

        attributes = attributes_schema.dump(
            asset_category.attributes.all()).data
        asset_category_data = asset_category_schema.dump(asset_category).data

        response = jsonify({
            "status":
            'success',
            "message":
            SUCCESS_MESSAGES['updated'].format('Asset'),
            "data": {
                **asset_category_data, "customAttributes": attributes,
                "subCategories": subcategory_data
            }
        })
        response.status_code = 200
        return response

    @token_required
    @permission_required(Resources.ASSET_CATEGORIES)
    @validate_id
    def delete(self, asset_category_id):
        """
        Soft delete asset categories
        """
        asset_category = AssetCategory.get_or_404(asset_category_id)
        for asset in asset_category.assets.filter_by(deleted=False).all():
            delete_by_id(Asset, asset.id, '')
        sub_categories = [
            sub_category for sub_category in asset_category.children
            if sub_category.deleted is False
        ]
        for sub_category in sub_categories:
            for asset in sub_category.assets.filter_by(deleted=False).all():
                delete_by_id(Asset, asset.id, '')
            delete_by_id(AssetCategory, sub_category.id, '')
        return delete_by_id(AssetCategory, asset_category_id, 'Category')


@asset_categories_namespace.route('/<string:asset_category_id>/assets')
class AssetCategoryAsset(Resource):
    """
    Resource class for getting the list of assets that belong to an asset category  # noqa
    """

    @token_required
    @permission_required(Resources.ASSET_CATEGORIES)
    @validate_id
    def get(self, asset_category_id):
        """
        Gets list of assets that belong to an asset category
        """

        asset_category = AssetCategory.get_or_404(asset_category_id)

        args = request.args.to_dict()
        deleted = args.get('include')

        excluded_fields = EXCLUDED_FIELDS.copy()
        excluded_fields.remove('deleted')
        assets = AssetSchema(
            many=True, exclude=excluded_fields).dump(
                asset_category.assets, request_args=args).data if deleted == 'deleted' \
            else AssetCategoryWithAssetsSchema(
            exclude=EXCLUDED_FIELDS).dump(
            asset_category).data

        return {
            'status':
            'success',
            'message':
            serialization_errors['asset_category_assets'].format(
                asset_category.name),  # noqa
            'data':
            assets
        }


@asset_subcategories_namespace.route("/<string:subcategory_id>")
class AssetSubcategoryResource(Resource):
    """Delete asset subcategory resource"""

    @token_required
    @validate_id
    def delete(self, subcategory_id):
        """
        Soft delete asset categories
        Args:
            subcategory_id (str): the id of the resource to be deleted
        Raises:
            ValidationError (Exception):
                A message that indicates that the delete was unsuccessful
        Returns:
                    (dict): contains the response to be sent to the user
        """
        subcategory = AssetCategory.get_or_404(subcategory_id)
        if subcategory.parent_id:
            delete_asset_handler(subcategory_id)
            return delete_by_id(AssetCategory, subcategory_id, 'Subcategory')
        else:
            raises('cannot_delete', 403, 'category')
