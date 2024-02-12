# Standard library
import datetime

# Flask
from flask import request
from flask_restplus import Resource

# Paginator
from api.utilities.paginator import list_paginator

# Documentation
from api.utilities.swagger.collections.stock_count import stock_count_namespace
from api.utilities.swagger.swagger_models.stock_count import stock_count_models
from api.utilities.swagger.constants import PAGINATION_PARAMS

# Models
from ..models import StockCount, User

# Schemas
from ..schemas.stock_count import StockCountSchema

# Middleware
from ..middlewares.token_required import token_required

# Utilities
from ..utilities.validators.validate_json_request import validate_json_request
from ..utilities.validators.stock_count_validators import StockCountValidator
from api.utilities.validators.validate_id import validate_id

# Messages
from ..utilities.messages.success_messages import SUCCESS_MESSAGES

# Constants
from ..utilities.constants import EXCLUDED_FIELDS

# Query parser
from api.utilities.stock_count_query_parser import StockCountQueryParser
from ..utilities.helpers.resource_manipulation_for_delete import delete_by_id
# Resources
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@stock_count_namespace.route('/')
class StockCountResource(Resource):
    """
    Resource class for asset category stock count.
    """

    @token_required
    @permission_required(Resources.STOCK_COUNT)
    @validate_json_request
    @stock_count_namespace.expect(stock_count_models)
    def post(self):
        """Record asset category stock count.
         Returns:
            (dict): Returns status and success message.
                data(dict): Returns stock count details created.
        """

        request_data = request.get_json()

        excluded = EXCLUDED_FIELDS.copy() + ['updated_at', 'created_at']

        # Validate 'stockCount' list in request_data.
        StockCountValidator.validate_stock_count_list(request_data)

        stock_count_list = request_data['stockCount']

        # Extracts token_id from request token.
        token_id = request.decoded_token['UserInfo']['id']

        stock_taker = User.get_or_404(token_id)

        week_list = []
        stock_count_records = []
        # Add userId & centerId to each item in the stockCountList
        for stock_count_item in stock_count_list:
            stock_count_item.update({
                'tokenId': token_id,
                'centerId': stock_taker.center_id
            })
            week_list.append(stock_count_item.get('week'))
            stock_count_records.append(stock_count_item['assetCategoryId'])

        stock_count_schema = StockCountSchema(
            exclude=excluded,
            many=True,
            context={
                'asset_category_id_set': set(),
                'week_list': week_list
            })

        stock_count_data = stock_count_schema\
            .load_object_into_schema(stock_count_list)

        stock_count_data = StockCount.bulk_create(stock_count_data)

        return {
            'status':
            'success',
            'message':
            SUCCESS_MESSAGES['recorded'].format('Stock count'),
            'data': [
                record
                for record in StockCountSchema.format_output(stock_count_data)
            ]
        }, 201

    @token_required
    @permission_required(Resources.STOCK_COUNT)
    @stock_count_namespace.doc(params=PAGINATION_PARAMS)
    def get(self):
        """View function for the GET request
        Returns:
            dict: The response with the stock count data
        """
        return return_stock_count(request)


@stock_count_namespace.route('/<string:stock_count_id>')
class SingleStockCountResource(Resource):
    @token_required
    @permission_required(Resources.STOCK_COUNT)
    @validate_id
    def delete(self, stock_count_id):
        """Soft deletes the stock count
        Args:
            stock_count_id: The id of the stock count to be deleted
        Returns:
            dict: A success status and a message of successful deletion of
            the stock count
        """
        return delete_by_id(StockCount, stock_count_id, 'Stock count')


def return_stock_count(request):
    """Function to get stock count
    Args:
        request(object): global request object
    Returns:
        dict: The response with the stock count data
    """

    date_args = ('month', 'year', 'startCreatedAt', 'endCreatedAt')
    date_queries = list(map(request.args.get, date_args))
    url_queries = request.args.to_dict()
    paginate_value = url_queries.pop('pagination', None)
    include = url_queries.get('include')

    if isinstance(paginate_value, str) and paginate_value.lower() == 'false':
        paginate_value = False

    # if there are no date queries we default to the current month, year
    if not any(date_queries):
        now = datetime.datetime.now()
        url_queries['month'] = str(now.month)
        url_queries['year'] = str(now.year)

    raw_stock_counts = StockCountQueryParser.get_filtered_stock_counts(
        url_queries, include_deleted=True)

    raw_stock_counts = raw_stock_counts if include == 'deleted' else \
        StockCountQueryParser.get_filtered_stock_counts(
            url_queries)

    formatted = [
        data for data in StockCountSchema.format_output(raw_stock_counts)
    ]
    results, meta = list_paginator(formatted, paginate=paginate_value)

    return {
        'message': 'Stock count received',
        'status': 'success',
        'data': results,
        'meta': meta
    }
