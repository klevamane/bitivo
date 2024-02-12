"""Module for permission resources"""
# third party
from flask_restplus import Resource
from flask import request

# Schemas
from ..schemas.history import HistorySchema

# Decorators
from api.middlewares.token_required import token_required

# Utilities
from api.utilities.helpers.pagination_conditional import should_resource_paginate

# Models
from ..models import History

# Messages
from ..utilities.messages.success_messages import SUCCESS_MESSAGES
from ..utilities.helpers.resource_manipulation import get_paginated_resource, get_all_resources
from api.utilities.swagger.collections.history import history_namespace
from api.utilities.swagger.constants import HISTORY_REQUEST_PARAMS
# Resourses
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@history_namespace.route('/')
class HistoryResource(Resource):
    """Resource class for History
    """

    @token_required
    @permission_required(Resources.HISTORY)
    @history_namespace.doc(params=HISTORY_REQUEST_PARAMS)
    def get(self):
        """Get list of all history"""
        data, meta = should_resource_paginate(request, History, HistorySchema)
        return {
            "message": SUCCESS_MESSAGES['fetched'].format('History'),
            "data": data,
            "meta": meta,
            "status": 'success'
        }
