"""Module for Single Hot Desk Resource """
# standard libraries
from flask_restplus import Resource
from flask import request

# schemas
from ..schemas.hot_desk import CancelHotDeskRequestSchema

# decorators
from ..utilities.validators.validate_id import validate_id
from ..middlewares.token_required import token_required
from ..utilities.validators.validate_json_request import validate_json_request, validate_reason

# utilities
from api.utilities.swagger.collections.hot_desk import hot_desk_namespace
from api.utilities.swagger.swagger_models.hot_desk import cancel_request_model
from ..utilities.constants import EXCLUDED_FIELDS
from ..utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.helpers.hot_desk import get_hotdesk_of_specific_user_by_requester_id
from api.utilities.enums import HotDeskRequestStatusEnum
from bot.utilities.user_hot_desk import cancel_hot_desk_by_id
from ..utilities.error import raises
# Resources
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@hot_desk_namespace.route("/<string:hot_desk_id>/cancel")
class CancelHotDeskRequestResource(Resource):
    @token_required
    @permission_required(Resources.HOT_DESKS)
    @validate_id
    @validate_json_request
    @validate_reason
    @hot_desk_namespace.expect(cancel_request_model)
    def patch(self, *args, **kwargs):
        """Endpoint to Cancel a hot desk request
        Kwargs:
            hot_desk_id(str):Hot desk_request_id
            reason(str):Reason for canceling hotdesk

        Returns:
            status(str): status message
            message(str): information on what has been updated
        """
        hot_desk_id = kwargs.get('hot_desk_id')
        reason = {"reason": kwargs.get("reason").lower()}
        username = request.decoded_token['UserInfo']['name']
        requester_id = request.decoded_token['UserInfo']['id']
        hotdesk_request = get_hotdesk_of_specific_user_by_requester_id(
            hot_desk_id, requester_id)

        if ((hotdesk_request.status == HotDeskRequestStatusEnum.pending) or
            (hotdesk_request.status == HotDeskRequestStatusEnum.approved)):

            hotdesk_ref_no = hotdesk_request.hot_desk_ref_no
            schema = CancelHotDeskRequestSchema(exclude=EXCLUDED_FIELDS)
            data = schema.load_object_into_schema(
                reason,
                partial=[
                    'assignee_id', 'hot_desk_ref_no', 'requester_id', 'status'
                ])
            cancel_hot_desk_by_id(hot_desk_id, reason['reason'])

            return {
                "message":
                SUCCESS_MESSAGES['successfully_cancelled'].format(
                    username, hotdesk_ref_no),
                "status":
                "success"
            }

        raises('invalid_hotdesk_status', 404, 'hot desk')
