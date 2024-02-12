"""Module with tests for get maintenance category endpoint"""
# Messages
from api.utilities.messages.error_messages import (database_errors, jwt_errors,
                                                   serialization_errors)

# Utilities
from api.utilities.messages.success_messages import SUCCESS_MESSAGES

# app config
from config import AppConfig

API_V1_BASE_URL = AppConfig.API_BASE_URL_V1


class TestGetMaintenanceCategoryEndpoint:
    """Get maintenance category endpoint tests"""

    def test_get_maintenance_category_succeeds(
            self, init_db, client, auth_header, new_maintenance_category):
        """Test when request is valid.

        Args:
            init_db (object): Initialize the test db
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
            new_maintenance_category (obj): fixture for creating a maintenance
            category
        """
        new_maintenance_category.save()
        response = client.get(
            f'{API_V1_BASE_URL}/maintenance-categories/{new_maintenance_category.id}',
            headers=auth_header)
        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == SUCCESS_MESSAGES[
            'successfully_fetched'].format('Maintenance Category')
        assert 'workOrders' in response.json['data']

    def test_get_maintenance_category_with_non_existing_id_fails(
            self, init_db, client, auth_header):
        """Should return 404 when a valid but non-existing is provided

        Args:
            init_db (object): Initialize the test db
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
        """
        response = client.get(
            f'{API_V1_BASE_URL}/maintenance-categories/-Lc3pO',
            headers=auth_header)
        assert response.status_code == 404
        assert response.json['status'] == 'error'
        assert response.json['message'] == database_errors[
            'non_existing'].format('Maintenance category')

    def test_get_maintenance_category_with_invalid_id_fails(
            self, init_db, client, auth_header):
        """Should return 404 when a invalid id is provided

        Args:
            init_db (object): Initialize the test db
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
        """
        response = client.get(
            f'{API_V1_BASE_URL}/maintenance-categories/@#',
            headers=auth_header)
        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['message'] == serialization_errors['invalid_id']

    def test_get_maintenance_category_with_no_token_fails(
            self, init_db, client, new_maintenance_category):
        """Should fail with no token in the header

        Args:
            init_db (object): Initialize the test db
            client(FlaskClient): fixture to get flask test client
            new_maintenance_category (obj): fixture for creating a maintenance
            category
        """
        new_maintenance_category.save()
        response = client.get(
            f'{API_V1_BASE_URL}/maintenance-categories/{new_maintenance_category.id}'
        )
        assert response.status_code == 401
        assert response.json['status'] == 'error'
        assert response.json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_get_maintenance_category_with_invalid_token_fails(
            self, init_db, client, new_maintenance_category):
        """Should fail with invalid token

        Args:
            init_db (object): Initialize the test db
            client(FlaskClient): fixture to get flask test client
            maintenance_category (obj): fixture for creating a maintenance
            category
        """
        new_maintenance_category.save()
        response = client.get(
            f'{API_V1_BASE_URL}/maintenance-categories/{new_maintenance_category.id}',
            headers={'Authorization': "Bearer invalid"})
        assert response.status_code == 401
        assert response.json['status'] == 'error'
        assert response.json['message'] == jwt_errors['INVALID_TOKEN_MSG']
