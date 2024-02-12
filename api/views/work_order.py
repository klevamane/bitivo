"""Module for work order related endpoints"""

# Flask
from flask import request

# Third-party libraries
from flask_restplus import Resource

# Middlewares
from api.utilities.error import raises
from api.utilities.validators.work_order_validators \
    import validate_assignee_as_member_of_center

# Model
from api.models import WorkOrder, MaintenanceCategory

# Decorator
from api.middlewares.token_required import token_required

# Schemas
from ..schemas.work_order import WorkOrderSchema

# Validators
from ..utilities.validators.validate_json_request import validate_json_request

# Validators
from ..utilities.validators.validate_id import validate_id

# Utilities
from ..utilities.messages.success_messages import SUCCESS_MESSAGES
from ..utilities.constants import EXCLUDED_FIELDS
from api.utilities.swagger.collections.work_order import work_order_namespace
from api.utilities.swagger.swagger_models.work_order import work_order_model
from api.utilities.swagger.constants import PAGINATION_PARAMS
from api.utilities.helpers.pagination_conditional import should_resource_paginate
from ..utilities.helpers.endpoint_response import get_success_responses_for_post_and_patch
from ..utilities.helpers.resource_manipulation_for_delete import delete_with_cascade, bulk_delete
# Resources
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@work_order_namespace.route('/')
class WorkOrderResource(Resource):
    """Resource class for a work order"""

    @token_required
    @permission_required(Resources.WORK_ORDERS)
    @work_order_namespace.doc(params=PAGINATION_PARAMS)
    def get(self):
        """Gets the list of Work orders"""
        data, meta = should_resource_paginate(request, WorkOrder,
                                              WorkOrderSchema)
        return {
            "data": data,
            "message": SUCCESS_MESSAGES['fetched'].format('Work Orders'),
            "meta": meta,
            "status": 'success'
        }

    @token_required
    @permission_required(Resources.WORK_ORDERS)
    @validate_json_request
    @work_order_namespace.expect(work_order_model)
    def post(self):
        """Method for creating a work order.

           Payload should have the following parameters:

           title(str): title of the work order
           description(str): description of the work order
           centerId(str): id of center
           assigneeId(str): token id of an assignee
           maintenanceCategoryId(str): id of maintenance category
           frequency_type(str): frequency type for work order
           frequencyUnits(int) : frequency unit for work order
           start_date(str) : work order start date,
           end_date(str) : work order end date

        Returns:
            dict: a dictionary of the created work order
        """

        exclude = EXCLUDED_FIELDS.copy()
        request_object = request.get_json()

        work_order_schema = WorkOrderSchema(exclude=exclude)
        work_order_data = work_order_schema.load_object_into_schema(
            request_object)
        work_order_details = WorkOrder(**work_order_data)
        work_order_details.save()

        return get_success_responses_for_post_and_patch(
            work_order_details,
            work_order_schema,
            'Work Order',
            status_code=201,
            message_key='created')

    @token_required
    @permission_required(Resources.WORK_ORDERS)
    @validate_json_request
    def delete(self):
        """This endpoint deletes more than a single work order

        Returns:
            dict: Response from the delete request
        """
        work_order_id_list = request.get_json()
        if not work_order_id_list:
            raises('cannot_be_empty', 400, 'work orders')

        return bulk_delete(request, WorkOrder, *work_order_id_list)


@work_order_namespace.route('/<string:work_order_id>')
class SingleWorkOrderResource(Resource):
    """Work order Resource class for implementing  HTTP verbs."""

    @token_required
    @permission_required(Resources.WORK_ORDERS)
    @validate_id
    def get(self, work_order_id):
        """Gets a specific work order.

        Args:
            work_order_id(str): the id of the work_order_id
        Returns:
            dict : A dictionary containing the response sent to the user

        """

        work_order_obj = WorkOrder.get_or_404(work_order_id)
        exclude = EXCLUDED_FIELDS.copy()
        work_order_schema = WorkOrderSchema(exclude=exclude)
        data = work_order_schema.dump(work_order_obj).data

        return {
            'data':
            data,
            "message":
            SUCCESS_MESSAGES['successfully_fetched'].format("Work order"),
            "status":
            "success"
        }

    @token_required
    @permission_required(Resources.WORK_ORDERS)
    @validate_id
    def delete(self, work_order_id):
        """This endpoint deletes a work order

        Args:
            work_order_id (str): The id of the work order to be deleted

        Returns:
            dict: Response from the delete request
        """

        return delete_with_cascade(request, WorkOrder, work_order_id,
                                   'work order')

    @token_required
    @permission_required(Resources.WORK_ORDERS)
    @validate_id
    @validate_json_request
    @work_order_namespace.expect(work_order_model)
    def patch(self, work_order_id):
        """An endpoint to update existing work order
            Args:
                work_order_id (str): the work order id
            Returns:
                dict: a dictionary of the updated request, message and status
        """

        # Fetch work_order  by id
        work_order = WorkOrder.get_or_404(work_order_id)
        maintenanceCategory = MaintenanceCategory.get_or_404(
            work_order.maintenance_category.id)
        end_date = work_order.end_date
        start_date = work_order.start_date
        # get the request_object
        request_object = request.get_json()
        context = {
            "end_date": end_date.strftime("%Y-%m-%d %H:%M:%S"),
            "start_date": start_date.strftime("%Y-%m-%d %H:%M:%S"),
            "work_order_id": work_order_id
        }
        validate_assignee_as_member_of_center(request_object,
                                              maintenanceCategory.center_id,
                                              work_order.assignee_id)

        work_order_schema = WorkOrderSchema(
            exclude=EXCLUDED_FIELDS, context=context)

        work_order_data = work_order_schema.load_object_into_schema(
            request_object, partial=True)

        work_order.update_(**work_order_data)

        return get_success_responses_for_post_and_patch(
            work_order,
            work_order_schema,
            "Work Order",
            status_code=200,
            message_key='updated')
