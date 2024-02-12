"""Tests for analytics report"""

# Standard Library
import json
from datetime import date, timedelta

# Local Module
from api.utilities.messages.error_messages import serialization_errors, jwt_errors
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.constants import CHARSET, ASSET_REPORT_QUERIES

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1
analytics_url = BASE_URL + '/assets/analytics?report={}'


class TestAssetAnalytics:
    def asserts_for_success(self, response, query, new_user):
        """Helper function for asserting success
        Args:
            self (class):  This class instance
            response (class): Response object
            query (str): Report query string
        Returns:
            None
        """
        new_user.save()
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['message'] == SUCCESS_MESSAGES[
            'asset_report'].format(query)
        assert 'data' in response_json
        assert query in response_json['data']

    def test_asset_flow_method_is_called(self, client, init_db,
                                         auth_header_two, new_user):
        """Tests that asset flow method should be called
        Args:
            self (class):  Instance of this class
            client (func): Flask test client
            auth_header_two (func): Authentication token
        Returns:
            None
        """
        new_user.save()
        query = 'assetFlow'
        response = client.get(
            analytics_url.format(query),
            headers=auth_header_two,
        )

        self.asserts_for_success(response, query, new_user)

    def test_asset_inflow_method_is_called(self, client, init_db,
                                           auth_header_two, new_user):
        """Tests that asset inflow method should be called
        Args:
            self (class):  Instance of this class
            client (func): Flask test client
            auth_header_two (func): Authentication token
        Returns:
            None
        """
        new_user.save()
        query = 'assetInflow'
        response = client.get(
            analytics_url.format(query),
            headers=auth_header_two,
        )

        self.asserts_for_success(response, query, new_user)

    def test_asset_outflow_method_is_called(self, client, auth_header_two,
                                            init_db, new_user):
        """Tests that asset outflow method should be called
        Args:
            self (class):  Instance of this class
            client (func): Flask test client
            auth_header_two (func): Authentication token
        Returns:
            None
        """
        new_user.save()
        query = 'assetOutflow'
        response = client.get(
            analytics_url.format(query),
            headers=auth_header_two,
        )

        self.asserts_for_success(response, query, new_user)

    def test_asset_stock_level_method_is_called(self, client, init_db,
                                                auth_header_two, new_user):
        """Tests that stock level method should be called
        Args:
            self (class):  Instance of this class
            client (func): Flask test client
            auth_header_two (func): Authentication token
        Returns:
            None
        """
        new_user.save()
        query = 'stockLevel'
        response = client.get(
            analytics_url.format(query),
            headers=auth_header_two,
        )

        self.asserts_for_success(response, query, new_user)

    def test_all_report_methods_are_called_without_report_query(
            self, client, init_db, auth_header_two):
        """Tests that are the report methods should be called
        Args:
            self (class):  Instance of this class
            client (func): Flask test client
            auth_header_two (func): Authentication token
        Returns:
            None
        """
        analytics_url = BASE_URL + '/assets/analytics'
        response = client.get(
            analytics_url,
            headers=auth_header_two,
        )

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert 'assetFlow' in response_json['data']
        assert 'assetOutflow' in response_json['data']
        assert 'assetInflow' in response_json['data']
        assert 'stockLevel' in response_json['data']

    def test_invalid_report_query_fails(self, client, auth_header_two,
                                        init_db):
        """Should return a 400 response
        Tests that a 400 response is thrown when the report query is
        not one of assetFlow, assetInflow, assetOutflow, stockLevel
        Args:
            self (class):  Instance of this class
            client (func): Flask test client
            auth_header_two (func): Authentication token
        Returns:
            None
        """

        response = client.get(
            analytics_url,
            headers=auth_header_two,
        )

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json[
            'message'] == serialization_errors['invalid_request_param'].format(
                'report query', ', '.join(ASSET_REPORT_QUERIES))

    def test_get_report_should_fail_when_token_is_not_provided(
            self, client, init_db):
        """Should return a 401 error code when
        getting reports without authorization
        Args:
            self (class):  Instance of this class
            client (func): Flask test client
        Returns:
            None
        """
        response = client.get(analytics_url)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_get_asset_flow_with_start_and_end_date_success(
            self, client, init_db, auth_header_two,
            new_data_for_asset_flows_test):
        """
        Should return a dictionary with asset flow report when
        start and end date is present
          Args:
            client (func): Flask test client
            auth_header_two (func): Authentication token
         Returns:
            None
        """
        asset_flow_url = analytics_url + \
                         '&startDate={}&endDate={}'
        response = client.get(
            asset_flow_url.format('assetFlow',
                                  date.today() - timedelta(7), date.today()),
            headers=auth_header_two)
        response_json = json.loads(
            response.data.decode(CHARSET))['data']['assetFlow']
        assert response.status_code == 200
        assert 'outflow' in response_json
        assert 'inflow' in response_json
        assert 'reconciliation' in response_json
        assert response_json['outflow'] == 2
        assert response_json['inflow'] == 1
        assert response_json['reconciliation'] == 1

    def test_get_asset_flow_without_start_and_end_date_success(
            self, client, init_db, auth_header_two):
        """
        Should return a dictionary with asset flow report when
        start and end date is present
          Args:
            client (func): Flask test client
            auth_header_two (func): Authentication token
            init_db: Initialize the test db
         Returns:
            None
        """
        response = client.get(
            analytics_url.format('assetFlow'), headers=auth_header_two)
        response_json = json.loads(
            response.data.decode(CHARSET))['data']['assetFlow']
        assert response.status_code == 200
        assert 'outflow' in response_json
        assert 'inflow' in response_json
        assert 'reconciliation' in response_json

    def test_get_asset_flow_without_end_date_success(self, client, init_db,
                                                     auth_header_two):
        """
        Should return a dictionary with asset flow report when
        start and end date is present
          Args:
            client (func): Flask test client
            auth_header_two (func): Authentication token
            init_db: Initialize the test db
         Returns:
            None
        """
        asset_flow_url = analytics_url + \
                         '&startDate={}'
        response = client.get(
            asset_flow_url.format('assetFlow',
                                  date.today() - timedelta(days=7)),
            headers=auth_header_two)
        response_json = json.loads(
            response.data.decode(CHARSET))['data']['assetFlow']
        assert response.status_code == 200
        assert 'outflow' in response_json
        assert 'inflow' in response_json
        assert 'reconciliation' in response_json

    def test_get_asset_flow_where_end_date_lesser_than_start_date_failure(
            self, client, init_db, auth_header_two):
        """
        Should return a dictionary with asset flow report when
        start and end date is present
          Args:
            client (func): Flask test client
            auth_header_two (func): Authentication token
            init_db: Initialize the test db
         Returns:
            None
        """
        asset_flow_url = analytics_url + \
                         '&startDate={}&endDate={}'
        response = client.get(
            asset_flow_url.format('assetFlow', date.today(),
                                  date.today() - timedelta(days=7)),
            headers=auth_header_two)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert 'message' in response_json
        assert response_json['message'] == serialization_errors[
            'invalid_date_range']

    def test_get_asset_flow_with_invalid_date_type_failure(
            self, client, init_db, auth_header_two):
        """
        Should return a dictionary with asset flow report when
        start and end date is present
          Args:
            client (func): Flask test client
            auth_header_two (func): Authentication token
            init_db: Initialize the test db
         Returns:
            None
        """
        asset_flow_url = analytics_url + \
                         '&startDate={}&endDate={}'
        response = client.get(
            asset_flow_url.format('assetFlow', '111-2-01', '111-2-08'),
            headers=auth_header_two)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['message'] == serialization_errors[
            'invalid_date'].format('111-2-01')
