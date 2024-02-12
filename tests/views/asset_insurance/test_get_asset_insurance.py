"""Module for testing get insurance policies of an asset"""
from flask import json

# Utilities
from api.utilities.constants import CHARSET
from api.utilities.messages.error_messages import serialization_errors
from api.utilities.messages.error_messages import jwt_errors
from api.utilities.messages.success_messages import SUCCESS_MESSAGES

import json

# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestAssetInsurance:
    """ Test get asset insurance endpoint """

    def test_get_asset_insurance_unauthorized(self, client, init_db,
                                              new_asset_insurance):
        """
        Should return jwt error when token is not provided

        Args:
            client (object): Fixture to get flask test client
            init_db (object): Fixture for initializing test database
            new_asset_insurance(object): Fixture for creating a new asset insurance
        """
        new_asset_insurance.save()
        response = client.get(
            f'{API_BASE_URL_V1}/assets/{new_asset_insurance.asset_id}/insurance'
        )

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json["status"] == "error"
        assert response_json["message"] == jwt_errors['NO_TOKEN_MSG']

    def test_get_asset_insurance_with_valid_asset_id_succeeds(
            self, client, init_db, new_asset_insurance, auth_header_two):
        """
        Tests get a new asset insurance with valid id succeeds

        Args:
            client (object): Fixture to get flask test client
            init_db (object): Fixture for initializing test database
            new_asset_insurance(object): Fixture for creating a new asset insurance
        """
        new_asset_insurance.save()
        response = client.get(
            f'{API_BASE_URL_V1}/assets/{new_asset_insurance.asset_id}/insurance',
            headers=auth_header_two)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        response_json['data']['company'] == new_asset_insurance.company
        response_json['data']['id'] == new_asset_insurance.id
        assert response_json["status"] == "success"
        assert response_json["message"] == SUCCESS_MESSAGES['fetched'].format(
            'Asset insurance policies')
        assert isinstance(response_json['data']['history'], list)

    def test_get_asset_insurance_for_non_existent_asset_fails(
            self, client, init_db, new_asset_insurance, auth_header_two):
        """
        Tests get a new asset insurance with invalid id fails

        Args:
            client (object): Fixture to get flask test client
            init_db (object): Fixture for initializing test database
            new_asset_insurance(object): Fixture for creating a new asset insurance
        """
        new_asset_insurance.save()
        response = client.get(
            f'{API_BASE_URL_V1}/assets/-LjpfnB1FO4HKAS/insurance',
            headers=auth_header_two)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'not_found'].format('Asset')

    def test_get_asset_insurance_for_asset_with_no_insurance_succeeds(
            self, client, init_db, asset_inflow, auth_header_two):
        """
        Tests get a new asset insurance with invalid id fails

        Args:
            client (object): Fixture to get flask test client
            init_db (object): Fixture for initializing test database
            asset_inflow(object): Fixture for creating a new asset
            with no insurance
        """
        asset_inflow.save()
        response = client.get(
            f'{API_BASE_URL_V1}/assets/{asset_inflow.id}/insurance',
            headers=auth_header_two)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        response_json['data'] == {}
        assert response_json["status"] == "success"
        assert response_json["message"] == SUCCESS_MESSAGES['fetched'].format(
            'Asset insurance policies')
