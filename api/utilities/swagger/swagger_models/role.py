"""
Model Definition for role collection
"""

from flask_restplus import fields
from ..collections.role import role_namespace

# swagger model that defines role fields
role_model = role_namespace.model(
    "role_model", {
        'title': fields.String(
            required=True, description='title of the role'
        ),
        'description': fields.String(
            required=True, description='Description of role type'
        ),
        'resourceAccessLevels': fields.List(
            fields.Nested(role_namespace.model('resource_access_levels',{
                'permissionIds': fields.List(fields.String(required=True,
                description='permission IDs')),
                'resourceId': fields.String(required=True, 
                description='Id of the resource')
            }))
        )
    }
)
