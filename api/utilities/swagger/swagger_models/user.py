"""
Model Definition for user collection
"""
from flask_restplus import fields
from ..collections.user import user_namespace

user_model = user_namespace.model(
    "user_model", {
        "name": fields.String(required=True, description="user's name"),
        "email": fields.String(required=True, description="email"),
        "centerId": fields.String(required=True, description="center ID"),
        "roleId": fields.String(required=True, description="role ID"),
        "tokenId": fields.String(required=True, description="token ID"),
        "image_url": fields.String(required=True, description="link to image")
    }
)
