"""Module that handles asset warranty"""

# Third-party libraries
from flask_restplus import Resource
from flask import request

from api.utilities.swagger.collections.asset import (asset_namespace,
                                                     asset_warranty_namespace)
from api.utilities.swagger.swagger_models.asset import asset_warranty_model

# schemas
from ..schemas.asset_warranty import AssetWarrantySchema
from ..schemas.asset import AssetSchema

# models
from ..models import AssetWarranty
from ..models import Asset

# Messages
from ..utilities.messages.success_messages import SUCCESS_MESSAGES

# validators
from ..utilities.validators.validate_id import check_id_valid, validate_id
from ..utilities.validators.validate_json_request import validate_json_request
from ..utilities.validators.date_validator import validate_date_range

# helpers
from ..middlewares.token_required import token_required
from ..utilities.helpers.endpoint_response import (
    get_success_responses_for_post_and_patch)
from ..utilities.constants import EXCLUDED_FIELDS, REDUNDANT_FIELDS
# Resources
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@asset_namespace.route('/<string:asset_id>/warranty')
class AssetWarrantyResource(Resource):
    """Resource class for asset warranty endpoints."""

    @token_required
    @permission_required(Resources.ASSETS)
    @validate_json_request
    @asset_namespace.expect(asset_warranty_model)
    def post(self, asset_id):
        """
        Endpoint to create an asset warranty package.

        Args:
            asset_id (string): id for the asset
            request (object): request object

        Returns:
            reponse (dict): response data
        """

        check_id_valid(asset_id=asset_id)
        Asset.get_or_404(asset_id)
        request_data = request.get_json()
        start_date = request_data.get('startDate')
        end_date = request_data.get('endDate')
        validate_date_range(start_date, end_date)
        request_data['assetId'] = asset_id

        excluded = EXCLUDED_FIELDS.copy()
        excluded.extend(REDUNDANT_FIELDS)
        asset_warranty_schema = AssetWarrantySchema(exclude=excluded)

        asset_warranty_data = asset_warranty_schema.load_object_into_schema(
            request_data)
        asset_warranty = AssetWarranty(**asset_warranty_data)
        asset_warranty.save()

        return get_success_responses_for_post_and_patch(
            asset_warranty,
            asset_warranty_schema,
            'Asset warranty package',
            status_code=201,
            message_key='created')

    @token_required
    @permission_required(Resources.ASSETS)
    @validate_id
    def get(self, asset_id):
        """ Gets all warranty details belonging to a specific asset
        Args:
            self (assetWarrantyResource): instance of asset warranty resource
            asset_id (string): the id of the asset
           Returns:
            dict: a dictionary of an asset warranty details
        """

        Asset.get_or_404(asset_id)
        excluded = EXCLUDED_FIELDS.copy()
        excluded.extend(REDUNDANT_FIELDS)
        asset_warranty_schema = AssetWarrantySchema(exclude=excluded)
        asset_warranty_data = asset_warranty_schema.dump(
            AssetWarranty.query_().filter_by(asset_id=asset_id).first()).data

        return {
            "status":
            'success',
            "message":
            SUCCESS_MESSAGES['successfully_fetched'].format('Asset warranty'),
            "data":
            asset_warranty_data
        }, 200


@asset_warranty_namespace.route('/<string:warranty_id>')
class SingleAssetWarrantyResource(Resource):
    """
    Resource class for carrying out operations on a single
    warranty
    """

    @token_required
    @permission_required(Resources.ASSETS)
    @validate_id
    @validate_json_request
    @asset_warranty_namespace.expect(asset_warranty_model)
    def patch(self, warranty_id):
        """
        PATCH method for updating a asset warranty package.
         Method parameters:
            warranty_id (str): the unique id of the warranty being
            updated
         Request payload can have the following parameters:
            status (str): new status(active or expired)
            startDate (str): new start date
            endDate (str): new end date
         Response payload should have the following parameters:
            data (dict): a dictionary with the updated information
            message (str): a message showing role update success
            status (str): a message showing role was updated successfully
        """
        asset_warranty = AssetWarranty.get_or_404(warranty_id)

        request_data = request.get_json()
        start_date = request_data.get('startDate')
        end_date = request_data.get('endDate')
        if not start_date:
            start_date = str(asset_warranty.start_date)
        if not end_date:
            end_date = str(asset_warranty.end_date)
        validate_date_range(start_date, end_date)

        excluded = EXCLUDED_FIELDS.copy()
        excluded.extend(REDUNDANT_FIELDS)
        asset_warranty_schema = AssetWarrantySchema(exclude=excluded)

        asset_warranty_data = asset_warranty_schema.load_object_into_schema(
            request_data, partial=True)

        asset_warranty.update_(**asset_warranty_data)

        return (get_success_responses_for_post_and_patch(
            asset_warranty,
            asset_warranty_schema,
            'Asset warranty package',
            status_code=200,
            message_key='updated'))
