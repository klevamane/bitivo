"""Module for request resource endpoints."""

# Third party
from flask import json

# Mocks
from tests.mocks.requests import EXPECTED_REQUEST_RESPONSE_KEYS, SUMMARY_REQUEST

# Utilities
from api.utilities.constants import CHARSET
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import (serialization_errors,
                                                   jwt_errors)

# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestGetRequestEndpoint:
    """Class for Request resource GET endpoints."""

    def test_get_request_details_with_valid_request_id_succeeds(
            self, client, auth_header, new_request):
        """Should return a request when a valid request id is Passed in.
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            new_request: fixture for a request
        """

        request = new_request.save()

        response = client.get(
            f'{API_BASE_URL_V1}/requests/{request.id}', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        response_data = response_json['data']

        assert response.status_code == 200
        assert response_data['id'] == request.id
        assert response_data['centerId'] == request.center_id
        assert response_data['description'] == request.description
        assert response_data['subject'] == request.subject
        assert response_data['requester']['center']['id'] == response_data[
            'centerId']
        assert response_json['status'] == 'success'
        assert "serialNumber" in response_data
        assert "inProgressAt" in response_data
        assert "completedAt" in response_data
        assert "closedAt" in response_data
        assert "dueBy" in response_data
        assert "center" in response_data['requester']
        assert len(EXPECTED_REQUEST_RESPONSE_KEYS) == len(response_data.keys())
        assert set(EXPECTED_REQUEST_RESPONSE_KEYS) == set(response_data.keys())
        assert response_json['message'] == \
            SUCCESS_MESSAGES['fetched'].format('Request')

    def test_get_request_with_invalid_request_id_should_fail(
            self, client, auth_header):
        """Should return an error if an invalid request id is provided.
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """

        response = client.get(
            f'{API_BASE_URL_V1}/requests/-LM3$u$2p$^o&C@#',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors['invalid_id']

    def test_get_request_with_non_existent_id_fails(self, client, auth_header):
        """Should return a 404 status code when a non-existent id is provided.
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """

        response = client.get(
            f'{API_BASE_URL_V1}/requests/-LM3u2poCwe4jyQ0UbPN',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'not_found'].format('Request')

    def test_get_request_details_with_no_token_fails(self, client,
                                                     new_request):
        """Should return an error when no token is provided.
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            new_request: fixture for a request
        """
        request = new_request.save()
        response = client.get(f'{API_BASE_URL_V1}/requests/{request.id}')
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_get_request_details_when_eager_loaded_with_comment_with_valid_request_id_succeeds(
            self, client, auth_header, new_request, new_comment):
        """Should return a request when a valid request id is Passed in.
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            new_request: fixture for a request
            new_comment: fixture for a comment
        """

        request = new_request.save()
        comment = new_comment.save()
        response = client.get(
            f'{API_BASE_URL_V1}/requests/{request.id}?include=comments',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        response_data = response_json['data']

        assert response.status_code == 200
        assert response_data['id'] == request.id
        assert response_data['centerId'] == request.center_id
        assert response_data['description'] == request.description
        assert response_data['subject'] == request.subject
        assert response_data['comments'][0]['id'] == comment.id
        assert response_data['comments'][0]['parentId'] == request.id
        assert response_json['status'] == 'success'
        assert response_json['message'] == \
            SUCCESS_MESSAGES['fetched'].format('Request')

    def test_get_request_details_when_invalid_query_param_is_provided(
            self, client, auth_header, new_request):
        """Should return a request when a valid request id is Passed in.
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            new_request: fixture for a request
        """

        request = new_request.save()
        response = client.get(
            f'{API_BASE_URL_V1}/requests/{request.id}?include=comment',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_include_key'].format('comments')

    def test_get_user_requests_with_existing_user_succeeds(
            self, client, init_db, auth_header, new_request):
        """ Should succeed when correct data is given.
        Args:
            client (object): Fixture to get flask test client
            auth_header (dict): Fixture to get token
            init_db (object): Fixture for initializing test database
            new_request (Request): Fixture for getting test request data
        """
        new_request.save()
        response = client.get(
            f'{API_BASE_URL_V1}/people/{new_request.requester_id}/requests',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert "data" in response_json
        assert len(response_json["data"]) > 0
        assert response_json['meta']['currentPage'] != ''
        assert response_json['meta']['firstPage'] != ''
        assert response_json['meta']['previousPage'] == ''
        assert response_json['meta']['page'] == 1
        assert 'pagesCount' in response_json['meta']
        assert 'totalCount' in response_json['meta']

    def test_get_user_requests_with_non_existing_user_fails(
            self, client, init_db, auth_header):
        """ Should fail when incorrect data is given.
        Args:
            client (object): Fixture to get flask test client
            auth_header (dict): Fixture to get token
            init_db (object): Fixture for initializing test database
        """
        response = client.get(
            f'{API_BASE_URL_V1}/people/-QVBqszg8VD7ynVR/requests',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'not_found'].format('User')

    def test_get_summary_request_succeeds(self, client, auth_header,
                                          new_request):
        """
        Should succeed and return a summary  request when with a valid parameter in URL.
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            new_request: fixture for a request
        """

        new_request.save()
        response = client.get(
            f'{API_BASE_URL_V1}/requests?include=summary', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        response_data = response_json['data']

        assert response.status_code == 200
        data = response_data[-1]['requestSummary']
        mock_data = SUMMARY_REQUEST['requestSummary']
        assert data['totalRequests'] == mock_data['totalRequests']
        assert data['totalOpenRequests'] == mock_data['totalOpenRequests']
        assert data['totalInProgressRequests'] == mock_data[
            'totalInProgressRequests']
        assert data['totalClosedRequests'] == mock_data['totalClosedRequests']
        assert data['totalClosedRequests'] == mock_data['totalClosedRequests']
        assert data['totalCompletedRequests'] == mock_data[
            'totalCompletedRequests']
        assert response_json['status'] == 'success'
        assert response_json['message'] == \
            SUCCESS_MESSAGES['fetched'].format('Requests')

    def test_get_summary_request_when_invalid_query_param_is_provided_fails(
            self, client, auth_header, new_request):
        """
        Should fail when invalid query param is passed in URL.
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            new_request: fixture for a request
        """

        new_request.save()
        response = client.get(
            f'{API_BASE_URL_V1}/requests?include=wrong', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_include_key'].format('summary or deleted')

    def test_get_responders_request_summary_succeeds(
            self, client, auth_header, new_user, init_db, new_request_type,
            new_center, new_request):
        """
        Should succeed and return a responder request summary
        
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            new_user(dict): fixture to get user
            auth_header(dict): fixture to get token
            new_request(obj): fixture for a request
            new_request_type(obj): fixture for a request_type
            new_center(obj): fixture for a center
        """

        new_request.save()
        new_center.save()
        new_request_type.save()

        # dynamic filter with responder id
        response = client.get(
            f'{API_BASE_URL_V1}/requests?include=summary&responder_id={new_user.token_id}',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        response_data = response_json['data']

        assert response.status_code == 200
        data = response_data[-1]['requestSummary']
        mock_data = SUMMARY_REQUEST['requestSummary']
        assert data['totalRequests'] == mock_data['totalRequests']
        assert data['totalOpenRequests'] == mock_data['totalOpenRequests']
        assert data['totalInProgressRequests'] == mock_data[
            'totalInProgressRequests']
        assert data['totalClosedRequests'] == mock_data['totalClosedRequests']
        assert data['totalCompletedRequests'] == mock_data[
            'totalCompletedRequests']
        assert response_json['status'] == 'success'
        assert response_json['message'] == \
            SUCCESS_MESSAGES['fetched'].format('Requests')

        # dynamic filter with request_type id
        response = client.get(
            f'{API_BASE_URL_V1}/requests?include=summary&request_type_id={new_request_type.id}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data']
        assert response.status_code == 200
        data = response_data[-1]['requestSummary']
        assert data['totalRequests'] == mock_data['totalRequests']

        # dynamic filteer with center id
        response = client.get(
            f'{API_BASE_URL_V1}/requests?include=summary&center_id={new_user.center_id}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data']
        assert response.status_code == 200
        data = response_data[-1]['requestSummary']
        assert data['totalRequests'] == mock_data['totalRequests']

        # dynamic filter with requester id
        response = client.get(
            f'{API_BASE_URL_V1}/requests?include=summary&requester_id={new_user.token_id}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data']
        assert response.status_code == 200
        data = response_data[-1]['requestSummary']
        assert data['totalRequests'] == mock_data['totalRequests']

        # dynamic filter with requester id and center id
        response = client.get(
            f'{API_BASE_URL_V1}/requests?include=summary&requester_id={new_user.token_id}&center_id={new_user.center_id}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data']
        assert response.status_code == 200
        data = response_data[-1]['requestSummary']
        assert data['totalRequests'] == mock_data['totalRequests']
