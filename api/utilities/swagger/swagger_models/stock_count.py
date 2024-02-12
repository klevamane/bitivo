"""
Model Definition for stock count collection
"""

from flask_restplus import fields

from ..collections.stock_count import stock_count_namespace

stock_count_models = stock_count_namespace.model(
    "stock_count_models", {
        'tokenId': fields.String(
            required=True, description='token id'),
        'stockCount': fields.List(
            fields.Nested(stock_count_namespace.model(
                "assets_model", {
                    'assetCategoryId': fields.String(
                        required=True, description='asset category id'),
                    'count': fields.String(
                        required=True, description='count'),
                    'week': fields.String(
                        required=True, description='week')
                    }
            ))
        )
    }
)
