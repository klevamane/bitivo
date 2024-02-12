"""Tests for endpoints to get users with 'provisionUser'."""
from flask import json
import jwt

# Constants
from api.utilities.constants import CHARSET

# Messages
from api.utilities.messages.error_messages import serialization_errors
from api.utilities.messages.success_messages import SUCCESS_MESSAGES

# Mocks
from tests.mocks.user import USER_DATA_NEW, USER_DATA_VALID

# app config
from config import AppConfig

API_V1_BASE_URL = AppConfig.API_BASE_URL_V1
SECRET_KEY = AppConfig.JWT_SECRET_KEY


class TestProvisionUser:
    """Test to get user details with 'provisionUser' query param"""

    def test_get_user_details_with_non_existing_id_provision_should_succeed(
            self, client, init_db, auth_header, new_user, default_role):
        """
        Test that user details are successfully returned when a non existing
        person id with 'provisionUser' query param set to 'true'
        """
        new_user.save()
        response = client.get(
            f'{API_V1_BASE_URL}/people/{new_user.token_id}?provisionUser=true',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert (response.status_code, response_json['status']) == (200,
                                                                   'success')
        user_data = response_json['data']
        assert 'id' in user_data
        assert 'name' in user_data
        assert 'email' in user_data
        assert 'status' in user_data
        assert 'imageUrl' in user_data
        assert 'tokenId' in user_data
        assert 'role' in user_data
        assert 'id' in user_data['role']
        assert 'title' in user_data['role']
        assert 'description' in user_data['role']
        assert type(user_data) is dict

    def test_get_user_details_with_invalid_provision_user_value_fails(
            self, client, init_db, auth_header, new_user):
        """
        Test that getting a user details with an invalid 'provisionUser' param
        value fails
        """
        response = client.get(
            f'{API_V1_BASE_URL}/people/-LX1Sz-LCNKCKv0IRwZn?provisionUser=madden',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        response_json['message'] = serialization_errors[
            'invalid_query_strings'].format('provisionUser', 'madden')

    def test_add_user_without_center_id_succeeds(self, client, init_db,
                                                 auth_header, new_custom_role):
        """
        Should return an 201 status code and new user data when center id is
        not provided in a valid data
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_center(BaseModel): fixture for creating a center
            new_role(BaseModel): fixture for creating a role
        """

        new_custom_role.save()
        USER_DATA_NEW['roleId'] = new_custom_role.id
        response = client.post(
            f'{API_V1_BASE_URL}/people',
            headers=auth_header,
            data=json.dumps(USER_DATA_NEW))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 201
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['created'].format(
            USER_DATA_NEW['name'])
        assert response_json['data']['name'] == USER_DATA_NEW['name']
        assert response_json['data']['email'] == USER_DATA_NEW['email']
        assert response_json['data']['imageUrl'] == USER_DATA_NEW['imageUrl']
        assert response_json['data']['status'] == 'enabled'
        assert 'roleId' not in response_json['data']
        assert 'centerId' not in response_json['data']
        assert type(response_json['data']['role']) is dict
        assert response_json['data']['role']['id'] == new_custom_role.id
        assert response_json['data']['role']['title'] == new_custom_role.title
        assert response_json['data']['role'][
            'description'] == new_custom_role.description

    def test_add_user_with_center_id_succeeds(
            self, client, init_db, auth_header, new_center, new_custom_role):
        """
        Should return an 201 status code and new user data when center id is
        provided in a valid data
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_center(BaseModel): fixture for creating a center
            new_role(BaseModel): fixture for creating a role
        """
        new_center.save()
        new_custom_role.save()
        USER_DATA_VALID['roleId'] = new_custom_role.id
        USER_DATA_VALID['centerId'] = new_center.id
        response = client.post(
            f'{API_V1_BASE_URL}/people',
            headers=auth_header,
            data=json.dumps(USER_DATA_VALID))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 201
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES[
            'added_to_center'].format(USER_DATA_VALID['name'], new_center.name)
        assert response_json['data']['name'] == USER_DATA_VALID['name']
        assert response_json['data']['email'] == USER_DATA_VALID['email']
        assert response_json['data']['imageUrl'] == USER_DATA_VALID['imageUrl']
        assert response_json['data']['status'] == 'enabled'
        assert 'roleId' not in response_json['data']
        assert 'centerId' not in response_json['data']
        assert type(response_json['data']['role']) is dict
        assert type(response_json['data']['center']) is dict
        assert response_json['data']['role']['id'] == new_custom_role.id
        assert response_json['data']['role']['title'] == new_custom_role.title
        assert response_json['data']['role'][
            'description'] == new_custom_role.description
        assert response_json['data']['center']['id'] == new_center.id
        assert response_json['data']['center'][
            'staffCount'] == new_center.user_count
        assert response_json['data']['center']['name'] == new_center.name
