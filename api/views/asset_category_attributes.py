"""Module for asset category attribute views"""  # pylint: disable=F0002

from flask_restplus import Resource  # pylint: disable=E0401
from flask import request

from api.utilities.swagger.collections.asset import asset_categories_namespace
from api.utilities.swagger.collections.attributes import attributes_namespace
from api.utilities.validators.validate_id import validate_id
from ..models.asset_category import AssetCategory
from ..models.attribute import Attribute
from ..schemas.attribute import AttributeSchema
from ..middlewares.token_required import token_required
from ..utilities.validators.validate_json_request import validate_json_request
from ..utilities.helpers.resource_manipulation_for_delete import delete_by_id
# Resources
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@asset_categories_namespace.route('/<string:asset_category_id>/attributes')
class AssetCategoryAttributes(Resource):
    """Resource class for asset categories attributes"""

    @token_required
    @permission_required(Resources.ASSET_CATEGORIES)
    @validate_id
    def get(self, asset_category_id):  # pylint: disable=C0103, w0622,R0201
        """Get attributes of an asset category"""

        asset_category = AssetCategory.get_or_404(asset_category_id)

        args = request.args.to_dict()
        deleted = args.get('include')

        attributes_schema = AttributeSchema(many=True) if deleted == 'deleted' \
            else AttributeSchema(many=True, exclude=['deleted'])

        attributes = attributes_schema.dump(
            asset_category.attributes.filter_by(deleted=False),
            request_args=args).data

        return {
            'status': 'success',
            'message': 'Asset category attributes retrieved',
            'data': {
                'name': asset_category.name,
                'customAttributes': attributes
            }
        }, 200


@attributes_namespace.route('/<string:attribute_id>')
class DeleteAssetCategoryAttributes(Resource):
    """Resource class for deleting asset categories attributes"""

    @token_required
    @permission_required(Resources.ASSET_CATEGORIES)
    @validate_id
    def delete(self, attribute_id):
        """Delete an asset category attribute"""
        return delete_by_id(Attribute, attribute_id, "Attribute")
