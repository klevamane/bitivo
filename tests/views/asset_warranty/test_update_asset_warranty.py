"""Module for testing asset warranty resources."""
from flask import json

from api.models.asset import Asset

from api.utilities.constants import CHARSET
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import (serialization_errors,
                                                   jwt_errors)
from tests.mocks.asset_warranty import (VALID_ASSET_WARRANTY_PACKAGE,
                                        WARRANTY_WRONG_DATE_FORMAT,
                                        WARRANTY_INVALID_DATE_RANGE)

# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestUpdateAssetWarranty:
    """Tests the update asset warranty package endpoint"""

    def test_update_start_date_and_end_date_succeeds(
            self, client, init_db, auth_header, new_asset_warranty, new_user):
        """
        Should return a 200 response code when valid start date and
        end date is used

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_asset_warranty (obj): fixture to create a new
                                      asset warranty

        Returns:
            None
        """
        new_user.save()
        new_asset_warranty.save()
        data = json.dumps(VALID_ASSET_WARRANTY_PACKAGE)
        response = client.patch(
            f'{API_BASE_URL_V1}/warranty/{new_asset_warranty.id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert isinstance(response_json, dict)
        assert response_json["status"] == "success"
        assert response_json["message"] == SUCCESS_MESSAGES['updated'].format(
            'Asset warranty package')
        assert response_json["data"]["startDate"] == \
            VALID_ASSET_WARRANTY_PACKAGE['startDate']

    def test_update_start_date_succeeds(self, client, init_db, auth_header,
                                        new_asset_warranty):
        """
        Should return a 200 response code when valid start date without
        an end date is used

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_asset_warranty (obj): fixture to create a new
                                      asset warranty

        Returns:
            None
        """
        new_asset_warranty.save()
        warranty_start_date = VALID_ASSET_WARRANTY_PACKAGE.copy()
        del warranty_start_date['endDate']
        data = json.dumps(warranty_start_date)
        response = client.patch(
            f'{API_BASE_URL_V1}/warranty/{new_asset_warranty.id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert isinstance(response_json, dict)
        assert response_json["status"] == "success"
        assert response_json["message"] == SUCCESS_MESSAGES['updated'].format(
            'Asset warranty package')
        assert response_json["data"]["startDate"] == \
            VALID_ASSET_WARRANTY_PACKAGE['startDate']

    def test_update_end_date_succeeds(self, client, init_db, auth_header,
                                      new_asset_warranty):
        """
        Should return a 200 response code when valid end date without
        an start date is used

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_asset_warranty (obj): fixture to create a new
                                      asset warranty

        Returns:
            None
        """
        new_asset_warranty.save()
        warranty_end_date = VALID_ASSET_WARRANTY_PACKAGE.copy()
        del warranty_end_date['startDate']
        data = json.dumps(warranty_end_date)
        response = client.patch(
            f'{API_BASE_URL_V1}/warranty/{new_asset_warranty.id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert isinstance(response_json, dict)
        assert response_json["status"] == "success"
        assert response_json["message"] == SUCCESS_MESSAGES['updated'].format(
            'Asset warranty package')
        assert response_json["data"]["endDate"] == \
            VALID_ASSET_WARRANTY_PACKAGE['endDate']

    def test_update_asset_warranty_with_wrong_date_format_fails(
            self, client, init_db, auth_header, new_asset_warranty):
        """
        Should return a 400 response code when wrong date formats are 
        used

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_asset_warranty (obj): fixture to create a new
                                      asset warranty

        Returns:
            None
        """
        new_asset_warranty.save()
        data = json.dumps(WARRANTY_WRONG_DATE_FORMAT)
        response = client.patch(
            f'{API_BASE_URL_V1}/warranty/{new_asset_warranty.id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert isinstance(response_json, dict)
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'invalid_date'].format(WARRANTY_WRONG_DATE_FORMAT['startDate'])

    def test_update_asset_warranty_with_invalid_date_range_fails(
            self, client, init_db, auth_header, new_asset_warranty):
        """
        Should return a 400 response code when invalid date range is used

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_asset_warranty (obj): fixture to create a new
                                      asset warranty

        Returns:
            None
        """
        new_asset_warranty.save()
        data = json.dumps(WARRANTY_INVALID_DATE_RANGE)
        response = client.patch(
            f'{API_BASE_URL_V1}/warranty/{new_asset_warranty.id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert isinstance(response_json, dict)
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'invalid_date_range']

    def test_update_asset_warranty_for_nonexistent_asset_warranty_fails(
            self, client, init_db, auth_header, new_space):
        """
        Should return a 404 response code when a none existent id is
        used

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_space (obj): fixture to create a new
                             space

        Returns:
            None
        """

        data = json.dumps(VALID_ASSET_WARRANTY_PACKAGE)
        response = client.patch(
            f'{API_BASE_URL_V1}/warranty/{new_space.id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert isinstance(response_json, dict)
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'resource_not_found'].format('Asset warranty')

    def test_update_asset_warranty_without_auth_token_fails(
            self, client, new_asset_warranty):
        """
        Should return a 401 response code when the request is made
        without the auth token
        
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_space (obj): fixture to create a new
                             space

        Returns:
            None
        """
        data = json.dumps(VALID_ASSET_WARRANTY_PACKAGE)
        response = client.patch(
            f'{API_BASE_URL_V1}/warranty/{new_asset_warranty.id}', data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']
