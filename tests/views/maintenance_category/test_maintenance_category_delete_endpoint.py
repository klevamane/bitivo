"""Module with tests for delete maintenance category endpoint"""
# Mocks
from tests.mocks.maintenance_category import MAINTENANCE_CATEGORY

# Messages
from api.utilities.messages.error_messages import (database_errors, jwt_errors,
                                                   serialization_errors)
from api.utilities.messages.success_messages import SUCCESS_MESSAGES

from tests.mocks.user import user_one
# app config
from config import AppConfig

API_V1_BASE_URL = AppConfig.API_BASE_URL_V1


class TestDeleteMaintenanceCategoryEndpoint:
    """Delete maintenance category endpoint tests"""

    def test_delete_maintenance_category_succeeds(
            self, client, init_db, auth_header, duplicate_maintenance_category, new_user):
        """Should pass when maintenance is successfully deleted
        
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
            duplicate_maintenance_category (obj): fixture for creating a maintenance category
        """
        new_user.token_id = user_one.token_id
        new_user.save()
        duplicate_maintenance_category.save()
        response = client.delete(
            f'{API_V1_BASE_URL}/maintenance-categories/{duplicate_maintenance_category.id}',
            headers=auth_header)
        assert response.status_code == 200
        assert response.json['message'] == SUCCESS_MESSAGES['deleted'].format(
            'Maintenance Category')

    def test_delete_maintenance_category_with_invalid_id_fails(
            self, init_db, client, auth_header, new_user):
        """Should return 404 when a invalid id is provided
        
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
        """
        new_user.token_id = user_one.token_id
        new_user.save()
        response = client.delete(
            f'{API_V1_BASE_URL}/maintenance-categories/fgrer',
            headers=auth_header)
        assert response.status_code == 404
        assert response.json['message'] == database_errors[
            'non_existing'].format('Maintenance category')

    def test_non_existing_delete_maintenance_category_fails(
            self, init_db, client, auth_header, new_user):
        """Should return 404 when the id doesnot exist in the database
        
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
        """
        new_user.token_id = user_one.token_id
        new_user.save()
        response = client.delete(
            f'{API_V1_BASE_URL}/maintenance-categories/-Ltdjr',
            headers=auth_header)
        assert response.status_code == 404
        assert response.json['message'] == database_errors[
            'non_existing'].format('Maintenance category')

    def test_delete_already_deleted_maintenance_category_fails(
            self, client, init_db, auth_header, duplicate_maintenance_category, new_user):
        """Should return 404 when the maintenance category is already deleted
        
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
            duplicate_maintenance_category (obj): fixture for creating a maintenance category
        """
        new_user.token_id = user_one.token_id
        new_user.save()
        duplicate_maintenance_category.deleted = True
        duplicate_maintenance_category.save()
        response = client.delete(
            f'{API_V1_BASE_URL}/maintenance-categories/{duplicate_maintenance_category.id}',
            headers=auth_header)
        assert response.status_code == 404
        assert response.json['message'] == database_errors[
            'non_existing'].format('Maintenance category')

    def test_delete_maintenance_category_with_work_orders_fails(
            self, init_db, client, auth_header, new_maintenance_category,
            new_work_order, new_user):
        """Should fail when maintenance category has workorders
        
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
            duplicate_maintenance_category (obj): fixture for creating a maintenance category
            new_work_order (obj): fixture to create a maintenance category
        """
        new_user.token_id = user_one.token_id
        new_user.save()
        new_maintenance_category.save()
        new_work_order.save()
        response = client.delete(
            f'{API_V1_BASE_URL}/maintenance-categories/{new_maintenance_category.id}',
            headers=auth_header)
        assert response.status_code == 403
        assert response.json[
            'message'] == database_errors['model_delete_children'].format(
                'MaintenanceCategory', 'WorkOrder(s)')

    def test_delete_maintenance_category_with_no_token_fails(
            self, client, init_db, duplicate_maintenance_category, new_user):
        """Should fail with no token in the header
        
        Args:
            client(FlaskClient): fixture to get flask test client
            duplicate_maintenance_category (obj): fixture for creating a maintenance category
        """
        new_user.token_id = user_one.token_id
        new_user.save()
        duplicate_maintenance_category.save()
        response = client.delete(
            f'{API_V1_BASE_URL}/maintenance-categories/{duplicate_maintenance_category.id}'
        )
        assert response.status_code == 401
        assert response.json['status'] == 'error'
        assert response.json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_delete_maintenance_category_with_invalid_token_fails(
            self, init_db, client, duplicate_maintenance_category, new_user):
        """Should fail with invalid token
        
        Args:
            client(FlaskClient): fixture to get flask test client
            duplicate_maintenance_category (obj): fixture for creating a maintenance category
        """
        new_user.token_id = user_one.token_id
        new_user.save()
        duplicate_maintenance_category.save()
        response = client.delete(
            f'{API_V1_BASE_URL}/maintenance-categories/{duplicate_maintenance_category.id}',
            headers={'Authorization': "Bearer invalid"})
        assert response.status_code == 401
        assert response.json['status'] == 'error'
        assert response.json['message'] == jwt_errors['INVALID_TOKEN_MSG']
