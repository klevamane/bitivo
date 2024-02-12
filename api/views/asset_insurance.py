"""Module that handles asset-inurance operations"""
from datetime import date

# Third-party libraries
from flask_restplus import Resource
from flask import request

from api.utilities.swagger.collections.asset import (asset_namespace,
                                                     asset_insurance_namespace)
from api.utilities.swagger.swagger_models.asset import asset_insurance_model

# Models
from api.models.asset_insurance import AssetInsurance
from api.models.asset import Asset
from api.models.history import History

# schema
from api.schemas.asset_insurance import AssetInsuranceSchema
from api.schemas.asset import AssetSchema
from api.schemas.history import HistorySchema

# validator
from ..utilities.validators.validate_id import validate_id, check_id_valid
from ..utilities.validators.validate_json_request import validate_json_request
from ..utilities.validators.date_validator import validate_date_range
from ..utilities.helpers.endpoint_response import (
    get_success_responses_for_post_and_patch, )

# middlewares
from ..middlewares.token_required import token_required

# helpers
from ..utilities.constants import EXCLUDED_FIELDS, REDUNDANT_FIELDS
from ..utilities.messages.success_messages import SUCCESS_MESSAGES
# Resources
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@asset_namespace.route('/<string:asset_id>/insurance')
class AssetInsuranceResource(Resource):
    """Resource class for asset insurance endpoints."""

    @token_required
    @permission_required(Resources.ASSETS)
    @validate_id
    def get(self, asset_id):
        """Endpoint to get all insurance policies for an asset."""

        today = date.today().strftime("%Y/%m/%d")
        Asset.get_or_404(asset_id)
        excluded = EXCLUDED_FIELDS.copy()
        excluded.extend(REDUNDANT_FIELDS)
        asset_insurance_schema = AssetInsuranceSchema(exclude=excluded)
        asset_insurance_data = AssetInsurance.query_().filter(
            AssetInsurance.asset_id == asset_id,
            AssetInsurance.end_date >= today).first()
        history_insurance_schema = HistorySchema(exclude=excluded, many=True)

        if not asset_insurance_data:
            asset_insurance_policy = asset_insurance_schema.dump(
                AssetInsurance.query.filter(
                    AssetInsurance.asset_id == asset_id,
                    AssetInsurance.end_date < today).order_by(
                        AssetInsurance.end_date.desc()).first()).data
        else:
            asset_insurance_policy = asset_insurance_schema.dump(
                asset_insurance_data).data

            history = history_insurance_schema.dump(History.query_().filter(
                History.resource_id == asset_insurance_data.id).all())
            asset_insurance_policy.update(
                {'history': history.data if history.data else []})

        return {
            'status':
            'success',
            'message':
            SUCCESS_MESSAGES['fetched'].format('Asset insurance policies'),
            'data':
            asset_insurance_policy
        }, 200

    @token_required
    @permission_required(Resources.ASSETS)
    @validate_json_request
    @asset_insurance_namespace.expect(asset_insurance_model)
    def post(self, asset_id):
        """
        Endpoint to create an asset insurance.
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
        asset_insurance_schema = AssetInsuranceSchema(exclude=excluded)

        asset_insurance_data = asset_insurance_schema.load_object_into_schema(
            request_data)
        asset_insurance = AssetInsurance(**asset_insurance_data)
        asset_insurance.save()

        return get_success_responses_for_post_and_patch(
            asset_insurance,
            asset_insurance_schema,
            'Asset insurance',
            status_code=201,
            message_key='created',
        )


@asset_insurance_namespace.route('/<string:insurance_id>')
class SingleAssetInsuranceResource(Resource):
    """Resource class for performing crud on Asset Insurance Policies """

    @token_required
    @permission_required(Resources.ASSETS)
    @validate_id
    @validate_json_request
    @asset_insurance_namespace.expect(asset_insurance_model)
    def patch(self, insurance_id):
        """Method updates an asset insurance policy

        Args:
            insurance_id (str): The id of the insurance policy to edit

        Returns:
            Response (dict): Returns data, success message and status.
        """
        edit_insurance_data = request.get_json()
        start_date = edit_insurance_data.get('startDate')
        end_date = edit_insurance_data.get('endDate')
        insurance_obj = AssetInsurance.get_or_404(insurance_id)
        # Validate dates
        if not start_date:
            start_date = str(insurance_obj.start_date)
        if not end_date:
            end_date = str(insurance_obj.end_date)
        validate_date_range(start_date, end_date)
        excluded = EXCLUDED_FIELDS.copy()
        excluded.extend(REDUNDANT_FIELDS)
        insurance_schema = AssetInsuranceSchema(exclude=excluded)
        update_data = insurance_schema.load_object_into_schema(
            edit_insurance_data, partial=True)
        insurance_obj.update_(**update_data)
        asset_insurance_data = insurance_schema.dump(insurance_obj).data
        return {
            "data": asset_insurance_data,
            "status": 'success',
            "message":
            SUCCESS_MESSAGES['edited'].format('Asset insurance policy')
        }, 200
