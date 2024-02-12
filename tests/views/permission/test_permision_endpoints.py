"""
Module of tests for permission endpoints
"""
from flask import json
# Constants
from api.utilities.constants import CHARSET, MIMETYPE

# Messages
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import (authorization_errors,
                                                   jwt_errors)

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1


class TestPermissionEndpoints:
    """
    Tests for getting permissions
    """

    def test_get_permissions_with_authorization_succeeds(
            self, client, init_db, auth_header, new_permissions,
            grant_test_user_permissions):
        """Should succeed with a 200 OK status code

        Parameters:
            client(FlaskClient): Fixture to get flask test client
            init_db(SQLAlchemy): Fixture to initialize the test database
            auth_header(dict): Fixture to get token
            new_permissions(BaseModel): Fixture for creating a permissions
        """
        for permission in new_permissions:
            permission.save()
        grant_test_user_permissions()
        response = client.get(f'{BASE_URL}/permissions', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == \
            SUCCESS_MESSAGES['fetched'].format('Permissions')
        assert isinstance(response_json['data'], list)
        assert len(response_json['data']) >= 4

    def test_get_permissions_with_no_token_fails(self, client, init_db,
                                                 new_permissions):
        """Should return a 401 status code if a token is not provided
        
        Parameters:
            client(FlaskClient): Fixture to get flask test client
            init_db(SQLAlchemy): Fixture to initialize the test database
            new_permissions(BaseModel): Fixture for creating a permissions
        """
        for permission in new_permissions:
            permission.save()
        response = client.get(f'{BASE_URL}/permissions')
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_get_permissions_with_invalid_token_fails(self, client, init_db,
                                                      new_permissions):
        """Should return a 401 status code if the token is invalid

        Args:
            client(FlaskClient): Fixture to get flask test client
            init_db(SQLAlchemy): Fixture to initialize the test database
            new_permissions(BaseModel): Fixture for creating a permissions
        """
        for permission in new_permissions:
            permission.save()
        response = client.get(
            f'{BASE_URL}/permissions',
            headers={
                'Authorization': "Bearer XXXX",
                'Content-Type': MIMETYPE,
                'Accept': MIMETYPE
            })
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['INVALID_TOKEN_MSG']

    def test_get_permissions_with_user_without_access_to_permission_fails(
            self, client, init_db, auth_header, new_permissions,
            revoke_test_user_permissions):
        """Should fail with a 403 status code if user not authorized

        Args:
            client(FlaskClient): Fixture to get flask test client
            init_db(SQLAlchemy): Fixture to initialize the test database
            auth_header(dict): Fixture to get token
            new_permissions(BaseModel): Fixture for creating a permissions
        """
        for permission in new_permissions:
            permission.save()
        revoke_test_user_permissions()
        response = client.get(f'{BASE_URL}/permissions', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 403
        assert response_json['status'] == 'error'
        assert response_json['message'] == \
            authorization_errors['permissions_error'].format('view', 'permissions')
