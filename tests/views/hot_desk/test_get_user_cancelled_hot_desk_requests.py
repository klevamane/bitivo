from datetime import datetime
import json
# Local Module
from api.utilities.constants import CHARSET
from api.utilities.messages.error_messages import jwt_errors

# app config
from api.utilities.messages.success_messages import SUCCESS_MESSAGES

from config import AppConfig
from api.utilities.enums import HotDeskRequestStatusEnum
BASE_URL = AppConfig.API_BASE_URL_V1


class TestGetCancelledHotDeskRequestsByUser:
    """Test get cancelled hot desk request by user"""

    def test_get_cancelled_hot_desk_requests_succeeds(
            self, client, auth_header, new_hot_desk_request, new_user):
        """Tests that cancelled hot desk requests by a user is successfully fetched
        client (func): Flask test client
        auth_header (func): Authentication token
        new_hot_desk_request (Fixture): a fixture to create a new hot desk request
        new_user (Fixture): a fixture to create a new user
        Returns:
            None
        """
        new_user.save()
        new_hot_desk_request.status = HotDeskRequestStatusEnum.cancelled
        new_hot_desk_request.created_at = datetime.utcnow()
        new_hot_desk_request.save()
        token_id = new_user.token_id
        response = client.get(
            f'{BASE_URL}/hot-desks/cancelled/{token_id}', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert isinstance(response_json, dict)
        assert isinstance(response_json['meta'], dict)
        assert isinstance(response_json['data']['hotDesks'], list)
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['fetched'].format(
            'Cancelled hot desk requests for user')
        assert response_json['data']['hotDesks'][0]['id'] == new_hot_desk_request.id
        assert response_json['data']['hotDesks'][0]['status'] == new_hot_desk_request.status.value
        assert response_json['data']['hotDesks'][0]['approver']['tokenId'] == new_hot_desk_request.assignee_id
        assert f'{BASE_URL}/hot-desks/cancelled/{token_id}?page=1&limit=10' in response_json['meta']['firstPage']
        assert f'{BASE_URL}/hot-desks/cancelled/{token_id}' in response_json['meta']['currentPage']
        assert response_json['meta']['pagesCount'] == 1

    def test_get_cancelled_hot_desk_requests_pagination_false_succeeds(
            self, client, auth_header, new_hot_desk_request, new_user):
        """Tests that cancelled hot desk requests by a user without pagination is successfully fetched
        client (func): Flask test client
        auth_header (func): Authentication token
        new_hot_desk_request (Fixture): a fixture to create a new hot desk request
        new_user (Fixture): a fixture to create a new user
        Returns:
            None
        """
        token_id = new_user.token_id
        response = client.get(
            f'{BASE_URL}/hot-desks/cancelled/{token_id}?pagination=false', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert isinstance(response_json, dict)
        assert isinstance(response_json['data']['hotDesks'], list)
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['fetched'].format(
            'Cancelled hot desk requests for user')
        assert response_json['data']['hotDesks'][0]['id'] == new_hot_desk_request.id
        assert response_json['data']['hotDesks'][0]['status'] == new_hot_desk_request.status.value
        assert response_json['data']['hotDesks'][0]['approver']['tokenId'] == new_hot_desk_request.assignee_id
        assert response_json['meta'] is None

    def test_get_cancelled_hot_desk_requests_non_existing_requester_fail(
            self, client, auth_header, new_hot_desk_request):
        """Tests that cancelled hot desk requests by a non existing user
        client (func): Flask test client
        auth_header (func): Authentication token
        new_hot_desk_request (Fixture): a fixture to create a new hot desk request
        Returns:
            None
        """
        new_hot_desk_request.status = HotDeskRequestStatusEnum.cancelled
        new_hot_desk_request.created_at = datetime.utcnow()
        new_hot_desk_request.save()
        response = client.get(
            f'{BASE_URL}/hot-desks/cancelled/-hds43fb3JGCHkj-df', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'User not found'

    def test_get_cancelled_hot_desk_requests_no_token(
            self, client):
        """Tests that cancelled hot desk requests when a token is not provided
        client (func): Flask test client
        Returns:
            None
        """
        response = client.get(
            f'{BASE_URL}/hot-desks/cancelled/-hds43fb3JGCHkj-df')
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_get_cancelled_hot_desk_requests_no_cancelled_requests_succeeds(
            self, client, auth_header, new_hot_desk_request, new_user_two):
        """Tests that cancelled hot desk requests by a user is successfully fetched
        client (func): Flask test client
        auth_header (func): Authentication token
        new_hot_desk_request (Fixture): a fixture to create a new hot desk request
        new_user_two (Fixture): a fixture to create a new user
        Returns:
            None
        """
        new_user_two.save()
        new_hot_desk_request.save()
        response = client.get(
            f'{BASE_URL}/hot-desks/cancelled/{new_user_two.token_id}', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert len(response_json['data']['hotDesks']) == 0
