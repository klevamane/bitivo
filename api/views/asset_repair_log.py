"""Module that handles asset repair logs operations"""

# Third-party libraries
from flask_restplus import Resource
from flask import request

from api.utilities.swagger.collections.asset import (repair_logs_namespace,
                                                     asset_namespace)
from api.utilities.swagger.swagger_models.asset import asset_repair_log_model
from api.utilities.swagger.constants import PAGINATION_PARAMS
# schemas
from ..schemas.asset_repair_log import AssetRepairLogSchema
from ..schemas.asset import AssetSchema

# models
from ..models import AssetRepairLog, Asset

# helpers
from ..middlewares.token_required import token_required

from ..utilities.validators.date_validator import validate_asset_log_return_date
# helpers

from ..utilities.constants import EXCLUDED_FIELDS, REDUNDANT_FIELDS
from ..utilities.helpers.endpoint_response import (
    get_success_responses_for_post_and_patch)
from ..utilities.validators.validate_json_request import validate_json_request
from ..utilities.helpers.pagination_conditional import should_resource_paginate
from ..utilities.messages.success_messages import SUCCESS_MESSAGES
from ..utilities.validators.validate_id import validate_id
from ..utilities.paginator import list_paginator
# Resources
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@repair_logs_namespace.route('/')
class AssetRepairLogResource(Resource):
    """
    Resource class for carrying out CRUD operations
    on asset repair logs entity
    """

    @token_required
    @permission_required(Resources.ASSETS)
    @validate_json_request
    @repair_logs_namespace.expect(asset_repair_log_model)
    def post(self):
        """
        An endpoint that creates a new asset repair log in the database
        """
        excluded_fields = EXCLUDED_FIELDS.copy()
        repair_log_details = request.get_json()
        return_date = repair_log_details.get('expectedReturnDate', '')
        validate_asset_log_return_date(return_date)
        repair_log_data = AssetRepairLogSchema().load_object_into_schema(
            repair_log_details)
        repair_log_details = AssetRepairLog(**repair_log_data)
        repair_log_details.save()

        return get_success_responses_for_post_and_patch(
            repair_log_details,
            AssetRepairLogSchema(exclude=excluded_fields),
            'Repair Log',
            status_code=201,
            message_key='created')

    @token_required
    @permission_required(Resources.ASSETS)
    @repair_logs_namespace.doc(params=PAGINATION_PARAMS)
    def get(self):
        """
        An endpoint to get all Repair logs
        """
        data, pagination_object = should_resource_paginate(
            request, AssetRepairLog, AssetRepairLogSchema)

        return {
            "message": SUCCESS_MESSAGES['fetched'].format('Repair logs'),
            "status": 'success',
            "data": data,
            "meta": pagination_object
        }, 200


@repair_logs_namespace.route("/<string:repair_log_id>")
class SingleRepairLogResource(Resource):
    @token_required
    @permission_required(Resources.ASSETS)
    @validate_id
    @validate_json_request
    @repair_logs_namespace.expect(asset_repair_log_model)
    def patch(self, repair_log_id):
        """
        An endpoint to update the details of a single asset repair log
        Args:
            repair_log_id (str): The repair log id
        Returns:
            dict: A dictionary containing the response sent to the user
        """
        request_data = request.get_json()
        return_date = request_data.get('expectedReturnDate', '')
        validate_asset_log_return_date(return_date)
        repair_log = AssetRepairLog.get_or_404(repair_log_id)
        excluded = EXCLUDED_FIELDS.copy()
        repair_log_schema = AssetRepairLogSchema(exclude=excluded)
        data = repair_log_schema.load_object_into_schema(
            request_data, partial=True)
        repair_log.update_(**data)
        return get_success_responses_for_post_and_patch(
            repair_log,
            repair_log_schema,
            'Repair Log',
            status_code=200,
            message_key='updated')


@asset_namespace.route("/<string:asset_id>/repair-logs")
class RepairLogsForSingleAssetResource(Resource):
    @token_required
    @permission_required(Resources.ASSETS)
    @validate_id
    @asset_namespace.doc(params=PAGINATION_PARAMS)
    def get(self, asset_id):
        """
        An endpoint to get all repair logs of an asset
        Args:
            asset_id (str): The asset id
        Returns:
            dict: A dictionary containing all repair logs of an asset
        """
        Asset.get_or_404(asset_id)
        excluded_fields = EXCLUDED_FIELDS.copy()
        excluded_fields.extend(REDUNDANT_FIELDS)
        repair_log_schema = AssetRepairLogSchema(
            exclude=excluded_fields, many=True)
        repair_log_data = repair_log_schema.dump(
            AssetRepairLog.query_().filter_by(asset_id=asset_id).all()).data
        repair_log_display, pagination_obj = list_paginator(repair_log_data)
        message = SUCCESS_MESSAGES['fetched'].format('Repair Logs')
        return {
            'message': message,
            'status': 'success',
            'repairLogs': repair_log_display,
            'meta': pagination_obj
        }, 200
