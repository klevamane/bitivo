"""
Model Definition for permission collection
"""

from flask_restplus import fields
from ..collections.permission import permission_namespace


# swagger model that defines permission fields
permission_model = permission_namespace.model(
    "permission", {
        'type': fields.String(
            required=True, description='permission type'
        )
    }
)
