"""Test for the hot desk endpoint"""
# Standard Library
import json

# Local import
from api.utilities.messages.error_messages import jwt_errors
from api.utilities.messages.error_messages import serialization_errors
from api.utilities.constants import (
    CHARSET, HOT_DESK_TRUE_VALUE, HOT_DESK_QUERY_PARAMS, HOT_DESK_STATUS_VALUE)

# app config
from api.utilities.messages.error_messages.database_errors import error_dict
from api.utilities.messages.success_messages import SUCCESS_MESSAGES

from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1
hot_desk_cancel_param_url = BASE_URL + '/hot-desks?cancel={}'
hot_desk_request_by_user_url = BASE_URL + '/hot-desks?requester={}'
hot_desk_responder_param_url = BASE_URL + '/hot-desks?responder={}&status={}'
hot_desk_escalation_param_url = BASE_URL+'/hot-desks?escalation={}'
hot_desk_params_url = BASE_URL + '/hot-desks?{}'
hot_desk_url = BASE_URL + '/hot-desks?'
hot_desk_no_status_param_url = BASE_URL + '/hot-desks?responder={}'

value = 'true'


class TestResourceEndPoint:
    def test_hot_desk_requests_by_a_user_with_no_token_fails(self, client):
        """Tests that when no token or invalid token is passed, error is returned
        Args:
            client (FlaskClient): fixture to get flask test client

        """
        response = client.get(
            hot_desk_request_by_user_url.format('requester_id'))
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_hot_desk_request_by_a_user_not_found_fails(
        self, client, auth_header, new_hot_desk_request):
        """Tests that hot desk requests by a user is successfully fetched
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            new_hot_desk_request: a valid Hot_Desk_Request object
        """
        new_hot_desk_request.save()

        response = client.get(
            hot_desk_request_by_user_url.format('userNotFound'),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == error_dict['non_existing'].format(
            'User')

    def test_hot_desk_request_by_a_user_succeeds(
        self, client, auth_header, new_hot_desk_request, new_user):
        """Tests that hot desk requests by a user is successfully fetched
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            new_hot_desk_request: a valid Hot_Desk_Request object
            new_user: a valid User object in the database
        """
        new_hot_desk_request.save()

        response = client.get(
            hot_desk_request_by_user_url.format(new_user.token_id),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['data']['HotDeskRequestByUser']['hotDesks'][0][
                   'hotDeskRefNo'] == new_hot_desk_request.hot_desk_ref_no
        assert response_json['data']['HotDeskRequestByUser']['requester'][
                   'tokenId'] == new_user.token_id

    def test_hot_desk_cancel_reasons_counts_with_invalid_param_value_fails(
        self, client, auth_header):
        """Tests that hot desk cancel request fails if an invalid is provided
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
        """

        response = client.get(
            hot_desk_cancel_param_url.format('i'), headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors['invalid_request_param'].format( \
            'param value', ', '.join(HOT_DESK_TRUE_VALUE))

    def test_hot_desk_cancel_reasons_counts_with_invalid_param_fails(
        self, client, auth_header):
        """Tests that hot desk cancel request fails if an invalid is provided
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
        """

        response = client.get(
            hot_desk_params_url.format('approved'),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors['invalid_request_param'].format( \
            'query param', ', '.join(HOT_DESK_QUERY_PARAMS))

    def test_hot_desk_cancel_reasons_counts_with_no_param_key_fails(
        self, client, auth_header):
        """Tests that hot desk cancel request fails if an invalid is provided
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
        """

        response = client.get(hot_desk_url, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors['invalid_request_param'].format( \
            'query param', ' or '.join(HOT_DESK_QUERY_PARAMS))

    def test_hot_desk_cancel_reasons_counts_with_valid_param_key_succeeds(
        self, init_db, client, auth_header):
        """Tests that hot desk cancellation count requests is successfully fetched
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
        """

        response = client.get(
            hot_desk_cancel_param_url.format(value), headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'Success'
        assert response_json['message'] == SUCCESS_MESSAGES['fetched'].format(
            'Hot desk cancellation report')

    def test_get_approved_hot_desk_requests_by_a_responder_succeeds(
        self, client, auth_header, new_hot_desk_response, new_user):
        """ Tests approved hot desk requests by a responder is successfully fetched
            Args:
                client (func): Flask test client
                auth_header (func): Fixture for auth token
                new_hot_desk_response: Fixture to create a hot desk response
                new_user: Fixture to create a new user
        """
        new_hot_desk_response.assignee_id = new_user.token_id
        new_hot_desk_response.status = 'approved'
        new_hot_desk_response.save()
        response = client.get(
            hot_desk_responder_param_url.format(new_user.token_id, 'approved'),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['data']['responder'][
                   'tokenId'] == new_user.token_id
        assert response_json['data']['approvedHotDesks'][0][
                   'status'] == 'approved'
        assert isinstance(response_json['data']['responder'], dict)
        assert isinstance(response_json['data']['approvedHotDesks'], list)

    def test_get_rejected_hot_desk_requests_by_a_responder_succeeds(
        self, client, auth_header, new_hot_desk_response, new_user):
        """ Tests rejected hot desk requests by a responder is successfully fetched
            Args:
                client (func): Flask test client
                auth_header (func): Fixture for auth token
                new_hot_desk_response: Fixture to create a hot desk response
                new_user: Fixture to create a new user
        """
        new_hot_desk_response.assignee_id = new_user.token_id
        new_hot_desk_response.status = 'rejected'
        new_hot_desk_response.save()
        response = client.get(
            hot_desk_responder_param_url.format(new_user.token_id, 'rejected'),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['data']['responder'][
                   'tokenId'] == new_user.token_id
        assert response_json['data']['rejectedHotDesks'][0][
                   'status'] == 'rejected'
        assert isinstance(response_json['data']['responder'], dict)
        assert isinstance(response_json['data']['rejectedHotDesks'], list)

    def test_get_missed_hot_desk_requests_by_a_responder_succeeds(
        self, client, auth_header, new_hot_desk_response, new_user):
        """ Tests missed hot desk requests by a responder is successfully fetched
            Args:
                client (func): Flask test client
                auth_header (func): Fixture for auth token
                new_hot_desk_response: Fixture to create a hot desk response
                new_user: Fixture to create a new user
        """
        new_hot_desk_response.assignee_id = new_user.token_id
        new_hot_desk_response.status = 'pending'
        new_hot_desk_response.is_escalated = True
        new_hot_desk_response.save()
        response = client.get(
            hot_desk_responder_param_url.format(new_user.token_id, 'missed'),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['data']['responder'][
                   'tokenId'] == new_user.token_id
        assert response_json['data']['missedHotDesks'][0][
                   'status'] == 'pending'
        assert isinstance(response_json['data']['responder'], dict)
        assert isinstance(response_json['data']['missedHotDesks'], list)

    def test_get_hot_desks_requests_by_a_responder_with_invalid_status_fails(
        self, init_db, client, auth_header, new_user):
        """ Tests get hot desk requests by a responder with invalid status fails
            Args:
                client (func): Flask test client
                auth_header (func): Fixture for auth token
                new_user: Fixture to create a new user
        """
        new_user.save()
        response = client.get(
            hot_desk_responder_param_url.format(new_user.token_id, 'invalid'),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors['invalid_request_param'].format( \
            'status query param value', ', '.join(HOT_DESK_STATUS_VALUE))

    def test_get_hot_desks_requests_by_a_responder_without_status_param_fails(
        self, init_db, client, auth_header, new_user):
        """ Tests get hot desk requests by a responder with invalid status fails
            Args:
                client (func): Flask test client
                auth_header (func): Fixture for auth token
                new_user: Fixture to create a new user
        """
        new_user.save()
        response = client.get(
            hot_desk_no_status_param_url.format(new_user.token_id),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'required_param_key'].format('status')

    def test_hot_desk_escalation_count_with_valid_param_key_succeeds(self, init_db,
                                                                     client, auth_header):
        """Tests that hot desk escalation count requests is successfully fetched
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
        """

        response = client.get(
            hot_desk_escalation_param_url.format(value), headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'Success'
        assert response_json['message'] == SUCCESS_MESSAGES['fetched'].format(
            'Hot desk escalation report')

    def test_hot_desk_escalation_count_with_invalid_param_value_fails(self, client, auth_header):
        """Tests that hot desk escalation request fails if an invalid is provided
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
        """

        response = client.get(
            hot_desk_escalation_param_url.format('invalid'), headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors['invalid_request_param'].format( \
            'param value', ', '.join(HOT_DESK_TRUE_VALUE))
