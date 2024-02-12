"""Tests module for GET users in a center endpoint."""
# pylint: skip-file
import json

from api.utilities.constants import CHARSET
from api.utilities.messages.error_messages import (serialization_errors,
                                                   jwt_errors)
from config import AppConfig
V1_BASE_URL = AppConfig.API_BASE_URL_V1


class TestGetPeopleInCenter:
    """Test class for the get users in a center endpoint."""

    def test_get_users_valid_center_id(self, auth_header, client, init_db,
                                       test_center_with_users):
        """Test get users under an existing centre with existing users."""
        response = client.get(
            f'{V1_BASE_URL}/centers/{test_center_with_users.id}/people',
            headers=auth_header)
        response_data = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert isinstance(response_data['data'], list)
        assert len(response_data['data']) == 5
        assert 'center' not in response_data['data'][0]
        assert len(response_data['data'][0]['role']) == 3

    def test_get_users_valid_center_no_users(self, auth_header, client,
                                             init_db,
                                             test_center_with_deleted_users):
        """Test get users under existing centre with no users."""
        response = client.get(
            f'{V1_BASE_URL}/centers/{test_center_with_deleted_users.id}/people',
            headers=auth_header)
        response_data = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert isinstance(response_data['data'], list)
        assert response_data['data'] == []

    def test_get_users_invalid_center_id(self, auth_header, client, init_db):
        """Test get users with invalid center id."""
        response = client.get(
            f'{V1_BASE_URL}/centers/invalid-id@@/people', headers=auth_header)
        response_data = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_data['message'] == serialization_errors['invalid_id']

    def test_get_users_nonexistent_center(self, auth_header, client, init_db):
        """Test get users with nonexistent center."""
        response = client.get(
            f'{V1_BASE_URL}/centers/nonexistent/people', headers=auth_header)
        response_data = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_data['message'] == 'Center not found'

    def test_get_users_deleted_center(self, auth_header, client, init_db,
                                      test_deleted_center):
        """Test get users with deleted center."""
        response = client.get(
            f'{V1_BASE_URL}/centers/{test_deleted_center.id}/people',
            headers=auth_header)
        response_data = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_data['message'] == 'Center not found'

    def test_get_deleted_users(self, auth_header, client, init_db,
                               test_center_with_deleted_users):
        """Test get users under existing centre with deleted users returns
        empty list."""
        response = client.get(
            f'{V1_BASE_URL}/centers/{test_center_with_deleted_users.id}/people',
            headers=auth_header)
        response_data = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert isinstance(response_data['data'], list)
        assert response_data['data'] == []

    def test_get_deleted_users_with_params(self, auth_header, client, init_db,
                                           test_center_with_deleted_users):
        """Test get users under existing centre with deleted users returns
        empty list."""
        response = client.get(
            f'{V1_BASE_URL}/centers/{test_center_with_deleted_users.id}/people?include=deleted',
            headers=auth_header)
        response_data = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        for user in response_data['data']:
            assert user['deleted']
        assert isinstance(response_data['data'], list)
        assert len(response_data['data']) > 0

    def test_get_users_valid_center_id_no_token(self, client, init_db,
                                                test_center_with_users):
        """
        Test get users under an existing centre with existing users with no
        auth token
        """
        response = client.get(
            f'{V1_BASE_URL}/centers/{test_center_with_users.id}/people')
        response_data = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_data['message'] == jwt_errors['NO_TOKEN_MSG']
