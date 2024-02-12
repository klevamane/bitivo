import json
import datetime as dt
from calendar import monthrange
from dateutil.relativedelta import *

from api.schemas.stock_count import StockCountSchema
from api.utilities.messages.error_messages import \
    (jwt_errors, serialization_errors)
from api.utilities.helpers.get_last_month import get_last_month

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1
URL = f'{BASE_URL}/stock-count'


class TestGetStockCount:
    """Tests for the get stock-count endpoint"""

    @staticmethod
    def format_output(data):
        """Helper method for formatting data into the required form

        Args:
            data (list): The data to be formatted
        """
        formatted = [i for i in StockCountSchema.format_output(data)]
        return json.loads(json.dumps(formatted))

    def test_get_stock_count_properly_formats_data(
            self, init_db, client, save_stock_count, auth_header):
        """The output data should be properly formatted

        Args:
            init_db (func): Initialize test database
            client (func): Flask test client
            save_stock_count (func): Save stock count records
            auth_header (func): Authentication token
        """

        resp = client.get(URL, headers=auth_header)
        resp_data = json.loads(resp.data)['data']
        assert isinstance(resp_data, list)
        for item in resp_data:
            assert 'category' in item
            assert 'id' in item['category']
            assert 'name' in item['category']
            assert 'weeks' in item
            assert len('weeks') > 1
            weeks = item['weeks']
            for week in weeks:
                assert 'date' in weeks[week]
                assert 'count' in weeks[week]
            assert 'lastStockCount' in item
            max_date = max(weeks, key=lambda x: weeks[x]['date'])
            assert item['lastStockCount'] == weeks[max_date]['date']

    def test_get_stock_count_with_pagination_succeeds(
            self, client, auth_header, save_stock_count):
        """Stock-count data should be paginated

        Args:
            client (func): Flask test client
            save_stock_count (func): Save stock count records
            auth_header (func): Authentication token
        """
        resp = client.get(URL, headers=auth_header)
        resp_json = json.loads(resp.data)
        resp_data = resp_json['data']
        meta = resp_json['meta']
        assert resp.status_code == 200
        expected = self.format_output(save_stock_count)
        assert resp_data[0] == expected[0]
        assert meta['firstPage'].endswith('page=1&limit=10')
        assert 'page' not in meta['currentPage']
        assert 'limit' not in meta['currentPage']
        assert meta['nextPage'] == ''
        assert meta['previousPage'] == ''
        assert meta['page'] == 1
        assert 'pagesCount' in meta
        assert 'totalCount' in meta
        assert len(resp_data) <= 10

    def test_get_stock_count_succeeds_with_page_and_limit_queries(
            self, client, auth_header, save_stock_count):
        """Should succeed when page and limit queries are provided

        Args:
            client (func): Flask test client
            save_stock_count (func): Save stock count records
            auth_header (func): Authentication token
        """
        now = dt.datetime.now()
        query = f'?page=1&limit=1&year={now.year}'
        resp = client.get(f'{URL}{query}', headers=auth_header)
        assert resp.status_code == 200
        resp_json = json.loads(resp.data)
        meta = resp_json['meta']
        assert meta['firstPage'].endswith('page=1&limit=1')
        assert 'page=1&limit=1' in meta['currentPage']
        assert meta['previousPage'] == ''
        assert meta['page'] == 1

    def test_get_stock_count_with_invalid_limit_query_fails(
            self, client, auth_header):
        """Should fail when an invalid limit value is provided

        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
        """
        query = f'?page=1&limit=**'
        resp = client.get(f'{URL}{query}', headers=auth_header)
        resp_json = json.loads(resp.data)
        assert resp.status_code == 400
        assert 'meta' not in resp_json
        assert resp_json['status'] == 'error'
        assert resp_json['message'] == serialization_errors[
            'invalid_query_strings'].format('limit', '**')

    def test_get_stock_count_with_invalid_page_query_fails(
            self, client, auth_header):
        """Should fail when an invalid page value is provided

        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
        """
        query = f'?page=**&limit=1'
        resp = client.get(f'{URL}{query}', headers=auth_header)
        resp_json = json.loads(resp.data)
        assert resp.status_code == 400
        assert 'meta' not in resp_json
        assert resp_json['status'] == 'error'
        assert resp_json['message'] == serialization_errors[
            'invalid_query_strings'].format('page', '**')

    def test_get_stock_count_with_exceeded_page_and_limit_succeeds(
            self, client, auth_header):
        """Should succeed with exceeded page and limit values

        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
        """
        query = f'?page=1000&limit=1000'
        resp = client.get(f'{URL}{query}', headers=auth_header)
        resp_json = json.loads(resp.data)
        meta = resp_json['meta']
        assert meta['firstPage'].endswith('page=1&limit=1000')
        assert 'page=1&limit=1' in meta['currentPage']
        assert meta['previousPage'] == ''
        assert meta['page'] == 1
        assert 'pagesCount' in meta
        assert 'totalCount' in meta
        assert meta['message'] == serialization_errors['last_page_returned']

    def test_get_stock_count_with_no_query_succeeds(self, client, auth_header,
                                                    save_stock_count):
        """Should return data even if no query is provided

        Args:
            client (func): Flask test client
            save_stock_count (func): Save stock count records
            auth_header (func): Authentication token
        """
        resp = client.get(URL, headers=auth_header)
        resp_data = json.loads(resp.data)['data']
        assert resp.status_code == 200
        expected = self.format_output(save_stock_count)
        assert resp_data[0] == expected[0]

    def test_get_stock_count_with_asset_category_id_query_succeeds(
            self, client, auth_header, save_stock_count):
        """Should return data filtered by asset category

        Args:
            client (func): Flask test client
            save_stock_count (func): Save stock count records
            auth_header (func): Authentication token
        """
        category_id = save_stock_count[2].asset_category_id
        query = f'assetCategoryId={category_id}'
        resp = client.get(f'{URL}?{query}', headers=auth_header)
        resp_data = json.loads(resp.data)['data']
        stock_counts = [
            sc for sc in save_stock_count
            if sc.asset_category_id == category_id
        ]
        expected = self.format_output(stock_counts)
        assert resp.status_code == 200
        assert resp_data[0] == expected[0]
        assert resp_data[0]['category']['id'] == category_id

    def test_get_stock_count_with_valid_month_query_succeeds(
            self, client, auth_header, save_stock_count):
        """Should return data filtered by month

        Args:
            client (func): Flask test client
            save_stock_count (func): Save stock count records
            auth_header (func): Authentication token
        """
        month = save_stock_count[0].created_at.month
        query = f'month={month}'
        resp = client.get(f'{URL}?{query}', headers=auth_header)
        resp_data = json.loads(resp.data)['data']
        stock_counts = [
            sc for sc in save_stock_count if sc.created_at.month == month
        ]
        expected = self.format_output(stock_counts)
        assert resp.status_code == 200
        assert resp_data[0] == expected[0]

    def test_get_stock_count_with_valid_year_query_succeeds(
            self, client, auth_header, save_stock_count):
        """Should return data filtered by year

        Args:
            client (func): Flask test client
            save_stock_count (func): Save stock count records
            auth_header (func): Authentication token
        """
        year = dt.datetime.now().date().year
        query = f'year={year}'
        resp = client.get(f'{URL}?{query}', headers=auth_header)
        resp_data = json.loads(resp.data)['data']
        stock_counts = [
            sc for sc in save_stock_count if sc.created_at.year == year
        ]
        expected = self.format_output(stock_counts)
        assert resp.status_code == 200
        assert resp_data[0] == expected[0]

    def test_get_stock_count_with_invalid_year_query_fails(
            self, client, auth_header):
        """Should fail when an invalid year is provided

        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
        """
        year = 201
        query = f'year={year}'
        resp = client.get(f'{URL}?{query}', headers=auth_header)
        resp_json = json.loads(resp.data)
        assert resp.status_code == 400
        assert resp_json['status'] == 'error'
        assert resp_json['message'] == serialization_errors['invalid_period']\
            .format('year')

    def test_get_stock_count_with_invalid_month_query_fails(
            self, client, auth_header):
        """Should fail when an invalid month is provided

        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
        """
        month = 13
        query = f'month={month}'
        resp = client.get(f'{URL}?{query}', headers=auth_header)
        resp_json = json.loads(resp.data)
        assert resp.status_code == 400
        assert resp_json['status'] == 'error'
        assert resp_json['message'] == serialization_errors['invalid_period']\
            .format('month')

    def test_get_stock_count_with_week_query_succeeds(
            self, client, auth_header, save_stock_count):
        """Should return data filtered by week

        Args:
            client (func): Flask test client
            save_stock_count (func): Save stock count records
            auth_header (func): Authentication token
        """
        # individual week
        week = 2
        query = f'week={week}'
        resp = client.get(f'{URL}?{query}', headers=auth_header)
        resp_data = json.loads(resp.data)['data']
        stock_counts = [sc for sc in save_stock_count if sc.week == week]
        expected = self.format_output(stock_counts)
        assert resp.status_code == 200
        assert resp_data[0] == expected[0]
        assert '2' in resp_data[0]['weeks']

        # week range
        weeks = (2, 3)
        query = f'startWeek=2&endWeek=3'
        resp = client.get(f'{URL}?{query}', headers=auth_header)
        resp_data = json.loads(resp.data)['data']
        stock_counts = [
            sc for sc in save_stock_count if weeks[0] <= sc.week <= weeks[1]
        ]
        expected = self.format_output(stock_counts)
        assert resp.status_code == 200
        assert resp_data[0] == expected[0]
        assert '2' in resp_data[0]['weeks']

    def test_get_stock_count_with_pagination_query_false_succeeds(
            self, client, auth_header):
        """Should return all data without pagination

        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
        """
        pagination = False
        query = f'pagination={pagination}'
        resp = client.get(f'{URL}?{query}', headers=auth_header)
        resp_data = json.loads(resp.data)
        assert resp.status_code == 200
        assert resp_data['meta'] is None

    def test_get_stock_with_token_id_query_succeeds(self, client, auth_header,
                                                    save_stock_count):
        """Should return data filtered by token id

        Args:
            client (func): Flask test client
            save_stock_count (func): Save stock count records
            auth_header (func): Authentication token
        """
        token_id = save_stock_count[0].token_id
        query = f'tokenId={token_id}'
        resp = client.get(f'{URL}?{query}', headers=auth_header)
        resp_data = json.loads(resp.data)['data']
        stock_counts = [
            sc for sc in save_stock_count if sc.token_id == token_id
        ]
        expected = self.format_output(stock_counts)
        assert resp.status_code == 200
        assert resp_data[0] == expected[0]

    def test_get_stock_count_with_center_id_query_succeeds(
            self, client, auth_header, save_stock_count):
        """Should return data filtered by center id

        Args:
            client (func): Flask test client
            save_stock_count (func): Save stock count records
            auth_header (func): Authentication token
        """
        center_id = save_stock_count[1].center_id
        query = f'centerId={center_id}'
        resp = client.get(f'{URL}?{query}', headers=auth_header)
        resp_data = json.loads(resp.data)['data']
        stock_counts = [
            sc for sc in save_stock_count if sc.center_id == center_id
        ]
        expected = self.format_output(stock_counts)
        assert resp.status_code == 200
        assert resp_data[0] == expected[0]

    def test_get_stock_count_with_count_query_succeeds(
            self, client, auth_header, save_stock_count):
        """Should return data filtered by count

        Args:
            client (func): Flask test client
            save_stock_count (func): Save stock count records
            auth_header (func): Authentication token
        """
        count = (20, 30)
        query = f'startCount=20&endCount=30'
        resp = client.get(f'{URL}?{query}', headers=auth_header)
        resp_data = json.loads(resp.data)['data']
        stock_counts = [
            sc for sc in save_stock_count if count[0] <= sc.count <= count[1]
        ]
        expected = self.format_output(stock_counts)
        assert resp.status_code == 200
        assert resp_data[0] == expected[0]
        assert resp_data[0]['weeks']['2']['count'] == count[0]

    def test_get_stock_count_with_date_query_succeeds(
            self, client, auth_header, save_stock_count):
        """Test that providing a date range works as expected

        Args:
            client (func): Flask test client
            save_stock_count (func): Save stock count records
            auth_header (func): Authentication token
        """
        now = dt.datetime.now()
        last_month = dt.datetime.now() - relativedelta(months=3)
        start_date = str(last_month.date())
        end_day = monthrange(now.year, now.month)[1]
        end_date = f'{now.year}-{now.month}-{end_day}'
        query = f'startCreatedAt={start_date}&endCreatedAt={end_date}'
        resp = client.get(f'{URL}?{query}', headers=auth_header)
        resp_data = json.loads(resp.data)['data']
        assert resp.status_code == 200
        assert len(resp_data) == 2
        assert start_date < resp_data[0]['lastStockCount'] < end_date
        assert start_date < resp_data[1]['lastStockCount'] < end_date

    def test_get_stock_count_with_multiple_queries_succeeds(
            self, client, auth_header, save_stock_count):
        """Should return the proper data when multiple filters are applied

        Args:
            client (func): Flask test client
            save_stock_count (func): Save stock count records
            auth_header (func): Authentication token
        """
        category_id = save_stock_count[0].asset_category_id
        month = save_stock_count[0].created_at.month
        year = save_stock_count[0].created_at.year
        queries = f'assetCategoryId={category_id}&month={month}&year={year}'
        resp = client.get(f'{URL}?{queries}', headers=auth_header)
        resp_data = json.loads(resp.data)['data']
        stock_counts = [
            sc for sc in save_stock_count
            if sc.asset_category_id == category_id
            and sc.created_at.month == month and sc.created_at.year == year
        ]
        expected = self.format_output(stock_counts)
        assert resp.status_code == 200
        assert resp_data[0] == expected[0]

    def test_get_stock_count_with_non_matching_query_succeeds(
            self, client, save_stock_count, auth_header):
        """Should return an empty response when no results are found

        Args:
            client (func): Flask test client
            save_stock_count (func): Save stock count records
            auth_header (func): Authentication token
        """
        category_id = 'qwerty'
        query = f'assetCategoryId={category_id}'
        resp = client.get(f'{URL}?{query}', headers=auth_header)
        resp_data = json.loads(resp.data)['data']
        assert resp.status_code == 200
        assert isinstance(resp_data, list)
        assert resp_data == []

    def test_get_stock_count_with_no_token_fails(self, client):
        """Should fail when no toked is provided in the request

        Args:
            client (func): Flask test client
        """
        resp = client.get(URL)
        resp_json = json.loads(resp.data)
        assert resp.status_code == 401
        assert resp_json['status'] == 'error'
        assert resp_json['message'] == jwt_errors['NO_TOKEN_MSG']
