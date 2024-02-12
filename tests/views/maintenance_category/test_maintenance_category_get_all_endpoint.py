"""Module with tests for delete maintenance category endpoint"""
# System Imports
from flask import json

# Messages
from api.utilities.constants import CHARSET, MIMETYPE
from api.utilities.messages.error_messages import jwt_errors

# app config
from config import AppConfig

API_V1_BASE_URL = AppConfig.API_BASE_URL_V1


class TestGetAllMaintenanceCategoryEndpoint:
    """Fetch all maintenance category endpoint tests"""

    def test_get_all_maintenance_categories_succeeds(self, client, auth_header,
                                                     new_maintenance_category):
        """Should pass when maintenance is successfully fetched

        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
            maintenance_categories (obj): fixture for creating maintenance categories
        """
        maintenance_category = new_maintenance_category.save()
        response = client.get(
            f'{API_V1_BASE_URL}/maintenance-categories', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        response_data = response_json['data'][0]

        assert response.status_code == 200
        assert len(response_json['data'][0]) > 0
        assert response_data['id'] == maintenance_category.id
        assert response_data['title'] == maintenance_category.title

    def test_get_all_maintenance_categories_without_pagination_succeeds(
            self, client, auth_header, new_maintenance_category):
        """Should pass when maintenance is successfully fetched

        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
            maintenance_categories (obj): fixture for creating maintenance categories
        """
        maintenance_category = new_maintenance_category.save()
        response = client.get(
            f'{API_V1_BASE_URL}/maintenance-categories?pagination=false',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        response_data = response_json['data'][0]
        assert response.status_code == 200
        assert response_data['id'] == maintenance_category.id
        assert response_data['title'] == maintenance_category.title
        assert response_json['meta'] is None

    def test_maintenance_categories_pagination_meta_succeed(
            self, client, auth_header):
        """Should return the a list of maintenance categories and the pagination meta.

        Args:
            client(FlaskClient): fixture to get flask test client.
            auth_header(dict): fixture to get token.

        """

        response = client.get(
            f'{API_V1_BASE_URL}/maintenance-categories' + '?page=1&limit=4',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        maintenance_categories_data = response_json['data']
        maintenance_categories_meta = response_json['meta']

        assert maintenance_categories_meta['totalCount'] == len(
            maintenance_categories_data)
        assert maintenance_categories_meta['page'] == 1

    def test_get_maintainance_categories_with_no_token_fails(
            self, init_db, client, auth_header):
        """Tests when token is not provided.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_maintenance_categories_with_assignee_in_center: fixture that contain work order


        """
        response = client.get(f'{API_V1_BASE_URL}/maintenance-categories')
        response_data = json.loads(response.data.decode(CHARSET))
        assert response_data.get('status') == 'error'
        assert response_data.get('message') == jwt_errors['NO_TOKEN_MSG']
        assert response.status_code == 401

    def test_get_existing_maintenance_categories_should_fail_with_invalid_token(
            self, client, init_db):
        """
        Should fail when invalid token is provided

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
        """

        response = client.get(
            f'{API_V1_BASE_URL}/maintenance-categories',
            headers={
                'Authorization': "Bearer XXXX",
                'Content-Type': MIMETYPE,
                'Accept': MIMETYPE
            })
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['INVALID_TOKEN_MSG']

    def test_get_all_maintenance_categories_include_deleted_succeeds(
            self, client, auth_header, new_maintenance_category, request_ctx,
            mock_request_two_obj_decoded_token):
        """Should pass when maintenance is successfully fetched

        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
            maintenance_categories (obj): fixture for creating maintenance categories
        """

        maintenance_category = new_maintenance_category.save()
        maintenance_category.delete()

        response = client.get(
            f'{API_V1_BASE_URL}/maintenance-categories?include=deleted',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        response_data = response_json['data'][0]

        assert response.status_code == 200
        assert len(response_data) > 0
        assert response_data['id'] == maintenance_category.id
        assert response_data['title'] == maintenance_category.title
        assert isinstance(response_json['data'], list)

    def test_get_all_maintenance_categories_include_deleted_with_invalid_url_query_fails(
            self, client, auth_header, request_ctx,
            mock_request_two_obj_decoded_token, new_maintenance_category,
            duplicate_maintenance_category, new_user):
        """Should pass when maintenance is successfully fetched
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
            maintenance_categories (obj): fixture for creating maintenance categories
        """
        new_user.save()
        maintenance_category = duplicate_maintenance_category.save()
        maintenance_category.delete()

        response = client.get(
            f'{API_V1_BASE_URL}/maintenance-categories?includ=deleted',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json[
            'message'] == 'Invalid URL query: `includ` column does not exist on MaintenanceCategory table in the database'
