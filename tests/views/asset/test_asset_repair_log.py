"""Module for asset repair log resource endpoints."""
from flask import json
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import serialization_errors
from api.utilities.messages.error_messages.serialization_error import error_dict
from api.utilities.constants import CHARSET
from api.utilities.enums import AssetStatus, RepairLogStatusEnum

# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestAssetRepairLog:
    """Class for Asset repair log resource."""

    def test_create_asset_repair_log_valid_data_succeeds(
            self, auth_header, client, asset_repair_log):
        """
        Tests create asset repair log with valid data
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            asset_repair_log: Fixture to create an object
            of asset repait log
         Returns:
            None
        """
        data = json.dumps(asset_repair_log)
        response = client.post(
            f'{API_BASE_URL_V1}/repair-logs', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 201
        assert isinstance(response_json['data'], dict)
        assert isinstance(response_json['data']['asset'], dict)
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['created'].format(
            'Repair Log')
        assert response_json['data']['asset']['id'] == asset_repair_log[
            'assetId']
        assert response_json['data']['asset'][
            'status'] == AssetStatus.IN_REPAIRS.value
        assert response_json['data'][
            'status'] == RepairLogStatusEnum.open.value
        assert response_json['data']['issueDescription'] == asset_repair_log[
            'issueDescription']
        assert asset_repair_log['expectedReturnDate'] in response_json['data'][
            'expectedReturnDate']

    def test_create_asset_repair_log_without_asset_id_fails(
            self, auth_header, client, asset_repair_log):
        """
        Tests create asset repair log without assetId
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            asset_repair_log: Fixture to create an object
            of asset repait log
         Returns:
            None
        """
        del asset_repair_log['assetId']
        data = json.dumps(asset_repair_log)
        response = client.post(
            f'{API_BASE_URL_V1}/repair-logs', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert isinstance(response_json['errors'], dict)
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'An error occurred'
        assert response_json['errors']['assetId'][0] == error_dict[
            'field_required']

    def test_create_asset_repair_log_without_issue_description_fails(
            self, auth_header, client, asset_repair_log):
        """
        Tests create asset repair log without issueDescription
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            asset_repair_log: Fixture to create an object
            of asset repait log
         Returns:
            None
        """
        del asset_repair_log['issueDescription']
        data = json.dumps(asset_repair_log)
        response = client.post(
            f'{API_BASE_URL_V1}/repair-logs', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert isinstance(response_json['errors'], dict)
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'An error occurred'
        assert response_json['errors']['issueDescription'][0] == error_dict[
            'field_required']

    def test_create_asset_repair_log_without_expected_return_date_fails(
            self, auth_header, client, asset_repair_log):
        """
        Tests create asset repair log without expectedReturnDate
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            asset_repair_log: Fixture to create an object
            of asset repait log
         Returns:
            None
        """
        del asset_repair_log['expectedReturnDate']
        data = json.dumps(asset_repair_log)
        response = client.post(
            f'{API_BASE_URL_V1}/repair-logs', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert isinstance(response_json['errors'], dict)
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'An error occurred'
        assert response_json['errors']['expectedReturnDate'][0] == error_dict[
            'field_required']

    def test_create_asset_repair_log_with_invalid_asset_id_fails(
            self, auth_header, client, asset_repair_log):
        """
        Tests create asset repair log with invalid assetId
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            asset_repair_log: Fixture to create an object
            of asset repait log
         Returns:
            None
        """
        asset_repair_log['assetId'] = '{}'
        data = json.dumps(asset_repair_log)
        response = client.post(
            f'{API_BASE_URL_V1}/repair-logs', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert isinstance(response_json['errors'], dict)
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'An error occurred'
        assert response_json['errors']['assetId'][0] == serialization_errors[
            'invalid_asset_id']

    def test_create_asset_repair_with_date_before_today_fails(
            self, auth_header, client, asset_repair_log):
        """
        Tests create asset repair log with date before today
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            asset_repair_log: Fixture to create an object
            of asset repait log
         Returns:
            None
        """
        asset_repair_log['expectedReturnDate'] = '2018-01-01'
        data = json.dumps(asset_repair_log)
        response = client.post(
            f'{API_BASE_URL_V1}/repair-logs', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_return_date']

    def test_create_asset_repair_with_invalid_date_fails(
            self, auth_header, client, asset_repair_log):
        """
        Tests create asset repair log with invalid date
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            asset_repair_log: Fixture to create an object
            of asset repait log
         Returns:
            None
        """
        asset_repair_log['expectedReturnDate'] = '2018-01-01475687'
        data = json.dumps(asset_repair_log)
        response = client.post(
            f'{API_BASE_URL_V1}/repair-logs', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert 'Invalid date range please' in response_json['message']

    def test_create_asset_repair_with_non_existing_asset_fails(
            self, auth_header, client, asset_repair_log):
        """
        Tests create asset repair log with non existing assetId
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            asset_repair_log: Fixture to create an object
            of asset repait log
         Returns:
            None
        """
        asset_repair_log['assetId'] = 'Not-Found'
        data = json.dumps(asset_repair_log)
        response = client.post(
            f'{API_BASE_URL_V1}/repair-logs', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert isinstance(response_json['errors'], dict)
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'An error occurred'
        assert response_json['errors']['assetId'][0] == serialization_errors[
            'asset_not_found']
