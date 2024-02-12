# Third party
from flask import json

# Utilities
from api.utilities.constants import CHARSET, MIMETYPE
from api.utilities.messages.error_messages import serialization_errors, jwt_errors
from api.utilities.messages.success_messages import SUCCESS_MESSAGES

# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestGetScheduleEndpoint:
    """Class for Schedule resource endpoints"""

    def test_get_schedule_assigned_to_user_succeeds(self, client, auth_header,
                                                    schedule_list):
        """Should return list of schedules when a valid assigneeId is passed

            Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            schedule_list: list of created schedule
        """
        assigneeId = schedule_list[0].assignee_id
        response = client.get(
            f'{API_BASE_URL_V1}/schedules?assigneeId={assigneeId}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data']

        assert response.status_code == 200
        assert type(response_data) == list
        assert 'assignee' in response_data[0]
        assert response_data[0]['assignee']['tokenId'] == assigneeId
        assert response_data[0]['status'] == 'pending'

    def test_get_schedule_list_should_with_invalid_token_fails(
            self, client, schedule_list):
        """Should fail when invalid token is provided

            Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            schedule_list: list of created schedule
        """
        assigneeId = schedule_list[0].assignee_id

        response = client.get(
            f'{API_BASE_URL_V1}/schedules?assigneeId={assigneeId}',
            headers={
                'Authorization': "Bearer XXXX",
                'Content-Type': MIMETYPE,
                'Accept': MIMETYPE
            },
        )

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['INVALID_TOKEN_MSG']

    def test_get_schedule_list_should_with_no_token_fails(
            self, client, schedule_list):
        """Should fail when invalid token is provided

            Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            schedule_list: list of created schedule
        """
        assigneeId = schedule_list[0].assignee_id

        response = client.get(
            f'{API_BASE_URL_V1}/schedules?assigneeId={assigneeId}',
            headers={
                'Authorization': "",
                'Content-Type': MIMETYPE,
                'Accept': MIMETYPE
            },
        )
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_get_all_schedule_succeeds(self, client, auth_header):
        """Should return list of schedules when a valid assigneeId is passed

          Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            schedule_list: list of created schedule
        """

        response = client.get(
            f'{API_BASE_URL_V1}/schedules?', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data']

        assert response.status_code == 200
        assert type(response_data) == list
        assert 'assignee' in response_data[0]
        assert 'dueDate' in response_data[0]
        assert 'status' in response_data[0]
        assert 'createdBy' in response_data[0]
        assert 'workOrder' in response_data[0]
        assert 'maintenanceCategory' in response_data[0]['workOrder']
        assert response_json['status'] == 'success'
        assert response_json['message'] == \
               SUCCESS_MESSAGES['fetched'].format('Schedules')

    def test_get_all_schedule_without_pagination_succeeds(
            self, client, auth_header):
        """Should return list of schedules when a valid assigneeId is passed with null meta

          Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            schedule_list: list of created schedule
        """

        response = client.get(
            f'{API_BASE_URL_V1}/schedules?pagination=false',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data']
        assert response.status_code == 200
        assert type(response_data) == list
        assert 'maintenanceCategory' in response_data[0]['workOrder']
        assert response_json['status'] == 'success'
        assert response_json['message'] == \
               SUCCESS_MESSAGES['fetched'].format('Schedules')
        assert response_json['meta'] is None

    def test_get_schedule_for_an_assigner_succeeds(self, client, auth_header,
                                                   schedule_list):
        """Should return list of schedules when a valid assigner is passed
             Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            schedule_list: list of created schedule
        """
        assigner = schedule_list[0].created_by
        response = client.get(
            f'{API_BASE_URL_V1}/schedules?created_by={assigner}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data']
        assert response.status_code == 200
        assert type(response_data) == list
        assert 'assignee' in response_data[0]
        assert response_data[0]['createdBy'] == assigner
        assert response_data[0]['status'] == 'pending'
        assert "createdBy" in response_data[0]


class TestGetSingleWorkOrderEndpoint:
    """Class for work order GET endpoint."""

    def test_get_schedule_by_id_succeeds(self, init_db, client, auth_header,
                                         new_schedule):
        """Tests when request is valid.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_schedule: fixture that contains the schedule

        """
        new_schedule.save()
        response = client.get(
            f'{API_BASE_URL_V1}/schedules/{new_schedule.id}',
            headers=auth_header)
        assert response.status_code == 200
        response_data = json.loads(response.data.decode(CHARSET))
        data = response_data.get('data')
        assert response_data['status'] == 'success'
        assert response_data['message'] == SUCCESS_MESSAGES[
            'successfully_fetched'].format('Schedule')
        assert data.get('status') == new_schedule.status.value

    def test_get_with_invalid_schedule_by_id_fails(self, init_db, client,
                                                   auth_header):
        """Tests when id is invalid.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token

        """
        response = client.get(
            f'{API_BASE_URL_V1}/schedules/fake-id', headers=auth_header)
        response_data = json.loads(response.data.decode(CHARSET))
        assert response_data.get('status') == 'error'
        assert response_data.get('message') == 'Schedule not found'
        assert response.status_code == 404

    def test_get_existing_schedule_with_no_token_fails(
            self, init_db, client, auth_header, new_schedule):
        """Tests when token is not provided.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_schedule: fixture that contain schedule


        """
        response = client.get(f'{API_BASE_URL_V1}/schedules/{new_schedule.id}')
        response_data = json.loads(response.data.decode(CHARSET))
        assert response_data.get('status') == 'error'
        assert response_data.get('message') == jwt_errors['NO_TOKEN_MSG']
        assert response.status_code == 401

    def test_get_existing_schedule_with_invalid_token_fails(
            self, client, init_db, new_schedule):
        """
        Should fail when invalid token is provided

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            new_schedule: fixture that contain schedule

        """

        new_schedule.save()
        response = client.get(
            f'{API_BASE_URL_V1}/schedules/{new_schedule.id}',
            headers={
                'Authorization': "Bearer XXXX",
                'Content-Type': MIMETYPE,
                'Accept': MIMETYPE
            })
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['INVALID_TOKEN_MSG']

    def test_get_schedule_details_when_eager_loaded_with_comment_with_valid_schedule_id_succeeds(
            self, client, auth_header, new_schedule, new_schedule_comment):
        """Should return a request when a valid request id is Passed in.
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            new_schedule: fixture for a schedule
            new_schedule_comment: fixture for a comment
        """

        schedule = new_schedule.save()
        new_schedule_comment.parent_id = schedule.id
        comment = new_schedule_comment.save()

        response = client.get(
            f'{API_BASE_URL_V1}/schedules/{schedule.id}?include=comments',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        response_data = response_json['data']

        assert response.status_code == 200
        assert response_data['id'] == schedule.id
        assert response_data['status'] == new_schedule.status.value
        assert response_data['comments'][0]['id'] == comment.id
        assert response_data['comments'][0]['parentId'] == schedule.id
        assert response_json['status'] == 'success'
        assert response_json['message'] == \
            SUCCESS_MESSAGES['successfully_fetched'].format('Schedule')

    def test_get_schedule_details_when_invalid_query_param_is_provided_fails(
            self, client, auth_header, new_schedule):
        """Should return a request when a valid request id is Passed in.
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            new_schedule: fixture for a schedule
        """

        schedule = new_schedule.save()
        response = client.get(
            f'{API_BASE_URL_V1}/schedules/{schedule.id}?include=comment',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_include_key'].format('comments')
