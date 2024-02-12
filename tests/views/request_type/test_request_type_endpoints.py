"""Module for asset resource endpoints."""
import pytest

# Flask
from flask import json

# Constant
from api.utilities.constants import CHARSET, VALID_TIME_UNITS

# Utilities
from api.utilities.messages.error_messages import serialization_errors, database_errors, jwt_errors
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.enums import RequestStatusEnum

# Mock
from tests.mocks.request_type import (
    VALID_REQUEST_TYPE_DATA, SUCCESS_RESPONSE,
    REQUEST_TYPE_WITH_MISSING_FIELDS,
    REQUEST_TYPE_WITH_MISSING_RESOLUTION_TIME, VALID_REQUEST_TYPE_UPDATE_DATA)

# Models
from api.models.request_type import RequestType
from api.models.request import Request

# Tasks
from faker import Faker

# app config
from config import AppConfig

fake = Faker()

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestRequestTypeEndpoint:
    """Class for request_type endpoints."""

    def test_get_request_type_by_id_succeeds(self, init_db, client,
                                             auth_header, new_request_type):
        """Tests when request is valid.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_request_type: fixture that contains the request type

        Returns:
            None
        """
        new_request_type.save()
        response = client.get(
            f'{API_BASE_URL_V1}/request-types/{new_request_type.id}',
            headers=auth_header)

        response_data = json.loads(response.data.decode(CHARSET))

        data = response_data.get('data')
        assert response_data['status'] == 'success'
        assert response_data['message'] == SUCCESS_MESSAGES[
            'successfully_fetched'].format('Request type')
        assert data.get('title') == new_request_type.title
        assert data.get('resolutionTime') == new_request_type.resolution_time
        assert data.get('responseTime') == new_request_type.response_time
        assert data.get('centerId') == new_request_type.center_id
        assert "requestsCount" in data
        assert response.status_code == 200

    def test_get_with_invalid_request_type_by_id_fails(
            self, init_db, client, auth_header, new_request_type):
        """Tests when id is invalid.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_request_type: fixture that contains the request type
        Returns:
            None
        """
        response = client.get(
            f'{API_BASE_URL_V1}/request-types/invalid_id', headers=auth_header)
        response_data = json.loads(response.data.decode(CHARSET))
        assert response_data.get('status') == 'error'
        assert response_data.get('message') == 'Request type not found'
        assert response.status_code == 404

    def test_get_request_type_with_no_token_fails(
            self, init_db, client, auth_header, new_request_type):
        """Tests when token is not provided.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_request_type (RequestType): fixture that uses the request_type

        Returns:
            None
        """
        response = client.get(
            f'{API_BASE_URL_V1}/request-types/{new_request_type.id}')
        response_data = json.loads(response.data.decode(CHARSET))
        assert response_data.get('status') == 'error'
        assert response_data.get('message') == jwt_errors['NO_TOKEN_MSG']
        assert response.status_code == 401

    def test_create_request_type_with_valid_data_succeed(  # pylint: disable=C0103
            self,
            client,
            init_db,  # pylint: disable=W0613
            auth_header,
            new_user):
        """
        Tests create request types with valid data.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_user (dict): fixture to create a new user

        """
        new_user.save()
        VALID_REQUEST_TYPE_DATA['assigneeId'] = new_user.token_id
        VALID_REQUEST_TYPE_DATA['centerId'] = new_user.center_id
        data = json.dumps(VALID_REQUEST_TYPE_DATA)
        response = client.post(
            f'{API_BASE_URL_V1}/request-types', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 201
        assert response_json['status'] == SUCCESS_RESPONSE['status']
        assert response_json['message'] == SUCCESS_RESPONSE['message']
        assert response_json['data']['assignee']['name'] == new_user.name
        assert response_json['data']['title'] == SUCCESS_RESPONSE['data'][
            'title']
        assert response_json['data']['resolutionTime'] == SUCCESS_RESPONSE[
            'data']['resolutionTime']

    def test_create_request_type_with_missing_field_succeeds(  # pylint: disable=C0103
            self,
            client,
            init_db,  # pylint: disable=W0613
            auth_header,
            new_user):
        """
        Tests create request types with valid data

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_user (dict): fixture to create a new user

        """
        new_user.save()
        REQUEST_TYPE_WITH_MISSING_FIELDS['assigneeId'] = new_user.token_id
        REQUEST_TYPE_WITH_MISSING_FIELDS['centerId'] = new_user.center_id
        data = json.dumps(REQUEST_TYPE_WITH_MISSING_FIELDS)
        response = client.post(
            f'{API_BASE_URL_V1}/request-types', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 201
        assert response_json['status'] == SUCCESS_RESPONSE['status']
        assert response_json['message'] == SUCCESS_RESPONSE['message']
        assert response_json['data']['assignee']['name'] == new_user.name
        assert response_json['data'][
            'title'] == REQUEST_TYPE_WITH_MISSING_FIELDS['title']
        assert response_json['data']['resolutionTime']['hours'] == 0
        assert response_json['data']['responseTime']['days'] == 0

    def test_create_request_type_with_invalid_resolution_time_type_fails(  # pylint: disable=C0103
            self,
            client,
            init_db,  # pylint: disable=W0613
            auth_header,
            new_user):
        """
        Tests create request types with valid data.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_user (dict): fixture to create a new user

        """
        joined_time_types = ' or '.join(VALID_TIME_UNITS)

        new_user.save()
        request_type_with_invalid_time_type = dict(**VALID_REQUEST_TYPE_DATA)

        request_type_with_invalid_time_type['assigneeId'] = new_user.token_id
        request_type_with_invalid_time_type['centerId'] = new_user.center_id

        request_type_with_invalid_time_type['responseTime'] = "hello"
        data = json.dumps(request_type_with_invalid_time_type)

        response = client.post(
            f'{API_BASE_URL_V1}/request-types', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == \
               serialization_errors['invalid_request_type_time'].format('responseTime', joined_time_types)

    def test_create_request_type_with_missing_field_in_response_time_fails(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            new_user):
        """
        Tests create request types with valid data

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_user (dict): fixture to create a new user

        """
        new_user.save()
        request_type_with_missing_fields = dict(**VALID_REQUEST_TYPE_DATA)
        request_type_with_missing_fields['assigneeId'] = new_user.token_id
        request_type_with_missing_fields['centerId'] = new_user.center_id
        request_type_with_missing_fields['responseTime']['days'] = 10
        request_type_with_missing_fields['closureTime']['days'] = 10
        del request_type_with_missing_fields['resolutionTime']
        data = json.dumps(request_type_with_missing_fields)
        response = client.post(
            f'{API_BASE_URL_V1}/request-types', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400

        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'missing_fields'].format('resolutionTime')

    def test_create_request_type_with_missing_field_in_resolution_time_fails(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            new_user):
        """
        Tests create request types with valid data

        
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_user (dict): fixture to create a new user

        """

        new_user.save()
        REQUEST_TYPE_WITH_MISSING_FIELDS['title'] = fake.sentence()
        REQUEST_TYPE_WITH_MISSING_FIELDS['assigneeId'] = new_user.token_id
        REQUEST_TYPE_WITH_MISSING_FIELDS['centerId'] = new_user.center_id
        REQUEST_TYPE_WITH_MISSING_FIELDS['resolutionTime']['hours'] = 10
        del REQUEST_TYPE_WITH_MISSING_FIELDS['responseTime']
        data = json.dumps(REQUEST_TYPE_WITH_MISSING_FIELDS)
        response = client.post(
            f'{API_BASE_URL_V1}/request-types', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'missing_fields'].format('responseTime')

    def test_create_request_type_with_hours_greater_than_24_fails(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            new_user):
        """
        Tests create request types with valid data

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_user (dict): fixture to create a new user

        """
        new_user.save()
        valid_request_type = dict(**VALID_REQUEST_TYPE_DATA)
        valid_request_type['assigneeId'] = new_user.token_id
        valid_request_type['centerId'] = new_user.center_id

        # makes the hour > 24
        valid_request_type['resolutionTime']['hours'] = 25

        request_type_with_hour_gt_24 = valid_request_type
        request_type_with_hour_gt_24['responseTime']['days'] = 2
        data = json.dumps(valid_request_type)
        response = client.post(
            f'{API_BASE_URL_V1}/request-types', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_date_input'].format('hours', '24')

    def test_post_with_days_less_than_zero_fails(
            self, init_db, client, auth_header, new_request_type):
        """Should fail when resolution_time['days'] < 0

        Args:
            init_db(SQLAlchemy): Fixture to initialize the test database actions
            new_request_type (object): Fixture to create a new request type
        """
        request_type = new_request_type.save()
        request_type_invalid_days = dict(**VALID_REQUEST_TYPE_DATA)
        request_type_invalid_days['assigneeId'] = request_type.assignee_id
        request_type_invalid_days['centerId'] = request_type.assignee_id
        request_type_invalid_days['resolutionTime']['days'] = -100
        data = json.dumps(request_type_invalid_days)
        response = client.post(
            f'{API_BASE_URL_V1}/request-types', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_day_in_date_input'].format('resolutionTime', 'days', '0')

    def test_post_with_sum_of_time_values_lte_zero_fails(
            self, init_db, client, auth_header, new_request_type):
        """Should fail when resolution_time['days'] < 0

        Args:
            init_db(SQLAlchemy): Fixture to initialize the test database actions
            new_request_type (object): Fixture to create a new request type
        """
        request_type = new_request_type.save()
        request_type_invalid_days = dict(**VALID_REQUEST_TYPE_DATA)
        request_type_invalid_days['assigneeId'] = request_type.assignee_id
        request_type_invalid_days['centerId'] = request_type.assignee_id
        request_type_invalid_days['resolutionTime'] = {
            "days": 0,
            "minutes": 0,
            "hours": 0
        }
        data = json.dumps(request_type_invalid_days)
        response = client.post(
            f'{API_BASE_URL_V1}/request-types', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        comma_seperated_time_types = ', '.join(VALID_TIME_UNITS)
        assert response_json['status'] == 'error'
        assert response_json[
            'message'] == serialization_errors['invalid_date_sum'].format(
                'resolutionTime', comma_seperated_time_types, '0')

    def test_assign_request_type_to_user_in_another_center_fails(  # pylint: disable=C0103
            self,
            client,
            init_db,  # pylint: disable=W0613
            auth_header,
            new_center,
            new_user):
        """
        Tests create request types with valid data

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_user (dict): fixture to create a new user
            new_center (dict): fixture to create a new center

        """
        new_user.save()
        new_center.save()
        valid_request_type = dict(**VALID_REQUEST_TYPE_DATA)
        valid_request_type['assigneeId'] = new_user.token_id
        valid_request_type['centerId'] = new_center.id
        valid_request_type['resolutionTime'] = {"hours": 20, "days": 10}
        valid_request_type['responseTime']['days'] = 2
        data = json.dumps(valid_request_type)
        response = client.post(
            f'{API_BASE_URL_V1}/request-types', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'user_not_found'].format('User')

    #pylint: disable=W0613

    def test_create_request_type_with_existing_data_fails(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            new_user,
            new_request_type_two):
        """
        Tests create request types with valid data

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        
            new_user (dict): fixture to create a new_user

        """
        sample_title = "Maintenance 101"
        new_request_type_two.title = sample_title
        new_request_type_two.save()
        request_type_with_existing_title = dict(**VALID_REQUEST_TYPE_DATA)

        request_type_with_existing_title['assigneeId'] = new_user.token_id
        request_type_with_existing_title['centerId'] = new_user.center_id
        request_type_with_existing_title['title'] = sample_title
        request_type_with_existing_title['resolutionTime'] = {"days": 10}
        request_type_with_existing_title['responseTime'] = {"days": 10}
        request_type_with_existing_title['closureTime'] = {"days": 10}
        data = json.dumps(request_type_with_existing_title)
        response = client.post(
            f'{API_BASE_URL_V1}/request-types', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'exists'].format(sample_title)

    def test_update_request_type_succeeds(self, client, auth_header,
                                          new_request_type):
        """
        Tests update request types with valid data and id

        Args:
            client (FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get token
            new_request_type2 (dict): fixture to create a new_request_type
        """
        new_request_type.save()
        request_type_id = new_request_type.id
        valid_request_type_data = dict(**VALID_REQUEST_TYPE_UPDATE_DATA)
        valid_request_type_data['assigneeId'] = new_request_type.assignee_id
        valid_request_type_data['centerId'] = new_request_type.center_id
        valid_request_type_data['resolutionTime'] = {
            "days": 10,
            "hours": 4,
            "minutes": 1
        }
        data = json.dumps(valid_request_type_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/request-types/{request_type_id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response_json['message'] == SUCCESS_MESSAGES['edited'].format(
            'Request type')
        assert response.status_code == 200
        assert response_json['status'] == SUCCESS_RESPONSE['status']

    def test_update_request_type_with_different_assignee_succeeds(
            self, client, auth_header, duplicate_request_type, second_user):
        """Should update assignee id to the id of the second user
        
        Args:
            client (FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get token
            duplicate_request_type (dict): fixture to create a new_request_type
            second_user(dict): fixture to create another user
        """
        duplicate_request_type.save()
        second_user.center_id = duplicate_request_type.center_id
        second_user.save()
        request_type_id = duplicate_request_type.id
        valid_request_type_data = dict(**VALID_REQUEST_TYPE_UPDATE_DATA)
        valid_request_type_data['assigneeId'] = second_user.token_id
        valid_request_type_data['centerId'] = duplicate_request_type.center_id
        valid_request_type_data['resolutionTime'] = {
            "days": 10,
            "hours": 4,
            "minutes": 1
        }
        data = json.dumps(valid_request_type_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/request-types/{request_type_id}',
            headers=auth_header,
            data=data)
        assert response.json['message'] == SUCCESS_MESSAGES['edited'].format(
            'Request type')
        assert response.status_code == 200
        assert response.json['data']['assignee'][
            'tokenId'] == second_user.token_id
        assert response.json['status'] == SUCCESS_RESPONSE['status']

    def test_update_request_type_assignee_updates_responder_id_of_open_requests_succeeds(
            self, client, auth_header, duplicate_request_type, second_user,
            new_request):
        """Should update the responder id to new assignee if request is open
        
        Args:
            client (FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get token
            duplicate_request_type (dict): fixture to create a new_request_type
            second_user(dict): fixture to create another user
            new_request(dict): fixture to create a new request

        """
        duplicate_request_type.save()
        new_request.request_type_id = duplicate_request_type.id
        new_request.status = RequestStatusEnum.open
        new_request.save()
        second_user.center_id = duplicate_request_type.center_id
        second_user.save()
        request_type_id = duplicate_request_type.id
        valid_request_type_data = dict(**VALID_REQUEST_TYPE_UPDATE_DATA)
        valid_request_type_data['assigneeId'] = second_user.token_id
        valid_request_type_data['centerId'] = duplicate_request_type.center_id
        valid_request_type_data['resolutionTime'] = {
            "days": 10,
            "hours": 4,
            "minutes": 1
        }
        data = json.dumps(valid_request_type_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/request-types/{request_type_id}',
            headers=auth_header,
            data=data)
        assert response.json['message'] == SUCCESS_MESSAGES['edited'].format(
            'Request type')
        assert response.status_code == 200
        assert response.json['data']['assignee'][
            'tokenId'] == second_user.token_id
        assert response.json['status'] == SUCCESS_RESPONSE['status']
        assert new_request.responder_id == second_user.token_id

    def test_update_request_type_assignee_updates_responder_id_of_in_progress_requests_succeeds(
            self, client, auth_header, duplicate_request_type, second_user,
            new_request):
        """Should update the responder id to new assignee if request is in progress
        
        Args:
            client (FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get token
            duplicate_request_type (dict): fixture to create a new_request_type
            second_user(dict): fixture to create another user
            new_request(dict): fixture to create a new request

        """
        duplicate_request_type.save()
        new_request.request_type_id = duplicate_request_type.id
        new_request.status = RequestStatusEnum.in_progress
        new_request.save()
        second_user.center_id = duplicate_request_type.center_id
        second_user.save()
        request_type_id = duplicate_request_type.id
        valid_request_type_data = dict(**VALID_REQUEST_TYPE_UPDATE_DATA)
        valid_request_type_data['assigneeId'] = second_user.token_id
        valid_request_type_data['centerId'] = duplicate_request_type.center_id
        valid_request_type_data['resolutionTime'] = {
            "days": 10,
            "hours": 4,
            "minutes": 1
        }
        data = json.dumps(valid_request_type_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/request-types/{request_type_id}',
            headers=auth_header,
            data=data)
        assert response.json['message'] == SUCCESS_MESSAGES['edited'].format(
            'Request type')
        assert response.status_code == 200
        assert response.json['data']['assignee'][
            'tokenId'] == second_user.token_id
        assert response.json['status'] == SUCCESS_RESPONSE['status']
        assert new_request.responder_id == second_user.token_id

    def test_update_request_type_assignee_cannot_update_responder_id_of_closed_requests_succeeds(
            self, client, auth_header, duplicate_request_type, second_user,
            new_request):
        """Should not update the responder id to new assignee if request is closed
        
        Args:
            client (FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get token
            duplicate_request_type (dict): fixture to create a new_request_type
            second_user(dict): fixture to create another user
            new_request(dict): fixture to create a new request

        """
        duplicate_request_type.save()
        new_request.request_type_id = duplicate_request_type.id
        new_request.status = RequestStatusEnum.closed
        new_request.save()
        second_user.center_id = duplicate_request_type.center_id
        second_user.save()
        request_type_id = duplicate_request_type.id
        valid_request_type_data = dict(**VALID_REQUEST_TYPE_UPDATE_DATA)
        valid_request_type_data['assigneeId'] = second_user.token_id
        valid_request_type_data['centerId'] = duplicate_request_type.center_id
        valid_request_type_data['resolutionTime'] = {
            "days": 10,
            "hours": 4,
            "minutes": 1
        }
        data = json.dumps(valid_request_type_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/request-types/{request_type_id}',
            headers=auth_header,
            data=data)
        assert response.json['message'] == SUCCESS_MESSAGES['edited'].format(
            'Request type')
        assert response.status_code == 200
        assert response.json['data']['assignee'][
            'tokenId'] == second_user.token_id
        assert response.json['status'] == SUCCESS_RESPONSE['status']
        assert new_request.responder_id != second_user.token_id

    def test_update_request_type_assignee_cannot_update_responder_id_of_completed_requests_succeeds(
            self, client, auth_header, duplicate_request_type, second_user,
            new_request):
        """Should not update the responder id to new assignee if request is completed
        
        Args:
            client (FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get token
            duplicate_request_type (dict): fixture to create a new_request_type
            second_user(dict): fixture to create another user
            new_request(dict): fixture to create a new request

        """
        duplicate_request_type.save()
        new_request.request_type_id = duplicate_request_type.id
        new_request.status = RequestStatusEnum.completed
        new_request.save()
        second_user.center_id = duplicate_request_type.center_id
        second_user.save()
        request_type_id = duplicate_request_type.id
        valid_request_type_data = dict(**VALID_REQUEST_TYPE_UPDATE_DATA)
        valid_request_type_data['assigneeId'] = second_user.token_id
        valid_request_type_data['centerId'] = duplicate_request_type.center_id
        valid_request_type_data['resolutionTime'] = {
            "days": 10,
            "hours": 4,
            "minutes": 1
        }
        data = json.dumps(valid_request_type_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/request-types/{request_type_id}',
            headers=auth_header,
            data=data)
        assert response.json['message'] == SUCCESS_MESSAGES['edited'].format(
            'Request type')
        assert response.status_code == 200
        assert response.json['data']['assignee'][
            'tokenId'] == second_user.token_id
        assert response.json['status'] == SUCCESS_RESPONSE['status']
        assert new_request.responder_id != second_user.token_id

    def test_update_request_type_with_invalid_title_fails(
            self, client, auth_header, new_request_type):
        """
        Tests update request types with invalid title format fails 

        Args:
            client (FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get token
            new_request_type (dict): fixture to create a new_request_type
        """
        new_request_type.save()
        request_type_id = new_request_type.id
        valid_request_type_data = {"title": "@#(#)!)"}
        data = json.dumps(valid_request_type_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/request-types/{request_type_id}',
            headers=auth_header,
            data=data)
        assert response.json['errors']['title'][0] == serialization_errors[
            'string_characters']
        assert response.status_code == 400
        assert response.json['status'] == 'error'

    def test_update_request_type_with_valid_title_succeeds(
            self, client, auth_header, new_request_type):
        """
        Tests update request types with valid title format return 200 

        Args:
            client (FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get token
            new_request_type (dict): fixture to create a new_request_type
        """
        new_request_type.save()
        request_type_id = new_request_type.id
        title = "This is my new title"
        valid_request_type_data = dict(**VALID_REQUEST_TYPE_UPDATE_DATA)
        valid_request_type_data['centerId'] = new_request_type.center_id
        valid_request_type_data['assigneeId'] = new_request_type.assignee_id
        valid_request_type_data['title'] = title
        data = json.dumps(valid_request_type_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/request-types/{request_type_id}',
            headers=auth_header,
            data=data)
        assert response.json['message'] == SUCCESS_MESSAGES['edited'].format(
            'Request type')
        assert response.status_code == 200
        assert response.json['status'] == SUCCESS_RESPONSE['status']
        assert response.json['data']['title'] == title

    def test_update_non_existing_request_type_fails(self, client, auth_header):
        """
        Tests update request types with invalid id
        Args:
            client (FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get token
            new_request_type2 (dict): fixture to create a new_request_type
        """

        response = client.patch(
            f'{API_BASE_URL_V1}/request-types/12345jfk', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'Request type not found'

    def test_update_request_type_endpoint_without_authentication_fails(
            self, client):
        """
        Tests update request types with valid data and id

        Args:
            client (FlaskClient): fixture to get flask test client
        """

        response = client.patch(
            f'{API_BASE_URL_V1}/request-types/12345jfk', headers={})
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_delete_request_type_succeeds(self, client, auth_header, init_db,
                                          new_request_type):
        """
        Tests delete request type succeeds

         Args:
            client (object): Fixture to get flask test client
            auth_header (dict): Fixture to get token
            init_db (object): Used to create the database structure using the models
            new_request_type (object): Fixture to create a new request type

        Returns:
            None
        """
        request_type = new_request_type.save()

        response = client.delete(
            f'{API_BASE_URL_V1}/request-types/{request_type.id}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['deleted'].format(
            'Request Type')

    def test_delete_request_type_fails_when_deleting_already_deleted_request_type(
            self, client, init_db, auth_header, new_request_type):
        """
        Test delete request type fails when deleting an already deleted request type

        Args:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
            init_db (object): Used to create the database structure using the models
            new_request_type (object): Fixture to create a new request type

        Returns:
            None
        """
        request_type = new_request_type.save()

        response = client.delete(
            f'{API_BASE_URL_V1}/request-types/{request_type.id}',
            headers=auth_header)
        response = client.delete(
            f'{API_BASE_URL_V1}/request-types/{request_type.id}',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'not_found'].format('Request type')

    def test_delete_request_type_fails_when_deleting_request_type_with_existing_request(
            self, client, init_db, auth_header, create_new_request):
        """
        Test delete request type fails when deleting a request type with requests
        Args:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
            init_db (object): Used to create the database structure using the models
            new_request_type (object): Fixture to create a new request type
        Returns:
            None
        """

        request = create_new_request.save()

        response = client.delete(
            f'{API_BASE_URL_V1}/request-types/{request.request_type_id}',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 403
        assert response_json['status'] == 'error'
        assert response_json[
            'message'] == 'Delete failed. RequestType has Request(s) not deleted.'

    def test_delete_request_type_fails_for_non_existing_request_type(
            self, client, auth_header):
        """
        Test delete request type fails when deleting a non existing request type
        in the Database

        Args:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token

        Returns:
            None
        """
        response = client.delete(
            f'{API_BASE_URL_V1}/request-types/-L2eethfh345',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404

        assert response_json['message'] == database_errors[
            'non_existing'].format('Request type')
        assert response_json['status'] == 'error'

    def test_delete_request_type_fails_for_no_token_supplied(self, client):
        """
        Test delete request type fails when no token is supplied

         Args:
            client (object): fixture to get flask test client

        Returns:
            None
        """
        response = client.delete(
            f'{API_BASE_URL_V1}/request-types/-LL9ab1iJLjgPNqHQ0Ha')

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401

        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']
        assert response_json['status'] == 'error'

    def test_delete_request_type_fails_for_request_type_id(
            self, client, auth_header):
        """
        Test delete request type fails when the space id contains invalid
        characters

         Args:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token

        Returns:
            None
        """

        response = client.delete(
            f'{API_BASE_URL_V1}/request-types/!#ffsfgs8L', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400

        assert response_json['message'] == serialization_errors['invalid_id']
        assert response_json['status'] == 'error'
