"""
Model Definition for sheet transformers collection
"""

from flask_restplus import fields

from ..collections.sheet_transformer import sheet_transform_namespace

sheet_transform_models = sheet_transform_namespace.model(
    "sheet_transform_models", {
        'doc-name': fields.String(
            required=True, description='upload document'),
        'email': fields.String(
            required=True, description='email address')
    }
)
