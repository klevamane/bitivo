"""Test file for asset repair log"""
from flask import json

from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import jwt_errors
from api.utilities.constants import CHARSET

# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestAssetRepairLog:
    """Test class for getting asset repair log"""

    def test_get_asset_repair_logs_when_no_repair_logs_succeeds(
            self, auth_header, client, new_asset_repair_log):
        """
        Test get asset repair logs when no repair logs succeeds
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            new_asset_repair_log: Fixture to create an object
            of asset repait log
         Returns:
            None
        """
        response = client.get(
            f'{API_BASE_URL_V1}/repair-logs', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['fetched'].format(
            'Repair logs')

        assert isinstance(response_json['data'], list)
        assert isinstance(response_json, dict)
        assert response_json['meta'] is not None
        assert response_json['data'] == []

    def test_get_asset_repair_log_with_pagination_succeeds(
            self, auth_header, client, new_asset_repair_log):
        """
        Test get asset repair log with pagination succeeds
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            new_asset_repair_log: Fixture to create an object
            of asset repait log
         Returns:
            None
        """
        new_asset_repair_log.save()
        response = client.get(
            f'{API_BASE_URL_V1}/repair-logs', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['fetched'].format(
            'Repair logs')
        assert isinstance(response_json['data'], list)
        assert isinstance(response_json, dict)
        assert isinstance(response_json['meta'], dict)
        assert isinstance(response_json['data'][0]['asset'], dict)
        assert response_json['meta'] is not None
        assert response_json['data'][0]['repairer'] == 'Repairer'
        assert response_json['data'][0]['issueDescription'] == \
            new_asset_repair_log.issue_description

    def test_get_asset_repair_log_without_pagination_succeeds(
            self, auth_header, client, new_asset_repair_log):
        """
        Test get asset repair log without pagination succeeds
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            new_asset_repair_log: Fixture to create an object
            of asset repait log
         Returns:
            None
        """
        new_asset_repair_log.save()
        response = client.get(
            f'{API_BASE_URL_V1}/repair-logs?pagination=false',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['fetched'].format(
            'Repair logs')

        assert isinstance(response_json['data'], list)
        assert isinstance(response_json, dict)
        assert isinstance(response_json['data'][0]['asset'], dict)
        assert response_json['meta'] is None

        assert response_json['data'][0]['repairer'] == 'Repairer'
        assert response_json['data'][0][
            'dateReported'] == '2019-03-12T00:00:00'
        assert response_json['data'][0]['issueDescription'] == \
            new_asset_repair_log.issue_description

    def test_get_asset_repair_log_should_fail_when_token_is_not_provided(
            self, client, init_db):
        """
        Should return a 401 error code when
        getting asset repair log without authorization
        Args:
            client (func): Flask test client
        Returns:
            None
        """
        response = client.get(f'{API_BASE_URL_V1}/repair-logs')
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']
