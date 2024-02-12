"""Module that handles asset-related operations"""
# standard libraries
from flask import request
from flask_restplus import Resource

# models
from api.models import (Asset, HotDeskRequest, User, WorkOrder)

# Decorators
from api.middlewares.token_required import token_required

# schemas
from api.schemas.asset import AssetSchema
from api.schemas.hot_desk import HotDeskRequestSchema
from api.schemas.user import UserSchema
from api.schemas.work_order import WorkOrderSchema

# Utilities
from ..utilities.constants import EXCLUDED_FIELDS
from ..utilities.validators.search_validator import validate_search_query_param
from ..utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.swagger.collections.global_search import global_search_namespace
from api.middlewares.permission_required import Resources
from ..middlewares.permission_required import permission_required


@global_search_namespace.route('/')
class SearchResource(Resource):
    """Resource for search assets endpoints."""

    @token_required
    @permission_required(Resources.ASSETS)
    @global_search_namespace.doc(
        params={"q": {
            "description": "The search criteria",
            "required": True
        }})
    def get(self):
        """
        Global Search endpoint 
        """

        qry_dict = request.args.to_dict()
        text = qry_dict.get('q')
        validate_search_query_param(request)
        results = GlobalSearch.search(text=text)
        return {
            'message':
            SUCCESS_MESSAGES['successfully_fetched'].format('search results'),
            'status':
            'success',
            'data':
            results
        }, 200


class GlobalSearch:
    @staticmethod
    def search(text):
        """
        Function to implement full text search

        Args:
            text : The search criteria provided
        """
        categories_mapper = {
            'asset': [Asset, AssetSchema],
            'hot_desk': [HotDeskRequest, HotDeskRequestSchema],
            'user': [User, UserSchema],
            'work_order': [WorkOrder, WorkOrderSchema]
        }
        excluded = EXCLUDED_FIELDS.copy()
        excluded.extend(['assigned_by', 'custom_attributes', 'updated_at'])
        results = []
        for each in categories_mapper:
            result = {}
            model, schema = categories_mapper[each]
            model_query = model.query_()
            model_schema = schema(many=True, exclude=excluded)
            result[model.__name__.lower() + 's'] = model_schema.dump(
                model_query.search(text).all()).data
            results.append(result)
        return results
