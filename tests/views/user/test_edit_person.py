"""Module for edit person endpoint"""

from flask import json

from api.utilities.constants import CHARSET, MIMETYPE
from api.models import Center, Role, User
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import (serialization_errors,
                                                   jwt_errors)
from tests.mocks.user import (USER_DATA_VALID, INVALID_FIELDS,
                              USER_EMAIL_ALREADY_EXISTS)

# app config
from config import AppConfig

API_V1_BASE_URL = AppConfig.API_BASE_URL_V1


class TestEditPersonEndpoint:
    """
    Tests endpoint for editing a person
    """

    def test_edit_person_should_pass_with_valid_request(
            self, init_db, client, auth_header, user_with_role, new_user):
        """
        Should return an 200 status code and updated user data when data provided
        in request is valid
        Parameters:
            init_db(object): fixture to initialize the test database
            client(object): fixture to get flask test client
            auth_header(dict): fixture to get token
            user_with_role(object): fixture to get user
        """
        new_user.save()
        USER_DATA_VALID['email'] = 'stevo@andela.com'
        new_user_with_role, _ = user_with_role
        new_user = new_user_with_role.save()
        user_update = json.dumps({
            'name': USER_DATA_VALID['name'],
            'email': USER_DATA_VALID['email'],
            'image_url': USER_DATA_VALID['imageUrl'],
            'roleId': new_user.role_id,
            'centerId': new_user.center_id,
            'status': 'diSablEd'  # case insensitive
        })
        center = Center.get(new_user.center_id)
        role = Role.get(new_user.role_id)
        response = client.patch(
            f'{API_V1_BASE_URL}/people/{new_user.token_id}',
            data=user_update,
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES[
            'person_updated'].format(USER_DATA_VALID['name'])
        assert response_json['data']['name'] == USER_DATA_VALID['name']
        assert response_json['data']['email'] == USER_DATA_VALID['email']
        assert response_json['data']['status'] == 'disabled'
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
        Assertions for expected role data in response body
        """
        assert response_json['data']['role']['id'] == role.id
        assert response_json['data']['role']['title'] == role.title
        assert response_json['data']['role']['description'] == role.description
        """
        Assertions for expected center data in response body
        """
        assert response_json['data']['center']['id'] == center.id
        assert response_json['data']['center'][
            'staffCount'] == center.user_count
        assert response_json['data']['center']['name'] == center.name

    def test_edit_person_should_update_partial_attrributes(
            self, client, init_db, auth_header, new_user, user_with_role):
        """
        Should return an 200 status code when partial valid fields are
        supplied for update
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user(BaseModel): fixture for creating a user
            new_center(BaseModel): fixture for creating a center
        """
        new_user_with_role, _ = user_with_role
        new_user = new_user_with_role.save()
        """
        Update only name of new user
        """
        user_update = {
            'name': 'Christiano Ronaldo',
        }
        response = client.patch(
            f'{API_V1_BASE_URL}/people/{new_user.token_id}',
            headers=auth_header,
            data=json.dumps(user_update))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['data']['name'] == user_update['name']
        """
        Update only centerId of new user
        """
        user_update = {
            'centerId': new_user.center_id,
        }
        center = Center.get(new_user.center_id)
        response = client.patch(
            f'{API_V1_BASE_URL}/people/{new_user.token_id}',
            headers=auth_header,
            data=json.dumps(user_update))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['data']['center']['name'] == center.name
        assert response_json['data']['center']['id'] == center.id
        """
        Update only status and email of new user
        """
        user_update = {
            'status': 'disabled',
            'email': 'odogwu_akataka@andela.com'
        }
        response = client.patch(
            f'{API_V1_BASE_URL}/people/{new_user.token_id}',
            headers=auth_header,
            data=json.dumps(user_update))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['data']['status'] == user_update['status']
        assert response_json['data']['email'] == user_update['email']

    def test_edit_person_should_fail_with_no_valid_field(
            self, client, init_db, new_user, auth_header):
        """
        Should return an 400 status code when no valid field is supplied
        in request body
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            user_with_role(BaseModel): fixture for creating a user
        """
        user_update = {
            'color': 'green white green',
            'unrelated': 'unrelated field',
        }
        response = client.patch(
            f'{API_V1_BASE_URL}/people/{new_user.token_id}',
            headers=auth_header,
            data=json.dumps(user_update))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['_schema'][0] == serialization_errors[
            'not_provided']

    def test_edit_person_should_fail_with_invalid_input_data(
            self, client, new_user, auth_header):
        """
        Should return an 400 status code when an invalid name, email,
        imageUrl, status, roleId and centerId fields are provided
        Parameters:
            client(object): fixture to get flask test client
            auth_header(dict): fixture to get token
            new_user(object): fixture to get user
        """

        user = json.dumps(INVALID_FIELDS)
        response = client.patch(
            f'{API_V1_BASE_URL}/people/{new_user.token_id}',
            data=user,
            headers=auth_header)
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

    def test_edit_person_should_fail_with_unsuccessful_authentication(
            self, client, new_user):
        """
        Test should fail when editing a person without a token
        Parameters:
            client(object): fixture to get flask test client
            new_user(object): fixture to get user
        """
        # When no token is provided
        user = json.dumps({'name': 'John'})
        response = client.patch(
            f'{API_V1_BASE_URL}/people/{new_user.id}', data=user)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']
        """
        Should fail when invalid toke is provided
        """
        response = client.patch(
            f'{API_V1_BASE_URL}/people/{new_user.id}',
            headers={
                'Authorization': "Bearer XXXX",
                'Content-Type': MIMETYPE,
                'Accept': MIMETYPE
            },
            data=user)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['INVALID_TOKEN_MSG']

    def test_edit_person_should_fail_with_unexisting_role(
            self, client, auth_header, new_user):
        """
        Should return an 400 status code when the specified role does not
        exist in database
        Parameters:
            client(object): fixture to get flask test client
            auth_header(dict): fixture to get token
            new_user(object): fixture to get user
        """
        new_user.save()
        user = json.dumps({'name': 'Anaeze', 'roleId': 'Ops'})
        response = client.patch(
            f'{API_V1_BASE_URL}/people/{new_user.id}',
            data=user,
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'not_found'].format('Role')

    def test_edit_person_should_fail_with_invalid_id(self, client,
                                                     auth_header):
        """
        Should return a 400 error response when person_id parameter is invalid
        Parameters:
            client(object): fixture to get flask test client
            auth_header(dict): fixture to get token
        """

        user = json.dumps({'name': 'Anaeze', 'roleId': 'Ops'})
        response = client.patch(
            f'{API_V1_BASE_URL}/people/@invalid_id@',
            data=user,
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors['invalid_id']

    def test_edit_person_should_fail_with_unexisting_center(
            self, client, user_with_role, auth_header):
        """
        Should return an 404 status code when the specified center does not
        exist in the database
        Parameters:
            client(object): fixture to get flask test client
            auth_header(dict): fixture to get token
            user_with_role(object): fixture to generate new user
        """
        new_user_with_role, _ = user_with_role
        new_user = new_user_with_role.save()
        user = json.dumps({
            'name': 'Anaeze',
            'centerId': 'unexisting_centerId'
        })
        response = client.patch(
            f'{API_V1_BASE_URL}/people/{new_user.token_id}',
            data=user,
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'not_found'].format('Center')

    def test_edit_person_should_fail_with_unexisting_person_id(
            self, client, auth_header):
        """
        Should return a 404 error response when person to be updated does
        not exist
        Parameters:
            client(object): fixture to get flask test client
            auth_header(dict): fixture to get token
        """
        user = json.dumps({
            'name': 'Anaeze',
            'email': 'shakitibobo@andela.com'
        })
        response = client.patch(
            f'{API_V1_BASE_URL}/people/unexisting_person_id',
            data=user,
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'not_found'].format('User')

    def test_edit_user_should_fail_with_already_existing_archived_user_email(
            self, client, init_db, auth_header, request_ctx,
            mock_request_obj_decoded_token, new_user):
        """
        Should return an 404 status code when supplied email owned by an
        archived/deleted user
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user(BaseModel): fixture for creating a user
            new_center(BaseModel): fixture for creating a center
        """
        token_id = new_user.token_id
        new_user.delete()
        new_user2 = {
            'name': 'Ayo',
            'email': 'testemail@gmail.com',
            'image_url': 'image.com/url',
            'token_id': '-LLEciLeGnBLmwwP5-F6'
        }
        response = client.patch(
            f'{API_V1_BASE_URL}/people/{token_id}',
            headers=auth_header,
            data=json.dumps(new_user2))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'not_found'].format("User")

    def test_edit_user_should_fail_with_already_existing_archived_user_email(
            self, client, init_db, auth_header, request_ctx,
            mock_request_two_obj_decoded_token, new_user):
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
        new_user.save()
        new_user.update_(delete=True)
        new_user.save()

        response = client.patch(
            f'{API_V1_BASE_URL}/people/{new_user.token_id}',
            headers=auth_header,
            data=json.dumps({"email": "testemail@andela.com"}))
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 409
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'exists'].format("Email")
