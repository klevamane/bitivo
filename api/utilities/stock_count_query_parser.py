# Standard library
from datetime import datetime

# SQLAlchemy
from sqlalchemy import extract, text

# Models
from api.models import StockCount, AssetCategory

# Query Parser
from api.utilities.query_parser import QueryParser

# Error
from api.utilities.error import raises


class StockCountQueryParser(QueryParser):
    """Extends QueryParser to handle month and year queries"""

    QueryParser.excluded_keys.extend(['month', 'year'])

    @classmethod
    def validate_date_value(cls, value, op, period):
        """Validator for checking whether month or year queries are valid

        Args:
            value (str): The query value to validate
            op (str): The datetime.strptime op to use
            period (str): The serialization error key to use
        """
        if value:
            try:
                datetime.strptime(value, op)
            except ValueError:
                raises('invalid_period', 400, period)

    @classmethod
    def parse_all(cls, model, url_queries):
        """Parse the stock count queries

        This method extends the query parser method `parse_all` to cater for
        the month and the year fields which are not valid table columns

        Args:
            model (object): The model for which the filters are to be generated
            url_queries (dict): The url query arguments

        Returns:
            tuple: A tuple with the appropriate filters
        """
        column_filters = QueryParser.parse_all(model, url_queries)
        month = url_queries.get('month')
        year = url_queries.get('year')
        cls.validate_date_value(month, '%m', 'month')
        cls.validate_date_value(year, '%Y', 'year')
        date_filters = {
            'month': extract('month', StockCount.created_at) == month,
            'year': extract('year', StockCount.created_at) == year
        }
        if month and year:
            return column_filters, date_filters['month'], date_filters['year']
        if month:
            return column_filters, date_filters['month'], text('')
        if year:
            return column_filters, text(''), date_filters['year']
        return column_filters, text(''), text('')

    @classmethod
    def get_filtered_stock_counts(cls, url_queries, include_deleted=False):
        column_filters, month_filter, year_filter = \
            cls.parse_all(StockCount, url_queries)

        raw_stock_counts = StockCount.query_(column_filters, include_deleted=include_deleted) \
            .join(AssetCategory) \
            .filter(StockCount.deleted == False) \
            .filter(month_filter, year_filter)

        return raw_stock_counts
