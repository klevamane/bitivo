"""Module to test endpoint to delete a person"""
from flask import json

from api.models import Center, User
from api.utilities.constants import CHARSET, MIMETYPE
from api.utilities.messages.error_messages import (jwt_errors,
                                                   serialization_errors)
from api.utilities.messages.success_messages import SUCCESS_MESSAGES

# app config
from config import AppConfig

API_V1_BASE_URL = AppConfig.API_BASE_URL_V1


class TestDeletePersonEndpoint:
    """Tests endpoint to delete a person"""

    def test_delete_person_should_fail_with_unsuccessful_authentication(
            self, init_db, client, new_role):  # pylint: disable=W0613
        """
        Should return a 401 error response when token is not provided
        or invalid

        :param client: request client fixture
        :return: None
        """

        center = Center(name='Lagos', image={'url': 'image url'})
        center.save()
        new_role.save()
        person = User(
            name='Tony',
            email='tony@example.com',
            image_url='url',
            token_id='-LLEciLeGnBLmwwP5-b0',
            role_id=new_role.id,
            center_id=center.id)
        person.save()

        # when no token is provided
        response = client.delete(f'{API_V1_BASE_URL}/people/{person.id}')
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

        # when token provided is invalid
        response = client.delete(
            f'{API_V1_BASE_URL}/people/{person.token_id}',
            headers={
                'Authorization': "Bearer XXXX",
                'Content-Type': MIMETYPE,
                'Accept': MIMETYPE
            })
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['INVALID_TOKEN_MSG']

    def test_delete_person_should_fail_with_invalid_person_id(
            self, init_db, client, auth_header, new_user):  # pylint: disable=W0613
        """
        Should return a 400 error response when person_id parameter is invalid

        :param init_db: initialize the database
        :param client: request client
        :param auth_header: authentication header
        :return: None
        """
        new_user.save()
        response = client.delete(
            f'{API_V1_BASE_URL}/people/@invalid_id@', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors['invalid_id']

    def test_delete_person_should_fail_with_unexisting_person_id(
            self, init_db, client, auth_header):  # pylint: disable=W0613
        """
        Should return a 404 error response when person to be deleted does
        not exist

        :param client: request client fixture
        :param auth_header: authentication header fixture
        :return: None
        """

        response = client.delete(
            f'{API_V1_BASE_URL}/people/non_existing_id', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'not_found'].format('User')

    def test_delete_person_should_fail_when_person_already_deleted(
            self, init_db, client, auth_header, request_ctx,
            mock_request_obj_decoded_token, new_role, new_user):  # pylint: disable=W0613
        """
        Should return a 404 error response when person to be deleted has
        already been deleted

        :param client: request client fixture
        :param auth_header: authentication header fixture
        :return: None
        """

        center = Center(name='Cairo', image={'url': 'image url'})
        center.save()
        new_user.save()
        new_role.save()
        person = User(
            name='Mary',
            email='mary@example.com',
            token_id='-LLEciLeGnBLmwwP5-q0',
            image_url='url',
            role_id=new_role.id,
            center_id=center.id,
            created_by=new_user.token_id)
        person.save()

        response = client.delete(
            f'{API_V1_BASE_URL}/people/{person.id}', headers=auth_header)
        response = client.delete(
            f'{API_V1_BASE_URL}/people/{person.id}', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'not_found'].format('User')

    def test_delete_person_should_pass_when_request_is_valid(
            self, init_db, client, auth_header, new_role):
        """
        Should return a 200 OK success response when delete person request is
        successful

        :param init_db: initialize database fixture
        :param client: request client fixture
        :param auth_header: authentication header fixture
        :return: None
        """

        center = Center(name='Kampala', image={'url': 'image url'})
        center.save()
        new_role.save()
        person = User(
            name='Paul',
            email='paul@example.com',
            image_url='url',
            token_id='-LLEciLeGnBLmwwP5-x0',
            role_id=new_role.id,
            center_id=center.id)
        person.save()

        response = client.delete(
            f'{API_V1_BASE_URL}/people/{person.token_id}', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['deleted'].format(
            person.name)
