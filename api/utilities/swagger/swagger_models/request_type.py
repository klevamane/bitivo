"""
Model Definition for request type collection
"""

from flask_restplus import fields
from ..collections.request_type import request_type_namespace

# swagger model that defines request type fields
request_type_model = request_type_namespace.model(
    "request_type_model", {
        'title': fields.String(
            required=True, description='title of the request type'
        ),
        'centerId': fields.String(
            required=True, description='center id'
        ),
        'assigneeId': fields.String(
            required=True, description='token id for the user'
        ),
        'responseTime': fields.Nested(request_type_namespace.model(
            'responseTime', {
                'days': fields.Integer(
                    required=True, description = 'response time'
                )
            }
        ) 
        ),
        'resolutionTime': fields.Nested(request_type_namespace.model(
            'resolutionTime', {
                'days': fields.Integer(
                    required=True, description = 'resolution time'
                )
            }
        ) 
        ),
         'closureTime': fields.Nested(request_type_namespace.model(
            'closureTime', {
                'hours': fields.Integer(
                    required=True, description = 'closure time'
                )
            }
        ) 
        )
    }
)
