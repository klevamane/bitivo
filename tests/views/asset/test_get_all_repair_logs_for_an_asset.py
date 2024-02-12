"""Test file with tests for get all repair-logs for an asset"""
from flask import json

from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.constants import CHARSET

# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestAssetRepairLog:
    """Test class for getting all repair logs for an asset"""

    def test_get_all_repair_logs_for_an_asset_succeeds(
            self, auth_header, client, new_asset_repair_log):
        """
        Test get all repair logs for an asset succeeds
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            new_asset_repair_log: Fixture to create an object
            of asset repair log
         Returns:
            None
        """
        new_asset_repair_log.save()
        response = client.get(
            f'{API_BASE_URL_V1}/assets/{new_asset_repair_log.asset_id}/repair-logs',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['fetched'].format(
            'Repair Logs')
        assert isinstance(response_json['repairLogs'], list)
        assert isinstance(response_json, dict)
        assert isinstance(response_json['meta'], dict)
        assert response_json['meta'] is not None

    def test_get_all_repair_logs_for_an_asset_with_no_token_fails(
            self, client, new_asset_repair_log):
        """
        Test get all repair logs for an asset with no token in header fails
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            new_asset_repair_log: Fixture to create an object
            of asset repair log
         Returns:
            None
        """
        new_asset_repair_log.save()
        response = client.get(
            f'{API_BASE_URL_V1}/assets/{new_asset_repair_log.asset_id}/repair-logs',
            headers=None)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'Bad request. Header does not contain an authorization token.'
        assert isinstance(response_json, dict)

    def test_get_all_repair_logs_for_an_asset_with_invalid_assetid_fails(
            self, client, auth_header, new_asset_repair_log):
        """
        Test get all repair logs for an asset with an invalid asset_id fails
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            new_asset_repair_log: Fixture to create an object
            of asset repair log
         Returns:
            None
        """
        new_asset_repair_log.save()
        asset_id = new_asset_repair_log.asset_id + "@dsdsd"
        response = client.get(
            f'{API_BASE_URL_V1}/assets/{asset_id}/repair-logs',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'Invalid id in parameter'
        assert isinstance(response_json, dict)

    def test_get_all_repair_logs_for_a_non_existing_asset_returns_404_not_found(
            self, client, auth_header, new_asset_repair_log):
        """
        Test get all repair logs for an asset returns 404 not found
        if the asset doesnot exist
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            new_asset_repair_log: Fixture to create an object
            of asset repair log
         Returns:
            None
        """
        new_asset_repair_log.save()
        asset_id = new_asset_repair_log.asset_id + "dsdsd"
        response = client.get(
            f'{API_BASE_URL_V1}/assets/{asset_id}/repair-logs',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'Asset not found'
        assert isinstance(response_json, dict)
