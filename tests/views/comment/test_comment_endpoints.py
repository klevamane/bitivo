""" Testing comments resource endpoints."""

# Third party libraries
from flask import json

# Utilities
from api.utilities.constants import CHARSET
from api.utilities.messages.error_messages import serialization_errors, database_errors
from api.utilities.messages.success_messages import SUCCESS_MESSAGES

# Mocks
from tests.mocks.comment import (
    MISSING_FIELD_COMMENT, INVALID_REQUEST_ID_COMMENT, EMPTY_BODY_MESSAGE,
    INVALID_PARENT_TYPE_COMMENT)
import json

# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestCommentEndpoints:
    """ Tests endpoints on comment module. """

    def test_create_comment_with_missing_fields_fails(self, client, init_db,
                                                      auth_header_two, new_user):
        """ Should fail when parentId is missing in data.
        Args:
            client (object): Fixture to get flask test client
            init_db (object): Used to create the database structure using the models
            auth_header_two (dict): Fixture to get token
        """
        new_user.save()
        data = json.dumps(MISSING_FIELD_COMMENT)
        response = client.post(
            f'{API_BASE_URL_V1}/comments', headers=auth_header_two, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response.json['errors']['parentId'][0] == serialization_errors[
            'field_required']

    def test_create_comment_with_invalid_parent_id_for_request_fails(
            self, client, init_db, auth_header_two, new_user):
        """ Should fail when requestId is invalid in data.
        Args:
            client (object): Fixture to get flask test client
            init_db (object): Used to create the database structure using the models
            auth_header_two (dict): Fixture to get token
        """
        new_user.save()
        data = json.dumps(INVALID_REQUEST_ID_COMMENT)
        response = client.post(
            f'{API_BASE_URL_V1}/comments', headers=auth_header_two, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json["status"] == "error"
        assert response_json["message"] == "Request not found"

    def test_create_comment_with_empty_body_fails(self, client, init_db,
                                                  auth_header_two, new_request):
        """ Should fail when invalid body message is provided.
        Args:
            client (object): Fixture to get flask test client
            init_db (object): Used to create the database structure using the models
            auth_header_two (dict): Fixture to get token
            new_request (object): Fixture for creating a new request

        """
        new_request.save()

        # Add a requestId to EMPTY_BODY_MESSAGE data
        EMPTY_BODY_MESSAGE['parentId'] = new_request.id

        data = json.dumps(EMPTY_BODY_MESSAGE)
        response = client.post(
            f'{API_BASE_URL_V1}/comments', headers=auth_header_two, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response.json['errors']['body'][0] == serialization_errors[
            'not_empty']

    def test_create_comment_with_valid_data_succeeds(self, client, init_db,
                                                     auth_header_two, new_request):
        """ Should succeed when correct data is given.
        Args:
            client (object): Fixture to get flask test client
            init_db (object): Used to create the database structure using the models
            auth_header_two (dict): Fixture to get token
            new_request (object): Fixture for creating a new request

        """
        new_request.save()

        # Add a requestId to MISSING_FIELD_COMMENT data
        MISSING_FIELD_COMMENT['parentId'] = new_request.id

        data = json.dumps(MISSING_FIELD_COMMENT)
        response = client.post(
            f'{API_BASE_URL_V1}/comments', headers=auth_header_two, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 201
        assert response_json["status"] == "success"
        assert response_json["message"] == SUCCESS_MESSAGES["created"].format(
            "Comment")

    def test_author_delete_comment_succeeds(self, client, auth_header_two, init_db,
                                            new_comment):
        """ Tests delete comment succeeds
    
        Args:
            client (object): Fixture to get flask test client.
            auth_header_two (dict): Fixture to get token.
            init_db (func): Initialises the database.
            new_comment (object): Fixture to create a new comment.

        """

        comment = new_comment.save()
        response = client.delete(
            f'{API_BASE_URL_V1}/comments/{comment.id}', headers=auth_header_two)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['deleted'].format(
            'Comment')

    def test_non_comment_author_delete_comment_fails(
            self, init_db, client, auth_header_two, new_comment2):
        """ Tests delete comment fails
    
        Args:
            client (object): Fixture to get flask test client.
            auth_header_two (dict): Fixture to get token.
            init_db (func): Initialises the database.
            new_comment2 (obj): Fixture to create a new comment.

        """

        new_comment2.save()
        response = client.delete(
            f'{API_BASE_URL_V1}/comments/{new_comment2.id}',
            headers=auth_header_two)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'delete_error'].format('Comment')

    def test_delete_comment_with_non_existing_comment_id_fails(
            self, client, auth_header_two, init_db):
        """ Tests delete comment fails

        Args:
            client (object): Fixture to get flask test client.
            auth_header_two (dict): Fixture to get token.
            init_db (object): Used to create the database structure using the models.

        """

        response = client.delete(
            f'{API_BASE_URL_V1}/comments/fkndhinknef4nj', headers=auth_header_two)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == database_errors[
            'non_existing'].format('Comment')

    def test_delete_with_already_deleted_comment_fails(
            self, client, auth_header_two, init_db, delete_comment):
        """ Tests delete already deleted comment fails

        Args:
            client (object): Fixture to get flask test client.
            auth_header_two (dict): Fixture to get token.
            init_db (func): Initialises the database.
            delete_comment (object): Fixture to create a soft deleted comment.

        """

        comment = delete_comment.save()
        response = client.delete(
            f'{API_BASE_URL_V1}/comments/{comment.id}', headers=auth_header_two)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'not_found'].format('Comment')

    def test_get_comment_with_existing_request_succeeds(
            self, client, init_db, auth_header_two, new_request):
        """ Should succeed when correct data is given.

        Args:
            client (object): Fixture to get flask test client
            auth_header_two (dict): Fixture to get token
            init_db (object): Fixture for initializing test database
            new_request (Request): Fixture for getting test request data
        """
        new_request.save()
        response = client.get(
            f'{API_BASE_URL_V1}/requests/{new_request.id}/comments',
            headers=auth_header_two)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert 'deleted' in response_json['data'][0]

    def test_get_deleted_comment_with_existing_request_succeeds(
            self, client, init_db, auth_header_two, new_request, delete_comment):
        """ Should succeed when response contains deleted comment.

        Args:
            client (object): Fixture to get flask test client
            auth_header_two (dict): Fixture to get token
            init_db (object): Fixture for initializing test database
            new_request (Request): Fixture for getting test request data
            delete_comment (Comment): Fixture for getting deleted comment data
        """
        new_request.save()
        delete_comment.save()
        response = client.get(
            f'{API_BASE_URL_V1}/requests/{new_request.id}/comments',
            headers=auth_header_two)
        response_json = response.json
        deleted_comment = [
            comment for comment in response.json.get('data')
            if comment['id'] == delete_comment.id
        ]

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert 'deleted' in response_json['data'][0]
        assert deleted_comment[0]['deleted'] is True

    def test_get_comment_with_non_existing_request_id_fails(
            self, client, init_db, auth_header_two):
        """ Should succeed when correct data is given.

        Args:
            client (object): Fixture to get flask test client
            auth_header_two (dict): Fixture to get token
            init_db (object): Fixture for initializing test database
        """
        response = client.get(
            f'{API_BASE_URL_V1}/requests/-LSzoQVBqszg8VD7ynVR/comments',
            headers=auth_header_two)
        assert response.status_code == 404

    def test_get_comment_including_the_comment_creator_image_url_succeeds(
            self, client, auth_header_two, new_request, new_user):
        """ Should succeed when correct data is given.

        Args:
            client (object): Fixture to get flask test client
            auth_header_two (dict): Fixture to get token
            init_db (object): Fixture for initializing test database
            new_request (Request): Fixture for getting test request data
            new_user (dict): fixture to create a new user
        """
        new_request.save()
        response = client.get(
            f'{API_BASE_URL_V1}/requests/{new_request.id}/comments',
            headers=auth_header_two)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert "imageUrl" in response_json["data"][0]['author']
        assert new_user.image_url == response_json["data"][0]['author'][
            'imageUrl']

    def test_create_comment_with_invalid_parent_type_fails(
            self, client, init_db, auth_header_two, new_request):
        """ Should fail when invalid parent type is given.
        Args:
            client (object): Fixture to get flask test client
            init_db (object): Used to create the database structure using the models
            auth_header_two (dict): Fixture to get token
            new_request (object): Fixture for creating a new request

        """
        new_request.save()

        # Add a parentId to INVALID_PARENT_TYPE_COMMENT data
        INVALID_PARENT_TYPE_COMMENT['parentId'] = new_request.id

        data = json.dumps(INVALID_PARENT_TYPE_COMMENT)
        response = client.post(
            f'{API_BASE_URL_V1}/comments', headers=auth_header_two, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json['message'] == serialization_errors[
            'invalid_choice'].format('parentType', ['Request', 'Schedule'])
