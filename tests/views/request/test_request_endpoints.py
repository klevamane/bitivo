"Module for request endpoints test"

from flask import json  #pylint: disable=E0401

# models
from api.models import Request

# constants
from api.utilities.constants import CHARSET

# messages
from api.utilities.messages.error_messages import (serialization_errors,
                                                   query_errors, filter_errors)
from api.utilities.messages.success_messages import SUCCESS_MESSAGES

# mock data
from tests.mocks.requests import EXPECTED_REQUEST_RESPONSE_KEYS

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1  #pylint: disable=C0103


class TestRequestsEndpoints:  # pylint: disable=R0904
    """"Request endpoints test"""

    def test_get_requests_endpoint_succeeds(  # pylint: disable=R0201,C0103
            self,
            client,
            init_db,  # pylint: disable=W0613
            auth_header,
            request_list):
        """Test get request list endpoint

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            request_list (list): fixture for list of created requests

        """
        request_instance, = request_list[-1],

        response = client.get(f'{BASE_URL}/requests', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        request_response = response_json["data"][0]

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert isinstance(response_json["data"], list)
        assert len(response_json["data"]) >= 5
        assert request_response["id"] == request_instance.id
        assert request_response["subject"] == request_instance.subject
        assert request_response["description"] == request_instance.description
        assert request_response["requestType"][
            'id'] == request_instance.request_type_id
        assert request_response["status"] == request_instance.status.value
        assert isinstance(request_response["requester"], dict)
        assert isinstance(request_response["requester"]['role'], dict)
        assert isinstance(request_response["responder"], dict)
        assert isinstance(request_response["responder"]['role'], dict)
        assert isinstance(request_response["attachments"], list)
        assert isinstance(request_response["closedBySystem"], bool)
        assert "serialNumber" in request_response
        assert "inProgressAt" in request_response
        assert "completedAt" in request_response
        assert "closedAt" in request_response
        assert "dueBy" in request_response
        assert "tokenId" in request_response["requester"]
        assert "name" in request_response["requester"]
        assert "email" in request_response["requester"]
        assert "tokenId" in request_response["responder"]
        assert "name" in request_response["responder"]
        assert "email" in request_response["responder"]
        assert len(EXPECTED_REQUEST_RESPONSE_KEYS) == len(
            request_response.keys())
        assert set(EXPECTED_REQUEST_RESPONSE_KEYS) == set(
            request_response.keys())

    def test_get_requests_endpoint_without_pagination_succeeds(  #pylint: disable=R0201,C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            request_list):
        """Test get request list endpoints

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token

        """

        response = client.get(
            f'{BASE_URL}/requests?pagination=False', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response_json['meta'] is None
        assert len(response_json['data']) == 5

    def test_get_requests_endpoint_pagination_succeeds(self, client, init_db,
                                                       auth_header):
        """Test get request list endpoint pagination

            Should return paginated list of requests

            Args:
                client (FlaskClient): fixture to get flask test client
                init_db (SQLAlchemy): fixture to initialize the test database
                auth_header (dict): fixture to get token

        """
        response = client.get(
            f'{BASE_URL}/requests?page=1&limit=3', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert 'meta' in response_json
        assert response_json['meta']['page'] == 1
        assert 'pagesCount' in response_json['meta']
        assert 'totalCount' in response_json['meta']
        assert response_json['status'] == 'success'
        assert isinstance(response_json['data'], list)
        assert len(response_json['data']) == 3

    def test_get_overdue_requests_succeeds(self, client, auth_header, init_db,
                                           overdue_requests):
        """Test to get a list of all overdue requests

        args:
            client(FlaskClient): Fixture to get flask test client
            auth_header(dict): Fixture to get token
            init_db(SQLAlchemy): Fixture to initialize test database
            overdue_requests(object): Fixture to bulk create overdue requests
        """

        response = client.get(
            f'{BASE_URL}/requests/overdue', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        response_one = response_json['data'][0]

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert isinstance(response_json["data"], list)
        assert "serialNumber" in response_one
        assert "inProgressAt" in response_one
        assert "completedAt" in response_one
        assert "closedAt" in response_one
        assert "dueBy" in response_one
        assert "tokenId" in response_one["requester"]
        assert "name" in response_one["requester"]
        assert "email" in response_one["requester"]
        assert "tokenId" in response_one["responder"]
        assert "name" in response_one["responder"]
        assert "email" in response_one["responder"]
        assert isinstance(response_one["requester"], dict)
        assert isinstance(response_one["requester"]['role'], dict)
        assert isinstance(response_one["responder"], dict)
        assert isinstance(response_one["responder"]['role'], dict)
        assert isinstance(response_one["attachments"], list)

    def test_get_soft_deleted_requests_succeeds(
            self, client, init_db, request_ctx,
            mock_request_two_obj_decoded_token, auth_header, new_request):
        """
        Test get requests inclusive of soft deleted requests

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_request (object): Fixture to create a new request
            request_ctx (object): request client context
            mock_request_obj_decoded_token (object): Mock decoded_token from request client context

        """

        new_request.save()
        new_request.delete()

        response = client.get(
            f'{BASE_URL}/requests?include=deleted', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        response_data = response_json['data'][0]

        assert response.status_code == 200
        assert response_data['id'] == new_request.id
        assert response_data["subject"] == new_request.subject
        assert response_data["description"] == new_request.description

    def test_get_soft_deleted_requests_with_invalid_query_param_fails(
            self, client, init_db, request_ctx,
            mock_request_two_obj_decoded_token, auth_header, new_request):
        """
        Should fail when invalid query param is passed in URL.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_request (object): Fixture to create a new request
            request_ctx (object): request client context
            mock_request_obj_decoded_token (object): Mock decoded_token from request client context

        """

        new_request.save()
        new_request.delete()

        response = client.get(
            f'{BASE_URL}/requests?include=del', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_include_key'].format('summary or deleted')
