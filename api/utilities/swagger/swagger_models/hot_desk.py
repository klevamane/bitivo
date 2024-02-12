"""
Model Definition for hot desk collection
"""

from flask_restplus import fields
from ..collections.hot_desk import hot_desk_namespace


# swagger model that defines hot desks fields
hotdesk_request_model = hot_desk_namespace.model(
    "hotdesk_request", {
        'complaint': fields.String(
            required=True, description='hot desk request body')
    }
)

cancel_request_model = hot_desk_namespace.model(
    "hotdesk_cancel_request", {
        'reason': fields.String(
            required=True, description='Reason for cancelling hotdesk')
    }
)
