"""Module to perform operations on maintenance categories"""

# Third party imports
from flask import request
from flask_restplus import Resource

# Flask
from flask_restplus import Resource
from flask import request, jsonify

# Validators
from api.middlewares.token_required import token_required
from api.middlewares.base_validator import ValidationError
from api.schemas.maintenance_categories import MaintenanceCategorySchema
from api.schemas.work_order import WorkOrderListSchema

# Messages

from api.utilities.messages.success_messages import SUCCESS_MESSAGES

# Model
from api.models import MaintenanceCategory

# utilities
from ..utilities.helpers.maintenance_category import create_maintenance_category
from ..utilities.helpers.endpoint_response import get_success_responses_for_post_and_patch
from ..utilities.validators.validate_json_request import validate_json_request
from api.utilities.validators.validate_id import validate_id
from api.utilities.helpers.pagination_conditional import should_resource_paginate
from api.utilities.paginator import pagination_helper
from ..utilities.constants import EXCLUDED_FIELDS
from api.utilities.validators.maintenance_category_validators import (
    validate_titles_exists)
from api.utilities.helpers.resource_manipulation import get_all_resources
from ..utilities.helpers.maintenance_category import (
    maintenance_category_transaction)
from ..utilities.swagger.collections.maintenance_category import maintenance_category_namespace
from ..utilities.swagger.swagger_models.maintenance_category import maintenance_category_model
from api.utilities.swagger.constants import MAINTENANCE_CATEGORY_REQUEST_PARAMS

# Resources
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@maintenance_category_namespace.route('/')
class MaintenanceCategoryResource(Resource):
    """
    Resource class for performing crud operations on the maintenance categories
    """

    @token_required
    @permission_required(Resources.MAINTENANCE_CATEGORIES)
    @validate_json_request
    @maintenance_category_namespace.expect(maintenance_category_model)
    def post(self):
        """
        Creates maintenance categories

        Args:
            title (str): Title of the maintenance category
            assetCategoryId(str): The category id of the asset
            centerId(str): The center id

        Returns:
            dict: a dictionary of the created work order
        """

        request_data = request.get_json()
        maintenance_category_schema = MaintenanceCategorySchema(
            exclude=EXCLUDED_FIELDS)

        maintenance_category = maintenance_category_schema.load_object_into_schema(
            request_data)

        work_orders = maintenance_category.pop('work_orders', None)
        maintenance_category = create_maintenance_category(
            maintenance_category, work_orders)

        response, status_code = get_success_responses_for_post_and_patch(
            maintenance_category,
            maintenance_category_schema,
            'Maintenance Category',
            status_code=201,
            message_key='created')
        return response, status_code

    @token_required
    @permission_required(Resources.MAINTENANCE_CATEGORIES)
    @maintenance_category_namespace.doc(
        params=MAINTENANCE_CATEGORY_REQUEST_PARAMS)
    def get(self):
        """
        Get a list of all maintenance categories
        """
        response, pagination_object = should_resource_paginate(
            request, MaintenanceCategory, MaintenanceCategorySchema)
        return {
            "data":
            response,
            "status":
            'success',
            "message":
            SUCCESS_MESSAGES['successfully_fetched'].format(
                'Maintenance schedules'),
            "meta":
            pagination_object
        }


@maintenance_category_namespace.route('/<string:maintenance_category_id>')
class SingleMaintenanceCategoryResource(Resource):
    """Resource to perform operations on a single maintenace category"""

    @token_required
    @permission_required(Resources.MAINTENANCE_CATEGORIES)
    @validate_id
    def get(self, maintenance_category_id):
        """Endpoint to fetch a single maintenance category.

        Args:
            maintenance_category_id (str): maintenance category id
        Returns:
            dict : A dictionary containing the response sent to the user

        """
        maintenance_category_obj = MaintenanceCategory.get_or_404(
            maintenance_category_id)
        maintenance_category_schema = MaintenanceCategorySchema(
            exclude=EXCLUDED_FIELDS)
        data = maintenance_category_schema.dump(maintenance_category_obj).data

        return {
            'data':
            data,
            'message':
            SUCCESS_MESSAGES['successfully_fetched'].format(
                'Maintenance Category'),
            'status':
            'success'
        }

    @token_required
    @permission_required(Resources.MAINTENANCE_CATEGORIES)
    @validate_id
    def delete(self, maintenance_category_id):
        """Performs soft delete operation on a maintenance category

        Args:
            maintenance_category_id (str): maintenance category id

        Returns:
            (dict): successfull delete message
        """
        maintenance_category = MaintenanceCategory.get_or_404(
            maintenance_category_id)
        maintenance_category.delete()
        return {
            'status': 'success',
            'message':
            SUCCESS_MESSAGES['deleted'].format('Maintenance Category')
        }

    @token_required
    @permission_required(Resources.MAINTENANCE_CATEGORIES)
    @validate_json_request
    @maintenance_category_namespace.expect(maintenance_category_model)
    def patch(self, maintenance_category_id):
        """Update a catategory

        Args:

        Returns:
            Response (dict) : Returns data, success message, and status.
        """
        update_request = request.get_json()
        work_orders = update_request.get('workOrders', None)

        work_orders_update = []
        work_orders_to_save = []
        work_order_validated = None

        update_request['workOrders'] = work_orders_to_save

        if work_orders:
            work_orders_update.extend([
                work_order for work_order in work_orders
                if 'workOrderId' in work_order
            ])
            work_orders_to_save.extend([
                work_order for work_order in work_orders
                if 'workOrderId' not in work_order
            ])
        maintenance_category_schema = MaintenanceCategorySchema(
            exclude=EXCLUDED_FIELDS)
        if work_orders_update:
            work_order_schema = WorkOrderListSchema()
            work_order_data = work_order_schema.load_object_into_schema(
                {'work_orders': work_orders_update}, partial=True)
            for index, item in enumerate(work_orders_update):
                work_order_data['work_orders'][index][
                    'workOrderId'] = work_orders_update[index]['workOrderId']
            work_order_validated = work_order_data['work_orders']
        maintenance_category_exist = MaintenanceCategory.get_or_404(
            maintenance_category_id)

        maintenance_category_data = maintenance_category_schema.load_object_into_schema(
            update_request, partial=True)

        validate_titles_exists(MaintenanceCategory, update_request,
                               maintenance_category_id)
        work_orders = maintenance_category_data.pop("work_orders", None)

        asset_details = maintenance_category_transaction(
            maintenance_category_exist,
            work_orders,
            maintenance_category_data,
            work_orders_update=work_order_validated)
        data = maintenance_category_schema.dump(asset_details).data

        response = jsonify({
            "status":
            'success',
            "message":
            SUCCESS_MESSAGES['updated'].format('Maintenance category'),
            "data":
            data
        })
        response.status_code = 200
        return response
