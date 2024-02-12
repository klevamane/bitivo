"""
Module of tests for user endpoints
"""
# System libraries
from unittest.mock import patch, Mock

# Third-party libraries
from flask import json

# Models
from api.models import User

# Constants
from api.utilities.constants import CHARSET

# Messages
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import (database_errors,
                                                   http_errors, jwt_errors)
# Mock data
from tests.mocks.user import (REQUESTER, INVALID_API_RESPONSE,
                              VALID_API_RESPONSE, EXTRA_ANDELA_USERS)

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1
API_STAGING = 'api.utilities.migration_helper.requests.get'


class TestMigratePeopleEndpoint:
    """
    Tests endpoint for migrating users to activo from api-staging
    """

    def test_migrate_people_fails_when_no_token_provided(
            self, client, init_db):
        """Should return an 401 status code and error message when requesting
        to migrate without authorization

        Args:
            client (FlaskClient): Fixture to get flask test client
            init_db (SQLAlchemy): Fixture to initialize the test database
        """
        response = client.post(f'{BASE_URL}/people/migrate')
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_migrate_people_returns_a_success_response(self, client, init_db,
                                                       auth_header, new_user):
        """Should return an 200 status code and success message notifying the
        user of scheduled migration

        Args:
            client (FlaskClient): Fixture to get flask test client
            init_db (SQLAlchemy): Fixture to initialize the test database
            auth_header (dict): Fixture to get token
        """
        from api.tasks.migration import Migrations

        Migrations.migrate_users.delay = Mock()
        new_user.save()

        response = client.post(
            f'{BASE_URL}/people/migrate', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['migrated'].format(
            'Users')

    @patch(API_STAGING)
    def test_user_sent_invalid_response_mail_with_invalid_api_response(
            self, mock_get, init_db):
        """User should be sent an email when api-staging returns invalid
        response data

        Args:
            mock_get (object): Fixture for mocking the get request response
            init_db (SQLAlchemy): Fixture to initialize the test database
        """
        from api.tasks.email_sender import Email
        from api.tasks.migration import Migrations

        Email.send_mail.delay = Mock()

        mock_get.return_value.json.return_value = {
            "values": INVALID_API_RESPONSE
        }
        requester = REQUESTER
        headers = {'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIs'}
        Migrations.migrate_users.s(requester, headers).apply()

        # assert that error response email is sent to user when invalid
        # data from api-staging is returned
        title = 'Activo User Migration'
        body = http_errors['invalid_response'].format('api-staging')
        Email.send_mail.delay.assert_called_once_with(
            title, [requester['email']], body)

    @patch(API_STAGING)
    def test_user_is_sent_success_email_with_no_skipped_records(
            self, mock_get, init_db):
        """Requester should be sent a success email containing an empty
        list of skipped records upon first migration

        Args:
            mock_get (object): Fixture for mocking the get request response
            init_db (SQLAlchemy): Fixture to initialize the test database
        """
        from api.tasks.email_sender import Email
        from api.tasks.migration import Migrations

        # Mock functions to test
        Email.send_mail.delay = Mock()
        mock_get.return_value.json.return_value = {
            "values": VALID_API_RESPONSE
        }
        requester = REQUESTER
        headers = {'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIs'}
        Migrations.migrate_users.s(requester, headers).apply()

        title = 'Activo User Migration'
        skipped = []  # empty list of skipped records
        body = database_errors['skipped'].format(requester['first_name'],
                                                 'people', json.dumps(skipped))

        # assert that email is sent to user with list of skipped records
        Email.send_mail.delay.assert_called_once_with(
            title, [requester['email']], body)

    @patch(API_STAGING)
    def test_user_is_sent_success_email_with_skipped_records(
            self, mock_get, init_db):
        """Requester should be sent a success email containing a list
        of skipped records upon second migration

        Args:
            mock_get (object): Fixture for mocking the get request response
            init_db (SQLAlchemy): Fixture to initialize the test database
        """
        from api.tasks.email_sender import Email
        from api.tasks.migration import Migrations

        # Mock functions to test
        Email.send_mail.delay = Mock()
        mock_get.return_value.json.return_value = {
            "values": VALID_API_RESPONSE
        }
        requester = REQUESTER
        headers = {'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIs'}
        Migrations.migrate_users.s(requester, headers).apply()

        title = 'Activo User Migration'
        skipped = [user['email']
                   for user in VALID_API_RESPONSE]  # list of skipped records
        body = database_errors['skipped'].format(requester['first_name'],
                                                 'people', json.dumps(skipped))

        # assert that email is sent to user with list of skipped records
        Email.send_mail.delay.assert_called_once_with(
            title, [requester['email']], body)

    @patch(API_STAGING)
    def test_user_count_increases_after_new_users_migration(
            self, mock_get, init_db):
        """The count of users in activo database should be increased to reflect
        new users migrated from api-staging

        Args:
            mock_get (object): Fixture for mocking the get request response
            init_db (SQLAlchemy): Fixture to initialize the test database
        """
        from api.tasks.migration import Migrations
        initial_count = User.count()

        new_data = VALID_API_RESPONSE.copy()
        new_data.extend(EXTRA_ANDELA_USERS)
        # Assert that new_data contain 5 users (3 existing and 2 new)
        assert len(new_data) == 5

        mock_get.return_value.json.return_value = {"values": new_data}
        requester = REQUESTER
        headers = {'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIs'}
        Migrations.migrate_users.s(requester, headers).apply()

        final_count = User.count()
        assert final_count > initial_count
        assert final_count - initial_count == 2
