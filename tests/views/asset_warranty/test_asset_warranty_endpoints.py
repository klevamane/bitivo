"""Module for testing asset warranty resources."""
from flask import json

from api.models.asset import Asset

from api.utilities.constants import CHARSET
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import (
    serialization_errors, jwt_errors
)
from tests.mocks.asset_warranty import (VALID_ASSET_WARRANTY_PACKAGE,
                                        WARRANTY_WRONG_DATE_FORMAT,
                                        WARRANTY_INVALID_DATE_RANGE)

# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestAssetNoteEndpoints:
    """Class for testing asset warranty resource"""

    def test_create_asset_warranty_succeeds(
            self,
            client,
            init_db,
            auth_header_two,
            new_asset_for_asset_warranty):
        """
        Test creating asset warranty package for specific asset succeeds

        Args:
            client (func): Flask test client
            init_db (func): Initialize the test database
            auth_header_two (func): Authentication token
            new_asset_for_asset_warranty (func): Create a new asset
        Returns:
            None
        """
        asset_id = new_asset_for_asset_warranty.id
        data = json.dumps(VALID_ASSET_WARRANTY_PACKAGE)
        response = client.post(
            f'{API_BASE_URL_V1}/assets/{asset_id}/warranty',
            headers=auth_header_two, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 201
        assert isinstance(response_json, dict)
        assert response_json["status"] == "success"
        assert response_json["message"] == SUCCESS_MESSAGES[
            'created'].format('Asset warranty package')
        assert response_json["data"]["startDate"] == \
            VALID_ASSET_WARRANTY_PACKAGE['startDate']

    def test_create_asset_warranty_for_nonexistent_asset_fails(
            self,
            client,
            init_db,
            auth_header_two,
            new_space):
        """
        Test creating asset warranty for non-existent asset fails

        Args:
            client (func): Flask test client
            init_db (func): Initialize the test database
            auth_header_two (func): Authentication token
            new_space: Fixture to create a new space object
        Returns:
            None
        """

        data = json.dumps(VALID_ASSET_WARRANTY_PACKAGE)
        response = client.post(
            f'{API_BASE_URL_V1}/assets/{new_space.id}/warranty',
            headers=auth_header_two, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert isinstance(response_json, dict)
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'not_found'].format('Asset')

    def test_create_asset_warranty_with_invalid_asset_id_fails(
            self,
            client,
            init_db,
            auth_header_two,
            new_asset_for_asset_warranty):
        """
        Test creating asset warranty with invalid asset id fails

        Args:
            client (func): Flask test client
            init_db (func): Initialize the test database
            auth_header_two (func): Authentication token
            new_asset_for_asset_warranty (func): Create a new asset
        Returns:
            None
        """

        asset_id = new_asset_for_asset_warranty.id
        data = json.dumps(VALID_ASSET_WARRANTY_PACKAGE)
        response = client.post(
            f'{API_BASE_URL_V1}/assets/@@{asset_id}/warranty',
            headers=auth_header_two, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert isinstance(response_json, dict)
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'invalid_id']

    def test_create_asset_warranty_without_auth_token_fails(
            self,
            client,
            new_asset_for_asset_warranty):
        """
        Test creating asset warranty without token fails

        Args:
            client (func): Flask test client
            new_asset_for_asset_warranty (func): Create a new asset
        Returns:
            None
        """
        asset_id = new_asset_for_asset_warranty.id
        data = json.dumps(VALID_ASSET_WARRANTY_PACKAGE)
        response = client.post(
            f'{API_BASE_URL_V1}/assets/{asset_id}/warranty',
            headers=None, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_create_asset_warranty_with_wrong_date_format_fails(
            self,
            client,
            init_db,
            auth_header_two,
            new_asset_for_asset_warranty):
        """
        Test creating asset warranty with wrong date format fails

        Args:
            client (func): Flask test client
            init_db (func): Initialize the test database
            auth_header_two (func): Authentication token
            new_asset_for_asset_warranty (func): Create a new asset
        Returns:
            None
        """

        asset_id = new_asset_for_asset_warranty.id
        data = json.dumps(WARRANTY_WRONG_DATE_FORMAT)
        response = client.post(
            f'{API_BASE_URL_V1}/assets/{asset_id}/warranty',
            headers=auth_header_two, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert isinstance(response_json, dict)
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'invalid_date'].format(WARRANTY_WRONG_DATE_FORMAT['startDate'])

    def test_create_asset_warranty_with_invalid_date_range_fails(
            self,
            client,
            init_db,
            auth_header_two,
            new_asset_for_asset_warranty):
        """
        Test creating asset warranty with invalid date range fails

        Args:
            client (func): Flask test client
            init_db (func): Initialize the test database
            auth_header_two (func): Authentication token
            new_asset_for_asset_warranty (func): Create a new asset
        Returns:
            None
        """

        asset_id = new_asset_for_asset_warranty.id
        data = json.dumps(WARRANTY_INVALID_DATE_RANGE)
        response = client.post(
            f'{API_BASE_URL_V1}/assets/{asset_id}/warranty',
            headers=auth_header_two, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert isinstance(response_json, dict)
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'invalid_date_range']
