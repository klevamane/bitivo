"""Tests for analytics report"""

# Standard Library
import json
from datetime import timedelta, datetime, date

# Local Module
from api.utilities.messages.error_messages import serialization_errors
from api.utilities.constants import CHARSET

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1
stock_level_url_with_dates = BASE_URL + '/assets/analytics?report=stockLevel' \
                                        '&startDate={}&endDate={}'
stock_level_url = BASE_URL + '/assets/analytics?report=stockLevel'


class TestAssetAnalyticsStockLevelEndpoints:
    """Test for asset analytics stock level endpoint"""

    def test_for_all_stock_level_report_succeeds(
            self,
            client,
            auth_header,
            init_db,
            save_stock_count,
    ):
        """Should return a list with the stock level reports
        Tests that the stockCount, runningLow, lowInStock, priority,
        name are returned when getting the report

        Args:
            save_stock_count (func): to create new stock counts for 4 weeks
            client (func): Flask test client
            init_db (func): Initialize the database
            auth_header (func): Authentication token

        Returns:
            None

        """

        response = client.get(
            stock_level_url,
            headers=auth_header,
        )
        response_json = json.loads(response.data.decode(CHARSET))['data']
        stock_level = response_json['stockLevel'][0]
        assert response.status_code == 200
        assert 'stockLevel' in response_json
        assert 'stockCount' in stock_level
        assert 'runningLow' in stock_level
        assert 'name' in stock_level
        assert 'lowInStock' in stock_level
        assert 'priority' in stock_level
        assert 'expectedBalance' in stock_level

    def test_for_stock_level_report_with_only_start_date_succeeds(
            self, client, auth_header):
        """Should return a 200 response
        Tests that the stockCount, runningLow, lowInStock, priority,
        name are returned as list when getting the report with only
        the start date

        Args:
            client (func): Flask test client
            auth_header (func): Authentication token

        Returns:
            None

        """

        stock_level_url = BASE_URL + '/assets/analytics?report=stockLevel' \
                                     '&startDate={}'

        response = client.get(
            stock_level_url.format(date.today()),
            headers=auth_header,
        )
        response_json = json.loads(response.data.decode(CHARSET))['data']
        stock_level = response_json['stockLevel'][0]
        assert response.status_code == 200
        assert 'stockLevel' in response_json
        assert 'stockCount' in stock_level
        assert 'runningLow' in stock_level
        assert 'name' in stock_level
        assert 'lowInStock' in stock_level
        assert 'priority' in stock_level
        assert 'expectedBalance' in stock_level

    def test_stock_level_report_within_a_date_range_succeeds(
            self, client, auth_header):
        """Should return a 200 response
        Tests that the right stockCount, runningLow, lowInStock, priority,
        name are returned when getting the report within a date range

        Args:
            client (func): Flask test client
            auth_header (func): Authentication token

        Returns:
            None

        """
        start_date = date.today() - timedelta(days=14)
        end_date = date.today() - timedelta(days=7)

        response = client.get(
            stock_level_url_with_dates.format(start_date, end_date),
            headers=auth_header,
        )
        response_json = json.loads(response.data.decode(CHARSET))['data']
        stock_level = response_json['stockLevel'][0]
        assert response.status_code == 200
        assert 'stockLevel' in response_json
        assert isinstance(stock_level['stockCount'], int)
        assert isinstance(stock_level['runningLow'], int)
        assert isinstance(stock_level['lowInStock'], int)
        assert isinstance(stock_level['priority'], str)
        assert isinstance(stock_level['name'], str)
        assert isinstance(stock_level['expectedBalance'], int)

    def test_for_stock_level_report_with_invalid_end_date_fails(
            self, client, auth_header):
        """Should return a 400 error when the end date passed is a date
        that is not greater than the current date.

        Args:
            client (func): Flask test client
            auth_header (func): Authentication token

        Returns:
            None

        """

        stock_level_url = BASE_URL + '/assets/analytics?report=stockLevel' \
                                     '&endDate={}'

        response = client.get(
            stock_level_url.format(date.today() - timedelta(days=1)),
            headers=auth_header,
        )
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_end_date']

    def test_for_stock_level_report_with_invalid_start_date_fails(
            self, client, auth_header):
        """Should return a 400 error when the start date passed is a date
        that is greater than the current date.

        Args:
            client (func): Flask test client
            auth_header (func): Authentication token

        Returns:
            None

        """

        stock_level_url = BASE_URL + '/assets/analytics?report=stockLevel' \
                                     '&startDate={}'

        response = client.get(
            stock_level_url.format(date.today() + timedelta(days=1)),
            headers=auth_header,
        )
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_start_date']

    def test_for_invalid_date_range_fails(self, client, auth_header):
        """Should return a 400 response
        Tests that the start date is not greater than the end date

        Args:
            client (func): Flask test client
            auth_header (func): Authentication token

        Returns:
            None

        """

        response = client.get(
            stock_level_url_with_dates.format(date.today(),
                                              date.today() - timedelta(7)),
            headers=auth_header,
        )
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_date_range']

    def test_for_invalid_date_format_fails(self, client, auth_header):
        """Should return a 400 response
        Tests that the dates are in the right format

        Args:
            client (func): Flask test client
            auth_header (func): Authentication token

        Returns:
            None

        """
        today = datetime.today()

        response = client.get(
            stock_level_url_with_dates.format(today,
                                              date.today() - timedelta(7)),
            headers=auth_header,
        )
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_date'].format(today)
