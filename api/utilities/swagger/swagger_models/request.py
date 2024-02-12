"""
Model Definition for request collection
"""

from flask_restplus import fields
from ..collections.request import request_namespace

# swagger model that defines request fields
request_model = request_namespace.model(
    "request_model", {
        'subject': fields.String(
            required=True, description='title of the request'
        ),
        'requestTypeId': fields.String(
            required=True, description='id of request type'
        ),
        'centerId': fields.String(
            required=True, description='id of center'
        ),
        'description': fields.String(
            required=True, description='description of request'
        ),
        'requesterId': fields.String(
            required=True, description='token id of requester'
        ),
        'attachments': fields.List(
            fields.Nested(request_namespace.model('cloudninary_model',{
            'public_id': fields.String(),
            'version': fields.String(),
            'signature': fields.String(),
            'width': fields.Integer(),
            'height': fields.Integer(),
            'created_at': fields.String(),
            'bytes': fields.Integer(),
            'type': fields.String(),
            'url': fields.String(),
            'secure_url': fields.String()
        }))
        )
    }
)
