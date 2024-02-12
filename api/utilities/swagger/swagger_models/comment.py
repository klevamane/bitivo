"""
Model Definition for comment collection
"""

from flask_restplus import fields
from ..collections.comment import comment_namespace


# swagger model that defines comment fields
comment_model = comment_namespace.model(
    "comment", {
        'body': fields.String(
            required=True, description='comment body'
        ),
        'parentId': fields.String(
            required=True, description='the id of the comment owner'
        ),
        'parentType': fields.String(
            required=True, description='the type of the comment'
        ),
        'authorId': fields.String(
            required=True, description='the id of the user'
        )
    }
)
