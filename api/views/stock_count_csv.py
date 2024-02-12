# Third party
from flask import request
from flask_restplus import Resource
import flask_excel as excel

# Documentation
from api.utilities.swagger.collections.stock_count import stock_count_namespace

# Utilities
from ..middlewares.token_required import token_required
from ..utilities.stock_count_query_parser import StockCountQueryParser
# Resources
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@stock_count_namespace.route('/export')
class ExportStockCountResource(Resource):
    """Resource class for exporting stock count as a csv"""

    @token_required
    @permission_required(Resources.STOCK_COUNT)
    def get(self):
        """Filter and export stock counts to csv"""

        stock_counts = StockCountQueryParser.get_filtered_stock_counts(
            request.args)

        stock_count_data = ({
            'Category': data.asset_category.name,
            'Date': data.created_at.date(),
            'Stock Count': data.count,
            'User': data.user.name
        } for data in stock_counts)

        return excel.make_response_from_records(stock_count_data, 'csv')
