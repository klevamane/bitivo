"""
    Module with tests for update comment endpoint
"""

from flask import json

from api.utilities.constants import CHARSET
from api.utilities.messages.error_messages import jwt_errors, database_errors
from api.utilities.messages.error_messages import (serialization_errors)

from tests.mocks.comment import (COMMENT_UPDATE_BODY, EMPTY_BODY_MESSAGE)

# app config
from config import AppConfig

API_V1_BASE_URL = AppConfig.API_BASE_URL_V1


class TestUpdateCommentEndpoint:
    """Update Comment endpoint """

    def test_update_comment_with_valid_data_succeeds(self, client, auth_header,
                                                     init_db, new_comment):
        """Should pass with valid update data
        
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            init_db(SQLAlchemy): fixture to initialize the test database
            new_comment (object): Fixture for a new comment 
        """
        new_comment.save()
        data = json.dumps(COMMENT_UPDATE_BODY)
        response = client.patch(
            f'{API_V1_BASE_URL}/comments/{new_comment.id}',
            data=data,
            headers=auth_header)
        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['data']['body'] == COMMENT_UPDATE_BODY['body']

    def test_update_comment_with_no_token_fails(self, client, new_comment,
                                                init_db):
        """Should fail with no token
        
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            new_comment (object): Fixture for a new comment 
        """
        new_comment.save()
        data = json.dumps(COMMENT_UPDATE_BODY)
        response = client.patch(
            f'{API_V1_BASE_URL}/comments/{new_comment.id}', data=data)
        assert response.status_code == 401
        assert response.json['status'] == 'error'
        assert response.json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_update_comment_with_invalid_token_fails(self, client, new_comment,
                                                     init_db):
        """Should fail with invalid token
        
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            new_comment (object): Fixture for a new comment 
        """
        new_comment.save()
        data = json.dumps(COMMENT_UPDATE_BODY)
        response = client.patch(
            f'{API_V1_BASE_URL}/comments/{new_comment.id}',
            data=data,
            headers={'Authorization': "Bearer invalid"})
        assert response.status_code == 401
        assert response.json['status'] == 'error'
        assert response.json['message'] == jwt_errors['INVALID_TOKEN_MSG']

    def test_update_non_existing_comment_fails(self, client, init_db,
                                               auth_header):
        """Should fail if comment id doesnt exist
        
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            init_db(SQLAlchemy): fixture to initialize the test database
            new_comment (object): Fixture for a new comment 
        """
        data = json.dumps(COMMENT_UPDATE_BODY)
        response = client.patch(
            f'{API_V1_BASE_URL}/comments/addfgfd',
            data=data,
            headers=auth_header)
        assert response.status_code == 404
        assert response.json['status'] == 'error'
        assert response.json['message'] == database_errors[
            'non_existing'].format('Comment')

    def test_update_comment_with_no_data_fails(self, client, init_db,
                                               auth_header, new_comment):
        """Should fail if no update data is sent in the request
        
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            init_db(SQLAlchemy): fixture to initialize the test database
            new_comment (object): Fixture for a new comment 
        """
        new_comment.save()
        data = json.dumps({})
        response = client.patch(
            f'{API_V1_BASE_URL}/comments/{new_comment.id}',
            data=data,
            headers=auth_header)
        assert response.status_code == 400
        assert response.json['status'] == "error"
        assert 'errors' in response.json
        assert len(response.json['errors']['body']) == 1
        assert response.json['errors']['body'][0] == serialization_errors[
            'field_required']
        assert response.json['message'] == 'An error occurred'

    def test_update_comment_with_empty_body_fails(self, client, init_db,
                                                  auth_header, new_comment):
        """Should fail with empty update body
        
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            init_db(SQLAlchemy): fixture to initialize the test database
            new_comment (object): Fixture for a new comment 
        """
        new_comment.save()
        data = json.dumps(EMPTY_BODY_MESSAGE)
        response = client.patch(
            f'{API_V1_BASE_URL}/comments/{new_comment.id}',
            data=data,
            headers=auth_header)
        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert len(response.json['errors']['body']) == 1
        assert response.json['errors']['body'][0] == serialization_errors[
            'not_empty']
        assert response.json['message'] == 'An error occurred'

    def test_update_comment_when_not_owner_fails(self, client, auth_header,
                                                 init_db, new_comment_user_two,
                                                 new_user):
        """Should fail when user is not owner of the comment
        
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            init_db(SQLAlchemy): fixture to initialize the test database
            new_comment_user_two (object): comment from a different user
        """
        comment = new_comment_user_two.save()
        data = json.dumps(COMMENT_UPDATE_BODY)
        response = client.patch(
            f'{API_V1_BASE_URL}/comments/{comment.id}',
            data=data,
            headers=auth_header)
        assert response.status_code == 403
        assert response.json['status'] == 'error'
        assert response.json['message'] == serialization_errors['not_owner']
