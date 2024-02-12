"""
Model Definition for space type collection
"""

from flask_restplus import fields

from ..collections.space_type import space_namespace

space_models = space_namespace.model(
    "space_models", {
        'name': fields.String(
            required=True, description='space name'),
        'centerId': fields.String(
            required=True, description='center id'),
        'spaceTypeId': fields.String(
            required=True, description='space type id'),
        'parentId': fields.String(
            required=True, description='parent id'),
    }
)

