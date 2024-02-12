"""
    Module with tests for update center endpoint
"""

from flask import json

from api.utilities.constants import CHARSET
from api.utilities.messages.error_messages import serialization_errors, jwt_errors
from tests.mocks.center import (VALID_CENTER, NEW_CENTER, INVALID_CENTER,
                                VALID_CENTER_TWO, INVALID_CENTER_NAME)

# app config
from config import AppConfig

API_V1_BASE_URL = AppConfig.API_BASE_URL_V1


class TestUpdateCenterEndpoint:
    """
    Update Center endpoint tests
    """

    def test_updates_center_successfully(
            self,
            client,
            auth_header,
            init_db,  #pylint: disable=W0613
            new_center,
            new_user):
        """
        Test center can be updated

        Parameters:
            client(object): fixture to get the flask test client
            auth_header(dict): fixture to get the token
            init_db(object): fixture to initialize the test database
            new_center: fixture to get a new Center Object
        """
        new_user.save()
        new_center.created_by = new_user.token_id
        new_center.save()
        updated_center = json.dumps(NEW_CENTER)

        response = client.patch(
            f'{API_V1_BASE_URL}/centers/{new_center.id}',
            data=updated_center,
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['data']['name'] == NEW_CENTER['name']

    def test_returns_center_not_found(self, client, auth_header):
        """
            Test that a 404 is returned when trying to edit a none
            existing center

            Parameters:
                client(object): fixture to get the flask test client
                auth_header(dict): fixture to get the token
        """

        updated_center = json.dumps(VALID_CENTER)

        response = client.patch(
            f'{API_V1_BASE_URL}/centers/L0jutmaukdahj1',
            data=updated_center,
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'

    def test_fails_when_no_token_present(self, client, new_center):
        """
        Test that a no token error message is returned when no
        token is in header

        Parameters:
            client(object): a fixture to get the flask test client
            new_center(object): the center object already in the DB
        """

        updated_center = json.dumps(VALID_CENTER)

        response = client.patch(
            f'{API_V1_BASE_URL}/centers/{new_center.id}', data=updated_center)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_rejects_duplicate_center(self, client, auth_header, new_center):
        """
        Test that update to an existing center name
        is rejected

        Parameters:
            client(object): a fixture to get flask test client
            auth_header(dict): a fixture with authorization token
            new_center(object): the center object already in the DB
        """

        new_center.save()
        center = json.dumps(VALID_CENTER)

        client.post(
            f'{API_V1_BASE_URL}/centers', data=center, headers=auth_header)

        response = client.patch(
            f'{API_V1_BASE_URL}/centers/{new_center.id}',
            data=center,
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 409
        assert response_json["message"] == serialization_errors[
            'exists'].format('Lagos Center')
        assert response_json["status"] == "error"

    def test_fails_with_invalid_data(self, client, auth_header, new_center):
        """
        Test that an error is returned when updating
        a center with invalid data. The invalid data is
        a center with a name containing only numbers

        Parameters:
            client(object): fixture to get flask test client
            auth_header(dict): fixture to get token
            new_center(object): the center object already in the DB
        """

        center = json.dumps(INVALID_CENTER)

        response = client.patch(
            f'{API_V1_BASE_URL}/centers/{new_center.id}',
            data=center,
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['name'][0] == serialization_errors[
            'string_characters']

    def test_fails_with_invalid_center_name(self, client, auth_header,
                                            new_center):
        """
        Test that an error is returned when updating
        a center with invalid center. The invalid data is
        a center with a name containing such characters
        as #!>%

        Parameters:
            client(object): fixture to get flask test client
            auth_header(dict): fixture to get token
            new_center(object): the center object already in the DB
        """

        center = json.dumps(INVALID_CENTER_NAME)

        response = client.patch(
            f'{API_V1_BASE_URL}/centers/{new_center.id}',
            data=center,
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['name'][0] == serialization_errors[
            'string_characters']

    def test_fails_with_invalid_image_data(self, client, auth_header,
                                           new_center):
        """
        Test that an error is returned when updating
        a center with invalid data. The invalid data is
        a center with an image that is a string

        Parameters:
            client(object): fixture to get flask test client
            auth_header(dict): fixture to get token
            new_center(object): the center object already in the DB
        """

        center = json.dumps(VALID_CENTER_TWO)

        response = client.patch(
            f'{API_V1_BASE_URL}/centers/{new_center.id}',
            data=center,
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
