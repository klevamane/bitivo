"""Module for Hot Desk Activity Log Resource """
# standard libraries
from flask_restplus import Resource
from flask import request

from api.utilities.swagger.collections.history import history_namespace
from api.utilities.swagger.constants import PAGINATION_PARAMS

# models
from api.models import HotDeskRequest, User

# schemas
from ..schemas.hot_desk import HotDeskRequestHistorySchema
from ..schemas.user import UserSchema

# decorators
from ..utilities.validators.validate_id import validate_id
from ..middlewares.token_required import token_required

# utilities
from ..utilities.constants import EXCLUDED_FIELDS
from ..utilities.messages.success_messages import SUCCESS_MESSAGES
from ..utilities.paginator import list_paginator, get_pagination_option
# Resourses
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@history_namespace.route("/<string:token_id>")
class SpecificUserActivityLogResource(Resource):
    @token_required
    @permission_required(Resources.PEOPLE)
    @validate_id
    @history_namespace.doc(params=PAGINATION_PARAMS)
    def get(self, token_id):
        """Endpoint to get all user's request activity log 
        Args:
            token_id(str):Token_id of the requester
        Returns:
            list: A dictionary containing user's request activity log
        """
        #  get the requester object
        User.get_or_404(token_id)
        excluded = EXCLUDED_FIELDS.copy()
        excluded.extend(
            ['role', 'image_url', 'center', 'status_dump', 'id', 'created_at'])
        current_user = User.get_or_404(token_id)
        user_schema = UserSchema(exclude=excluded)
        user_data = user_schema.dump(current_user).data

        # paginator
        paginate = get_pagination_option()

        # hotdesk activity log
        excluded = EXCLUDED_FIELDS.copy()
        excluded.extend(
            ['requester', 'complaint', 'reason', 'count', 'requester_id'])
        hot_desks = HotDeskRequest.query.filter(
            HotDeskRequest.deleted == False,
            HotDeskRequest.requester_id == token_id).order_by(
                HotDeskRequest.created_at.desc()).all()
        hotdesk_activity = HotDeskRequestHistorySchema(
            many=True, exclude=excluded)
        history_data = hotdesk_activity.dump(hot_desks).data

        # paginated data
        data, pagination_object = list_paginator(
            history_data, paginate=paginate)
        data = {
            "requester": user_data,
            "activityLog": data,
            "meta": pagination_object
        }
        return {
            "message":
            SUCCESS_MESSAGES['fetched'].format('Hot desk activity log'),
            "status": "success",
            'data': data,
        }
