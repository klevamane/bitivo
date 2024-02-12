"""Module for request type resource GET endpoint."""

# Third-party libraries
from flask import json

# utilities
from api.utilities.constants import CHARSET
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import jwt_errors

# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1
URL = f"{API_BASE_URL_V1}/request-types"


class TestRequestTypeGetEndpoints:
    """Class for request type resource GET endpoint test."""

    def test_get_a_list_of_request_type_succeed(self, client, auth_header,
                                                new_request_types):
        """Should return a 200 status code and a success message when a GET
        request is made to the request type endpoint.

        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            new_request_types(BaseModel): fixture for seeding request types
        """

        response = client.get(URL, headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response_json['message'] == SUCCESS_MESSAGES[
            'successfully_fetched'].format('Request types')
        assert response_json['status'] == 'success'
        assert isinstance(response_json['data'], list)

    def test_request_type_returned_succeed(self, client, auth_header):
        """Should return the a list of request types with the correct data type.

        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token

        """

        response = client.get(URL, headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        request_type_data = response_json['data'][0]

        assert isinstance(request_type_data['title'], str)
        assert isinstance(request_type_data['assignee'], dict)
        assert isinstance(request_type_data['centerId'], str)
        assert isinstance(request_type_data['responseTime'], dict)
        assert isinstance(request_type_data['resolutionTime'], dict)
        assert isinstance(request_type_data['closureTime'], dict)
        assert isinstance(request_type_data['requestsCount'], int)

    def test_request_type_pagination_meta_succeed(self, client, auth_header):
        """Should return the a list of request types and the pagination meta.

        Args:
            client(FlaskClient): fixture to get flask test client.
            auth_header(dict): fixture to get token.

        """

        response = client.get(URL + '?page=1&limit=4', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        request_type_data = response_json['data']
        request_type_meta = response_json['meta']

        assert request_type_meta['totalCount'] == len(request_type_data)
        assert request_type_meta['page'] == 1

    def test_request_type_with_no_token_fails(self, client):
        """Should return a 401 status code and an error message
         when no token is provided.

        Args:
            client(FlaskClient): fixture to get flask test client.

        """

        response = client.get(URL, headers={})

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']
