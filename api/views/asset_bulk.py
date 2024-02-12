"""Module that handles asset-related operations"""
# System libraries
import copy

from flask import request
# Third-party libraries
from flask_restplus import Resource

from api.middlewares.token_required import token_required
from api.models import Asset
from api.schemas.bulk_asset_schema import BulkAssetSchema
# Helpers
from api.tasks.notifications.asset_bulk import AssetBulkNotifications
from api.utilities.constants import EXCLUDED_FIELDS
from api.utilities.helpers.bulk_asset_helper import BulkAssetHelper
from api.utilities.messages.error_messages import serialization_error
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.swagger.collections.asset import asset_namespace
from api.utilities.swagger.swagger_models.asset import bulk_asset_model

# Helpers
from ..utilities.validators.validate_json_request import validate_json_request, validate_bulk_assets_json, \
    validate_assets_type
# Resources
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@asset_namespace.route('/bulk')
class AssetBulkResource(Resource):
    """This is a class that creates multiple assets"""

    @token_required
    @permission_required(Resources.ASSETS)
    @validate_json_request
    @validate_bulk_assets_json
    @validate_assets_type
    @asset_namespace.expect(bulk_asset_model)
    def post(self):
        """Method to handle bulk assets post
        Returns:
            Response: with either responds with success when
            some assets are added or error when none of assets is added
        """
        assets = request.get_json()
        asset_schema = BulkAssetSchema(exclude=EXCLUDED_FIELDS)

        # send this data to the schema
        helper = BulkAssetHelper(assets, asset_schema)
        error_free_assets, assets_with_errors, custom_attributes = \
            helper.pass_data_schema_and_validator()
        assets_with_errors_json = []
        for asset in assets_with_errors:
            asset_object = asset_schema.dump(asset[0])[0]
            asset_object.update({"errors": asset[1]})
            assets_with_errors_json.append(asset_object)
        del assets_with_errors
        added_assets_json = None
        failed_records, successful_records = \
            len(assets_with_errors_json), len(error_free_assets)
        summary = {
            "TotalNoRecords": failed_records + successful_records,
            "FailedRecords": failed_records,
            "SuccessfulRecords": successful_records
        }
        if error_free_assets:
            assets_objects = Asset.bulk_create(error_free_assets)
            added_assets_json = asset_schema.dump(
                assets_objects, many=True).data
            response = {
                **summary, "status": "success",
                "message":
                SUCCESS_MESSAGES['created'].format('Multiple assets'),
                "data": {
                    "AddedAssets": added_assets_json,
                    "NonAddedAssets": assets_with_errors_json
                }
            }, 201
        elif assets_with_errors_json:
            response = {
                **summary, "message":
                serialization_error.error_dict["not_created"].format(
                    "Multiple assets"),
                "data":
                assets_with_errors_json,
                "status":
                "error"
            }, 400
        copy_errors = copy.deepcopy(assets_with_errors_json)
        copy_assets = copy.deepcopy(added_assets_json)
        AssetBulkNotifications.send_bulk_assets_mail_handler(
            copy_assets, copy_errors, custom_attributes)
        return response
