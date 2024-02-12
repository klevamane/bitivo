""" Testing get a schedule comment resource"""

# Third party libraries
from flask import json

# Standard Mock library
from unittest.mock import Mock
from api.tasks.notifications.comment import CommentNotifications

# Utilities
from api.utilities.constants import CHARSET
from api.utilities.messages.error_messages import serialization_errors
from api.utilities.messages.error_messages import jwt_errors
from api.utilities.messages.success_messages import SUCCESS_MESSAGES

import json

# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestScheduleComment:
    """ Test comment schedule endpoint """

    def test_get_schedule_comment_unauthorized(self, client, init_db):
        """
        Should return jwt error when token is not provided

        Args:
            client (object): Fixture to get flask test client
            init_db (object): Fixture for initializing test database
        """

        response = client.get(
            f'{API_BASE_URL_V1}/schedules/-LSzoQVBqszg8VD7ynVR/comments')

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json["status"] == "error"
        assert response_json["message"] == jwt_errors['NO_TOKEN_MSG']

    def test_get_schedule_comment_with_non_existing_schedule_id_fails(
            self, client, init_db, auth_header, new_user):
        """ Should fail when schedule_id is not found in the comment table.

        Args:
            client (object): Fixture to get flask test client
            auth_header (dict): Fixture to get token
            init_db (object): Fixture for initializing test database
        """
        new_user.save()
        response = client.get(
            f'{API_BASE_URL_V1}/schedules/-LSzoQVBqszg8VD7ynVR/comments',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'not_found'].format('Schedule')

    def test_get_schedule_comment_succeeds(self, client, init_db, auth_header,
                                           new_schedule_comment, new_user):
        """ Should succeed when valid data is given. 

        Args:
            client (object): Fixture to get flask test client
            auth_header (dict): Fixture to get token
            init_db (object): Fixture for initializing test database
            new_schedule_comment (Comment): Fixture for getting test comment data
        """
        new_user.save()
        new_schedule_comment.save()
        response = client.get(
            f'{API_BASE_URL_V1}/schedules/{new_schedule_comment.parent_id}/comments',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json["message"] == SUCCESS_MESSAGES[
            'successfully_fetched'].format('Comments')
