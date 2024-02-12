# standard lib
import json

# utilities
from api.utilities.messages.error_messages import query_errors, jwt_errors
from api.utilities.constants import CHARSET

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1


class TestExportStockCountsAsCsv:
    """Tests for exporting stock counts as csv """

    def assert_csv_success(self, response, expected_csv):
        """Helper function to assert whether a csv file has been successfully generated
           Args:
               response(Response): HTTP response
               expected_csv(string): CSV formated string

        """

        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/csv'
        assert response.data.decode('utf-8') == expected_csv

    def test_export_stock_counts_as_csv_with_no_query_should_succeed(
            self, init_db, client, auth_header, new_stock_count):
        """Should return csv data file with stock counts information.

        Args:
            client(FlaskClient): Fixture to get flask test client
            init_db(SQLAlchemy): Fixture to initialize the test database
            auth_header(dict): Fixture to get token
            new_stock_count(object): Fixture to create a stock count
        """

        response = client.get(
            f'{BASE_URL}/stock-count/export', headers=auth_header)

        # Test endpoint returns an empty csv data when there are no stock counts
        assert response.data == b''

        # Test endpoint returns csv data when stock counts are saved in the db
        new_stock_count.save()

        response = client.get(
            f'{BASE_URL}/stock-count/export', headers=auth_header)

        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/csv'
        assert b'Category,Date,Stock Count,User' in response.data
        assert new_stock_count.asset_category.name in response.data.decode()
        assert new_stock_count.user.name in response.data.decode()
        assert str(new_stock_count.count) in response.data.decode()

    def test_export_filtered_stock_counts_as_csv_with_valid_queries_succeeds(
            self, client, init_db, auth_header, new_stock_count):
        """ Test that stock counts are filtered and a csv file is generated when valid queries are passed.

        Args:
            client(FlaskClient): Fixture to get flask test client
            init_db(SQLAlchemy): Fixture to initialize the test database
            auth_header(dict): Fixture to get token
            new_stock_count(object): Fixture to create a stock count
        """

        url = f'{BASE_URL}/stock-count/export'
        new_stock_count.save()
        expected_csv = 'Category,Date,Stock Count,User\r\n' \
                       f'{new_stock_count.asset_category.name},{new_stock_count.created_at.date()},' \
                       f'{new_stock_count.count},{new_stock_count.user.name}\r\n'

        response = client.get(
            f'{url}?assetCategoryId={new_stock_count.asset_category.id}',
            headers=auth_header)
        self.assert_csv_success(response, expected_csv)

        response = client.get(
            f'{url}?week={new_stock_count.week}', headers=auth_header)
        self.assert_csv_success(response, expected_csv)

        response = client.get(
            f'{url}?tokenId={new_stock_count.user.token_id}',
            headers=auth_header)
        self.assert_csv_success(response, expected_csv)

        response = client.get(
            f'{url}?centerId={new_stock_count.center_id}', headers=auth_header)
        self.assert_csv_success(response, expected_csv)

        response = client.get(
            f'{url}?year={new_stock_count.created_at.date().year}',
            headers=auth_header)
        self.assert_csv_success(response, expected_csv)

        response = client.get(
            f'{url}?month={new_stock_count.created_at.date().month}',
            headers=auth_header)
        self.assert_csv_success(response, expected_csv)

        response = client.get(
            f'{url}?year={new_stock_count.created_at.date().year}' + \
            f'&month={new_stock_count.created_at.date().month}',
            headers=auth_header)
        self.assert_csv_success(response, expected_csv)

    def test_export_filtered_stock_counts_as_csv_does_not_return_deleted_stock_counts(
            self, client, init_db, new_stock_count, auth_header):
        """Make sure that deleted stock counts are not returned in the filtered
        results

        Args:
            client(FlaskClient): Fixture to get flask test client
            init_db(SQLAlchemy): Fixture to initialize the test database
            auth_header(dict): Fixture to get token
            new_stock_count(object): Fixture to create a stock count
        """

        new_stock_count.deleted = True
        new_stock_count.save()
        response = client.get(
            f'{BASE_URL}/stock-count/export?assetCategoryId={new_stock_count.asset_category.id}',
            headers=auth_header)
        assert response.headers['Content-Type'] == 'text/csv'
        assert response.data.decode(CHARSET) == ''

    def test_export_filtered_stock_counts_as_csv_with_invalid_query_fails(
            self, client, new_stock_count, auth_header):
        """Test that an error is returned when an invalid query is provided

        Args:
            client(FlaskClient): Fixture to get flask test client
            init_db(SQLAlchemy): Fixture to initialize the test database
            auth_header(dict): Fixture to get token
            new_stock_count(object): Fixture to create a stock count
        """

        response = client.get(
            f'{BASE_URL}/stock-count/export?nam={new_stock_count.asset_category.id}',
            headers=auth_header)
        assert response.status_code == 400
        actual_message = json.loads(response.data)['message']
        expected_message = query_errors['invalid_query_non_existent_column']\
            .format('nam', 'StockCount')
        assert actual_message == expected_message

    def test_export_stock_count_as_csv_with_no_token_should_fail(
            self, client, init_db):
        """Should return a 401 status code and an error message if authorization
        token is not provided in the request header

        Args:
            client(FlaskClient): Fixture to get flask test client
            init_db(SQLAlchemy): Fixture to initialize the test database
        """

        response = client.get(f'{BASE_URL}/stock-count/export')
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']
