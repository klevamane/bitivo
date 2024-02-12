"""Module for Single Hot Desk Resource """
# standard libraries
from flask_restplus import Resource
from flask import request
from datetime import datetime

# models
from api.models import HotDeskRequest

# schemas
from ..schemas.user import UserSchema
from ..schemas.hot_desk import HotDeskRequestSchema, HotDeskComplaintSchema

# decorators
from ..utilities.validators.validate_id import validate_id
from ..middlewares.token_required import token_required
from ..utilities.validators.validate_json_request import validate_json_request

# utilities
from api.utilities.swagger.collections.hot_desk import hot_desk_namespace
from api.utilities.swagger.swagger_models.hot_desk import cancel_request_model
from api.utilities.swagger.constants import HOTDESK_CANCEL_REQUEST
from api.utilities.helpers.endpoint_response import get_success_responses_for_post_and_patch
from ..utilities.constants import EXCLUDED_FIELDS
from ..utilities.messages.success_messages import SUCCESS_MESSAGES
from ..utilities.error import raises
from ..utilities.validators.hot_desk_resource_validator import validate_cancellation_reason
from ..utilities.enums import HotDeskCancellationReasonEnum, HotDeskRequestStatusEnum
from ..utilities.verify_date_range import report_query_date_validator
from ..utilities.paginator import list_paginator, get_pagination_option
# Resources
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@hot_desk_namespace.route("/<string:hot_desk_id>")
class SingleHotDeskRequest(Resource):
    @token_required
    @permission_required(Resources.HOT_DESKS)
    @validate_id
    def get(self, hot_desk_id):
        excluded = EXCLUDED_FIELDS.copy() + ['reason', 'count', 'requester_id']
        current_user = request.decoded_token['UserInfo']['id']
        specific_hotdesk_request = HotDeskRequest.get_or_404(hot_desk_id)
        if current_user == specific_hotdesk_request.requester_id:
            hotdesk_schema = HotDeskRequestSchema(exclude=excluded)
            data = hotdesk_schema.dump(specific_hotdesk_request).data

            return {
                "message":
                SUCCESS_MESSAGES['successfully_fetched'].format(
                    'Hotdesk Request'),
                'status':
                "success",
                'data':
                data
            }

        raises('cant_view', 403).format('Hotdesk Request')

    @token_required
    @permission_required(Resources.HOT_DESKS)
    @validate_id
    @validate_json_request
    @hot_desk_namespace.expect(cancel_request_model)
    def patch(self, hot_desk_id):
        """
        An endpoint to update a hotdesk request with a particular complaint
        Args:
            hot_desk_id (str): The hotdesk request id
        Returns:
            dict: A dictionary containing the response sent to the user
        """
        hot_desk = HotDeskRequest.get_or_404(hot_desk_id)
        request_data = request.get_json()
        fields = ['reason', 'count', 'requester_id']
        excluded = EXCLUDED_FIELDS.copy()
        excluded.extend(fields)
        user_id = request.decoded_token['UserInfo']['id']
        if user_id == hot_desk.requester_id:
            hot_desk_complaint_schema = HotDeskComplaintSchema(
                exclude=excluded)
            data = hot_desk_complaint_schema.load_object_into_schema(
                request_data, partial=True)
            hot_desk.update_(complaint_created_at=datetime.utcnow(), **data)
            return get_success_responses_for_post_and_patch(
                hot_desk,
                hot_desk_complaint_schema,
                'Hotdesk Request',
                status_code=200,
                message_key='updated')
        raises('request_center_update', 403, 'complaint')


@hot_desk_namespace.route('/cancelled')
class CancelledHotDeskResource(Resource):
    """ Resource for cancelled hot desk requests """

    @token_required
    @permission_required(Resources.HOT_DESKS)
    @report_query_date_validator
    @hot_desk_namespace.doc(params=HOTDESK_CANCEL_REQUEST)
    def get(self, *args):
        """ Endpoint to fetch all hot desk requests for a particular cancellation reason 
        Args:
            start_date (date): Start date. Defaults to 7 days difference from the end date
            end_date (date): End date. Defaults to the current date
        Returns:
            dict: A dictionary of all hot desk requests cancelled with a particular reason
        """

        reasons_dict = {
            'changedmymind':
            HotDeskCancellationReasonEnum.changed_my_mind.value,
            'leavingearly': HotDeskCancellationReasonEnum.leaving_early.value,
            'delayedapproval':
            HotDeskCancellationReasonEnum.delayed_approval.value,
            'seatchanged': HotDeskCancellationReasonEnum.seat_changed.value,
            'others': 'others'
        }
        start_date, end_date = args
        reason = request.args.get('reason', '').lower().strip()
        paginate = get_pagination_option()

        validate_cancellation_reason(reason)
        reason_value = reasons_dict.get(reason, '')

        excluded = EXCLUDED_FIELDS.copy()
        excluded.extend([
            'requester_id', 'assignee_id', 'count', 'reason', 'complaint',
            'complaint_created_at'
        ])

        if reason_value == 'others':
            query = HotDeskRequest.query.filter(
                HotDeskRequest.status == HotDeskRequestStatusEnum.cancelled,
                HotDeskRequest.reason !=
                HotDeskCancellationReasonEnum.changed_my_mind.value,
                HotDeskRequest.reason !=
                HotDeskCancellationReasonEnum.seat_changed.value,
                HotDeskRequest.reason !=
                HotDeskCancellationReasonEnum.leaving_early.value,
                HotDeskRequest.reason !=
                HotDeskCancellationReasonEnum.delayed_approval.value,
                HotDeskRequest.created_at.between(start_date, end_date)).all()
            excluded.remove('reason')

        else:
            query = self.get_reason_query(reason_value, start_date, end_date)

        hot_desk_data = HotDeskRequestSchema(
            many=True, exclude=excluded).dump(query).data
        result, meta = list_paginator(hot_desk_data, paginate=paginate)

        return {
            'status': 'success',
            'message':
            SUCCESS_MESSAGES['cancelled_hot_desk_reason'].format(reason),
            'data': {
                reason: result
            },
            'meta': meta
        }

    def get_reason_query(self, reason, start_date, end_date):
        '''Function to get query depending on cancellation reason provided
        Args:
            reason : Cancellation reason
            start_date (date): Start date. Defaults to 7 days difference from the end date
            end_date (date): End date. Defaults to the current date
        Returns:
            Query
        '''
        query = HotDeskRequest.query_().filter(
            HotDeskRequest.reason == reason,
            HotDeskRequest.created_at.between(start_date, end_date)).all()
        return query
