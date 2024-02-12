"""Module for testing asset insurance resources."""
from flask import json

from api.models.asset import Asset

from api.utilities.constants import CHARSET
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import (
    serialization_errors, jwt_errors
)
from tests.mocks.asset_insurance import (VALID_ASSET_INSURANCE,
                                         INSURANCE_WRONG_DATE_FORMAT,
                                         INSURANCE_INVALID_DATE_RANGE)

# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestAssetInsuranceEndpoints:
    """Class for testing asset insurance resource"""

    def test_create_asset_insurance_succeeds(
            self,
            client,
            init_db,
            auth_header,
            new_asset, new_user):
        """
        Test creating asset insurance for specific asset succeeds
        Args:
            client (func): Flask test client
            init_db (func): Initialize the test database
            auth_header (func): Authentication token
            new_asset (func): Create a new asset
        Returns:
            None
        """

        data = json.dumps(VALID_ASSET_INSURANCE)
        new_user.save()
        response = client.post(
            f'{API_BASE_URL_V1}/assets/{new_asset.id}/insurance',
            headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 201
        assert isinstance(response_json, dict)
        assert response_json["status"] == "success"
        assert response_json["message"] == SUCCESS_MESSAGES[
            'created'].format('Asset insurance')
        assert response_json["data"]["company"] == VALID_ASSET_INSURANCE['company']

    def test_create_asset_insurance_for_nonexistent_asset_fails(
            self,
            client,
            init_db,
            auth_header,
            new_space):
        """
        Test creating asset insurance for non-existent asset fails
        Args:
            client (func): Flask test client
            init_db (func): Initialize the test database
            auth_header (func): Authentication token
            new_space: Fixture to create a new space object
        Returns:
            None
        """

        data = json.dumps(VALID_ASSET_INSURANCE)
        response = client.post(
            f'{API_BASE_URL_V1}/assets/{new_space.id}/insurance',
            headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert isinstance(response_json, dict)
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'not_found'].format('Asset')

    def test_create_asset_insurance_with_wrong_date_format_fails(
            self,
            client,
            init_db,
            auth_header,
            new_asset):
        """
        Test creating asset insurance with wrong date format fails
        Args:
            client (func): Flask test client
            init_db (func): Initialize the test database
            auth_header (func): Authentication token
            new_asset (func): Create a new asset
        Returns:
            None
        """

        asset_id = new_asset.id
        data = json.dumps(INSURANCE_WRONG_DATE_FORMAT)
        response = client.post(
            f'{API_BASE_URL_V1}/assets/{asset_id}/insurance',
            headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert isinstance(response_json, dict)
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'invalid_date'].format(INSURANCE_WRONG_DATE_FORMAT['startDate'])

    def test_create_asset_insurance_with_invalid_date_range_fails(
            self,
            client,
            init_db,
            auth_header,
            new_asset):
        """
        Test creating asset insurance with invalid date range fails
        Args:
            client (func): Flask test client
            init_db (func): Initialize the test database
            auth_header (func): Authentication token
            new_asset (func): Create a new asset
        Returns:
            None
        """

        asset_id = new_asset.id
        data = json.dumps(INSURANCE_INVALID_DATE_RANGE)
        response = client.post(
            f'{API_BASE_URL_V1}/assets/{asset_id}/insurance',
            headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert isinstance(response_json, dict)
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'invalid_date_range']
