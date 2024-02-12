"""
Module of tests for user endpoints
"""
from flask import json

from api.utilities.constants import CHARSET, MIMETYPE
from api.utilities.messages.error_messages import (serialization_errors,
                                                   jwt_errors)
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from tests.mocks.user import (USER_DATA_INCOMPLETE, USER_DATA_VALID,
                              USER_EMAIL_ALREADY_EXISTS, INVALID_FIELDS,
                              USER_NON_ANDELAN_EMAIL, USER_DATA_NEW,
                              USER_NO_IMAGE_URL, INVALID_TOKEN)

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1


class TestUserEndpoints:
    """
    Tests endpoint for adding person to a center
    """

    def test_add_user_should_pass_with_valid_request(
            self, client, init_db, auth_header, new_center, new_custom_role):
        """
        Should return an 201 status code and new user data when data provided
        in request is valid
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_center(BaseModel): fixture for creating a center
            new_role(BaseModel): fixture for creating a role
        """

        new_center.save()
        new_custom_role.save()
        USER_DATA_NEW['roleId'] = new_custom_role.id
        USER_DATA_NEW['centerId'] = new_center.id
        response = client.post(
            f'{BASE_URL}/people',
            headers=auth_header,
            data=json.dumps(USER_DATA_NEW))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 201
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES[
            'added_to_center'].format(USER_DATA_NEW['name'], new_center.name)
        assert response_json['data']['name'] == USER_DATA_NEW['name']
        assert response_json['data']['email'] == USER_DATA_NEW['email']
        assert response_json['data']['imageUrl'] == USER_DATA_NEW['imageUrl']
        assert response_json['data']['status'] == 'enabled'
        """
        Ensure that `roleId` and `centerId` were not returned in response body
        """
        assert 'roleId' not in response_json['data']
        assert 'centerId' not in response_json['data']
        """
        Assertions for data type of role and center in response
        """
        assert type(response_json['data']['role']) is dict
        assert type(response_json['data']['center']) is dict
        """
        Assertions for expected role data in response
        """
        assert response_json['data']['role']['id'] == new_custom_role.id
        assert response_json['data']['role']['title'] == new_custom_role.title
        assert response_json['data']['role'][
            'description'] == new_custom_role.description
        """
        Assertions for expected center data in response
        """
        assert response_json['data']['center']['id'] == new_center.id
        assert response_json['data']['center'][
            'staffCount'] == new_center.user_count
        assert response_json['data']['center']['name'] == new_center.name

    def test_add_user_should_fail_with_existing_user(self, client, init_db,
                                                     auth_header, new_center):
        """
        Should return an 409 status code when the user exist in database

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_center(BaseModel): fixture for creating a center
        """
        USER_DATA_NEW['tokenId'] = '-LLEciLeGnBLmwwP5-C0'
        response = client.post(
            f'{BASE_URL}/people',
            headers=auth_header,
            data=json.dumps(USER_DATA_NEW))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 409
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            "exists"].format("Email")

    def test_add_user_should_fail_with_unexisting_role(
            self, client, init_db, auth_header, new_center):
        """
        Should return an 400 status code when the specified role does not
        exist in database

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_center(BaseModel): fixture for creating a center
        """

        new_center.save()
        USER_DATA_VALID['centerId'] = new_center.id
        USER_DATA_VALID['roleId'] = 'unexisting_role_id'
        response = client.post(
            f'{BASE_URL}/people',
            headers=auth_header,
            data=json.dumps(USER_DATA_VALID))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            "not_found"].format("Role")

    def test_add_user_should_fail_with_incomplete_data(
            self, client, init_db, auth_header, default_role):
        """
        Should return an 400 status code when data provided in request body has
        missing required field(s)

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_center(BaseModel): fixture for creating a center
        """

        default_role.save()
        response = client.post(
            f'{BASE_URL}/people',
            headers=auth_header,
            data=json.dumps(USER_DATA_INCOMPLETE))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['email'][0] == serialization_errors[
            'field_required']
        assert response_json['errors']['imageUrl'][0] == serialization_errors[
            'field_required']

    def test_add_user_should_fail_with_unsuccessful_authentication(
            self, client, init_db):
        """
        Should return a 401 error response when token is not provided
        or invalid

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            new_center(BaseModel): fixture for creating a center
        """
        # When no token is provided
        response = client.post(
            f'{BASE_URL}/people', data=json.dumps(USER_DATA_VALID))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_add_user_should_fail_with_invalid_token(self, client, init_db):
        """
        Should fail when invalid token is provided
        """
        response = client.post(
            f'{BASE_URL}/people',
            headers={
                'Authorization': "Bearer XXXX",
                'Content-Type': MIMETYPE,
                'Accept': MIMETYPE
            },
            data=json.dumps(USER_DATA_VALID))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['INVALID_TOKEN_MSG']

    def test_user_with_token_signed_with_hs256_fails(self, client, init_db):
        """
        Should fail when a token signed with a different algorithm is provided
        """
        response = client.post(
            f'{BASE_URL}/people',
            headers={
                'Authorization': f"Bearer {INVALID_TOKEN}",
                'Content-Type': MIMETYPE,
                'Accept': MIMETYPE
            },
            data=json.dumps(USER_DATA_VALID))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['ALGORITHM_ERROR']

    def test_add_user_should_fail_with_unexisting_center(
            self, client, init_db, new_custom_role, auth_header):
        """
        Should return an 404 status code when the specified center does not
        exist in the database

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """

        new_custom_role.save()
        USER_DATA_VALID['centerId'] = 'unexisting_center_id'
        USER_DATA_VALID['roleId'] = new_custom_role.id
        response = client.post(
            f'{BASE_URL}/people',
            headers=auth_header,
            data=json.dumps(USER_DATA_VALID))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            "not_found"].format("Center")

    def test_add_user_should_fail_with_invalid_fields(self, client, init_db,
                                                      auth_header):
        """
        Should return an 400 status code when an invalid name, email,
        imageUrl, status, roleId and centerId fields are provided

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        response = client.post(
            f'{BASE_URL}/people',
            headers=auth_header,
            data=json.dumps(INVALID_FIELDS))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['email'][0] == serialization_errors[
            'email_syntax']
        assert response_json['errors']['name'][0] == serialization_errors[
            'string_characters'].format(INVALID_FIELDS['name'])
        assert response_json['errors']['imageUrl'][0] == serialization_errors[
            'url_syntax'].format(INVALID_FIELDS['imageUrl'])
        assert response_json['errors']['status'][0] == serialization_errors[
            'invalid_status']
        assert response_json['errors']['roleId'][0] == serialization_errors[
            'invalid_id_field']

    def test_add_user_should_fail_with_already_existing_email(
            self, client, init_db, auth_header, new_custom_role, new_center,
            new_user):
        """
        Should return an 409 status code when supplied email is already being
        used by another user

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user(BaseModel): fixture for creating a user
            new_center(BaseModel): fixture for creating a center
        """
        new_center.save()
        new_custom_role.save()
        new_user.save()

        USER_EMAIL_ALREADY_EXISTS['email'] = new_user.email
        USER_EMAIL_ALREADY_EXISTS['centerId'] = new_center.id
        USER_EMAIL_ALREADY_EXISTS['roleId'] = new_custom_role.id

        response = client.post(
            f'{BASE_URL}/people',
            headers=auth_header,
            data=json.dumps(USER_EMAIL_ALREADY_EXISTS))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 409
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'exists'].format("Email")

    def test_add_user_should_fail_with_already_existing_email_in_uppercase(
            self, client, init_db, auth_header, new_custom_role, new_center,
            new_user):
        """
        Should return an 409 status code when supplied email is already being
        used by another user

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user(BaseModel): fixture for creating a user
            new_center(BaseModel): fixture for creating a center
        """
        new_center.save()
        new_custom_role.save()
        new_user.save()

        USER_EMAIL_ALREADY_EXISTS['email'] = new_user.email.upper()
        USER_EMAIL_ALREADY_EXISTS['centerId'] = new_center.id
        USER_EMAIL_ALREADY_EXISTS['roleId'] = new_custom_role.id

        response = client.post(
            f'{BASE_URL}/people',
            headers=auth_header,
            data=json.dumps(USER_EMAIL_ALREADY_EXISTS))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 409
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'exists'].format("Email")

    def test_add_user_should_fail_with_non_andela_email(
            self, client, init_db, auth_header, new_custom_role, new_center,
            new_user):
        """
        Should return an 400 status code when supplied email is not a valid
        andela email

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user(BaseModel): fixture for creating a user
            new_center(BaseModel): fixture for creating a center
        """
        new_center.save()
        new_custom_role.save()
        new_user.save()

        USER_NON_ANDELAN_EMAIL['centerId'] = new_center.id
        USER_NON_ANDELAN_EMAIL['roleId'] = new_custom_role.id

        response = client.post(
            f'{BASE_URL}/people',
            headers=auth_header,
            data=json.dumps(USER_NON_ANDELAN_EMAIL))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['email'][0] == serialization_errors[
            'email_syntax']

    def test_add_user_should_fail_with_already_existing_archived_user_email(
            self, client, init_db, auth_header, request_ctx,
            mock_request_two_obj_decoded_token, user_with_role):
        """
        Should return an 409 status code when supplied email owned by an
        archived/deleted user

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user(BaseModel): fixture for creating a user
            new_center(BaseModel): fixture for creating a center
        """
        new_user, role_id = user_with_role
        new_user.save()  # create new user
        new_user.delete()  # soft delete new user

        USER_EMAIL_ALREADY_EXISTS['email'] = new_user.email
        USER_EMAIL_ALREADY_EXISTS['centerId'] = new_user.center_id
        USER_EMAIL_ALREADY_EXISTS['roleId'] = role_id

        response = client.post(
            f'{BASE_URL}/people',
            headers=auth_header,
            data=json.dumps(USER_EMAIL_ALREADY_EXISTS))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 409
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'archived'].format("Email")

    def test_add_user_should_fail_with_already_existing_archived_user_token_id(
            self, client, init_db, auth_header, request_ctx,
            mock_request_two_obj_decoded_token, user_with_role):
        """
        Should return an 409 status code when supplied token id owned by an
        archived/deleted user

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user(BaseModel): fixture for creating a user
            new_center(BaseModel): fixture for creating a center
        """
        new_user, role_id = user_with_role
        new_user.save()  # create new user
        new_user.delete()  # soft delete new user

        USER_EMAIL_ALREADY_EXISTS['email'] = 'menna@andela.com'
        USER_EMAIL_ALREADY_EXISTS['tokenId'] = new_user.token_id
        USER_EMAIL_ALREADY_EXISTS['centerId'] = new_user.center_id
        USER_EMAIL_ALREADY_EXISTS['roleId'] = role_id

        response = client.post(
            f'{BASE_URL}/people',
            headers=auth_header,
            data=json.dumps(USER_EMAIL_ALREADY_EXISTS))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 409
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'archived'].format("Token Id")

    def test_add_user_should_fail_with_already_existing_token_id(
            self, client, init_db, auth_header, new_custom_role, new_center,
            new_user):
        """
        Should return an 409 status code when supplied token id is already being
        used by another user

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user(BaseModel): fixture for creating a user
            new_center(BaseModel): fixture for creating a center
        """
        new_center.save()
        new_custom_role.save()
        new_user.save()

        USER_EMAIL_ALREADY_EXISTS['tokenId'] = new_user.token_id
        USER_EMAIL_ALREADY_EXISTS['centerId'] = new_center.id
        USER_EMAIL_ALREADY_EXISTS['roleId'] = new_custom_role.id

        response = client.post(
            f'{BASE_URL}/people',
            headers=auth_header,
            data=json.dumps(USER_EMAIL_ALREADY_EXISTS))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 409
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'exists'].format("Token Id")

    def test_add_user_with_empty_image_url_fails(self, client, init_db,
                                                 auth_header):
        """
        Should return an 400 status code when an invalid imageUrl
        field is provided

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token

        Returns:
            an error message
        """
        response = client.post(
            f'{BASE_URL}/people',
            headers=auth_header,
            data=json.dumps(USER_NO_IMAGE_URL))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['imageUrl'][0] == serialization_errors[
            'url_syntax'].format(USER_NO_IMAGE_URL['imageUrl'])
