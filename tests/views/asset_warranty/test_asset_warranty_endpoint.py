"""Module that handles asset warranty test"""

# third-party library
from flask import json

# Utilities
from api.utilities.constants import CHARSET
from api.utilities.messages.error_messages import serialization_errors
from api.utilities.messages.error_messages import jwt_errors
from api.utilities.messages.success_messages import SUCCESS_MESSAGES

#  import json

# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestAssetWarranty:
    """ Test get asset warranty endpoint """

    def test_get_asset_warranty_unauthorized(self, client, init_db,
                                             new_asset_warranty):
        """
        Should return jwt error when token is not provided
          Args:
            client (object): Fixture to get flask test client
            init_db (object): Fixture for initializing test database
            new_asset_warranty(object): Fixture for creating a new asset warranty
        """
        new_asset_warranty.save()
        response = client.get(
            f'{API_BASE_URL_V1}/assets/{new_asset_warranty.asset_id}/warranty')

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json["status"] == "error"
        assert response_json["message"] == jwt_errors['NO_TOKEN_MSG']

    def test_get_asset_warranty_with_valid_asset_id_succeeds(
            self, client, init_db, new_asset_warranty, auth_header_two):
        """
        Tests get a new asset warranty with valid id succeeds
          Args:
            client (object): Fixture to get flask test client
            init_db (object): Fixture for initializing test database
            new_asset_warranty(object): Fixture for creating a new asset warranty
        """
        new_asset_warranty.save()
        response = client.get(
            f'{API_BASE_URL_V1}/assets/{new_asset_warranty.asset_id}/warranty',
            headers=auth_header_two)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['data']['id'] == new_asset_warranty.id
        assert response_json["status"] == "success"
        assert response_json["message"] == SUCCESS_MESSAGES[
            'successfully_fetched'].format('Asset warranty')

    def test_get_asset_warranty_with_invalid_asset_id_fails(
            self, client, init_db, new_asset_warranty, auth_header_two):
        """
        Tests get a new asset warranty with invalid id fails
          Args:
            client (object): Fixture to get flask test client
            init_db (object): Fixture for initializing test database
            new_asset_warranty(object): Fixture for creating a new asset warranty
        """
        new_asset_warranty.save()
        response = client.get(
            f'{API_BASE_URL_V1}/assets/-LjpfnB1FO4HKAS/warranty',
            headers=auth_header_two)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'not_found'].format('Asset')
