"""Module for testing updating an asset repair log"""
from flask import json

from datetime import datetime, timedelta

from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import serialization_errors, jwt_errors
from api.utilities.constants import CHARSET
from api.utilities.enums import RepairLogStatusEnum

from ...mocks.asset_repair_log import ASSET_REPAIR_LOG_UPDATE_DATA
# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestUpdateAssetRepairLog:
    """Class for testing the update repair logs resource."""

    def test_update_asset_repair_log_succeeds(self, auth_header, client,
                                              new_asset_repair_log):
        """
        Tests successfully updating an asset repair log
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            new_asset_repair_log: Fixture to create an asset repair
            log in the database
         Returns:
            None
        """
        new_asset_repair_log.save()
        log_id = new_asset_repair_log.id
        update_data = ASSET_REPAIR_LOG_UPDATE_DATA
        data = json.dumps(update_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/repair-logs/{log_id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert isinstance(response_json['data'], dict)
        assert response_json['status'] == 'success'
        assert response_json['data']['issueDescription'] == update_data[
            'issueDescription']
        assert response_json['data']['repairer'] == 'Repairer'
        assert response_json['message'] == SUCCESS_MESSAGES['updated'].format(
            'Repair Log')

    def test_update_asset_repair_log_invalid_log_id_fails(
            self, auth_header, client, new_asset_repair_log):
        """
        Tests updating an asset repair log with an invalid log id
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            new_asset_repair_log: Fixture to create an asset repair
            log in the database
         Returns:
            None
        """
        new_asset_repair_log.save()
        log_id = new_asset_repair_log.id
        update_data = ASSET_REPAIR_LOG_UPDATE_DATA
        data = json.dumps(update_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/repair-logs/@{log_id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert isinstance(response_json, dict)
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors['invalid_id']

    def test_update_asset_repair_log_no_token_fails(self, client,
                                                    new_asset_repair_log):
        """
        Tests updating an asset repair log without an authentication token
        Args:
            client (func): Flask test client
            new_asset_repair_log: Fixture to create an asset repair
            log in the database
         Returns:
            None
        """
        new_asset_repair_log.save()
        log_id = new_asset_repair_log.id
        update_data = ASSET_REPAIR_LOG_UPDATE_DATA
        data = json.dumps(update_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/repair-logs/{log_id}', headers=None, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_update_non_existent_asset_repair_log_fails(
            self, auth_header, client, new_asset_repair_log):
        """
        Tests updating an asset repair log that does not exist
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            new_asset_repair_log: Fixture to create an asset repair
            log in the database
         Returns:
            None
        """
        new_asset_repair_log.save()
        log_id = new_asset_repair_log.id
        update_data = ASSET_REPAIR_LOG_UPDATE_DATA
        data = json.dumps(update_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/repair-logs/{log_id[:-1]}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert isinstance(response_json, dict)
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'not_found'].format('Asset repair log')

    def test_update_with_invalid_status_enum_fails(self, auth_header, client,
                                                   new_asset_repair_log):
        """
        Tests updating an asset repair log with invalid status
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            new_asset_repair_log: Fixture to create an asset repair
            log in the database
         Returns:
            None
        """
        new_asset_repair_log.save()
        log_id = new_asset_repair_log.id
        update_data = ASSET_REPAIR_LOG_UPDATE_DATA
        update_data.update({'status': 'done'})
        data = json.dumps(update_data)
        enum_list = [e.value for e in RepairLogStatusEnum]
        response = client.patch(
            f'{API_BASE_URL_V1}/repair-logs/{log_id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert isinstance(response_json, dict)
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'An error occurred'
        assert isinstance(response_json['errors']['status'], list)
        for value in enum_list:
            assert value in response_json['errors']['status'][0]

    def test_update_asset_repair_log_past_return_date_fails(
            self, auth_header, client, new_asset_repair_log):
        """
        Tests updating an asset repair log with a past date as
        expected return date
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            new_asset_repair_log: Fixture to create an asset repair
            log in the database
         Returns:
            None
        """
        new_asset_repair_log.save()
        log_id = new_asset_repair_log.id
        update_data = ASSET_REPAIR_LOG_UPDATE_DATA
        yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        update_data.update({'expectedReturnDate': yesterday})
        data = json.dumps(update_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/repair-logs/{log_id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert isinstance(response_json, dict)
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_return_date']
