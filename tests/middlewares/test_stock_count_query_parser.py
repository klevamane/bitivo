from pytest import raises
from werkzeug.datastructures import ImmutableMultiDict
from api.utilities.stock_count_query_parser import StockCountQueryParser
from api.models.stock_count import StockCount
from api.middlewares.base_validator import ValidationError
from api.utilities.messages.error_messages import serialization_errors


class TestStockCountQueryParser:
    """Test the functionality of stock count query parser for parsing year and month in query"""

    def asserts_for_success(self, request_args, stock_count):
        """Helper function for asserting success
         Args:
            request_args (ImmutableMultiDict):  Request arguments
            stock_count (str): Stock count instance

        Returns:
            None
        """
        column_filters, year_filter, month_filter = StockCountQueryParser.parse_all(
            StockCount, request_args)

        stock_counts = StockCount.query_(column_filters).filter(
            year_filter).filter(month_filter)

        assert stock_counts.count() == 1

        assert stock_counts.first(
        ).asset_category_id == stock_count.asset_category_id

    def test_valid_year_and_month_in_query_succeeds(self, init_db,
                                                    new_stock_count):
        """Should pass successfully if the query provided is valid

        Args:
            init_db (SQLAlchemy): Fixture to initialize the test database
            new_stock_count (): Fixture for creating stock count
        """

        new_stock_count.save()

        request_args = ImmutableMultiDict(
            [('year', f'{new_stock_count.created_at.date().year}'),
             ('month', f'{new_stock_count.created_at.date().month}')])

        self.asserts_for_success(request_args, new_stock_count)

    def test_valid_year_in_query_succeeds(self, init_db, new_stock_count):
        """Should pass successfully if the year in query provided is valid

        Args:
            init_db (SQLAlchemy): Fixture to initialize the test database
            new_stock_count (): Fixture for creating stock count
        """

        new_stock_count.save()

        request_args = ImmutableMultiDict(
            [('year', f'{new_stock_count.created_at.date().year}')])

        self.asserts_for_success(request_args, new_stock_count)

    def test_valid_month_in_query_succeeds(self, init_db, new_stock_count):
        """Should pass successfully if the month in query provided is valid

        Args:
            init_db (SQLAlchemy): Fixture to initialize the test database
            new_stock_count (): Fixture for creating stock count
        """

        new_stock_count.save()

        request_args = ImmutableMultiDict(
            [('month', f'{new_stock_count.created_at.date().month}')])

        self.asserts_for_success(request_args, new_stock_count)

    def test_invalid_year_in_query_fails(self, init_db):
        """Should fail if the year provided in query is invalid

        Args:
            init_db (SQLAlchemy): Fixture to initialize the test database
        """

        request_args = ImmutableMultiDict([('year', '0')])
        with raises(ValidationError) as error:
            StockCountQueryParser.parse_all(StockCount, request_args)

        assert error.value.status_code == 400
        assert error.value.error['status'] == 'error'
        assert error.value.error['message'] == serialization_errors[
            'invalid_period'].format('year')

    def test_invalid_month_in_query_fails(self, init_db):
        """Should fail if the month provided in query is invalid

        Args:
            init_db (SQLAlchemy): Fixture to initialize the test database
        """

        request_args = ImmutableMultiDict([('month', '0')])
        with raises(ValidationError) as error:
            StockCountQueryParser.parse_all(StockCount, request_args)

        assert error.value.status_code == 400
        assert error.value.error['status'] == 'error'
        assert error.value.error['message'] == serialization_errors[
            'invalid_period'].format('month')
