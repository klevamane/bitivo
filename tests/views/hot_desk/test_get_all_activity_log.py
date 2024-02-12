import json

# Local Module
from api.utilities.messages.error_messages import serialization_errors
from api.utilities.constants import CHARSET

# app config
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1


class TestGetSingleHotDesk:
    """Test Single hotdesk request"""

    def test_get_activity_log_of_specific_user_succeeds(
            self, client, auth_header, new_hot_desk_request, new_user):
        """Tests get activity log of user's request succeed
        client (func): Flask test client
        auth_header (func): Authentication token
        new_hot_desk_request: a valid Hot_Desk_Request object
        new_user: a valid user
         Returns:
            None
        """
        new_hot_desk_request.save()
        token_id = new_user.token_id
        response = client.get(
            f'{BASE_URL}/history/{new_user.token_id}', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['fetched'].format(
            'Hot desk activity log')
        assert 'requester' in response_json['data']
        assert 'activityLog' in response_json['data']
        assert 'meta' in response_json['data']
        assert f'{BASE_URL}/history/{token_id}?page=1&limit=10' \
            in response_json['data']['meta']['firstPage']
        assert f'{BASE_URL}/history/{token_id}' \
            in response_json['data']['meta']['currentPage']

    def test_get_activity_log_of_specific_if_user_has_no_request_succeeds(
            self, client, auth_header, approved_hot_desk_request, second_user):
        """Tests get activity log of user with no request fail
        client (func): Flask test client
        auth_header (func): Authentication token
        approved_hot_desk_request: a valid Hot_Desk_Request object
        second_user: a valid user
        Returns:
            None
        """
        second_user.save()
        approved_hot_desk_request.save()
        response = client.get(
            f'{BASE_URL}/history/{second_user.token_id}', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert 'activityLog' in response_json['data']
        assert response_json['data']['activityLog'] == []

    def test_get_activity_log_of_specific_user_if_pagination_false_succeeds(
            self, client, auth_header, new_hot_desk_request, new_user):
        """Tests get activitylog of a specific user if pagination false succeeds
        client (func): Flask test client
        auth_header (func): Authentication token
        new_hot_desk_request: a valid Hot_Desk_Request object
        new_user: a valid user
         Returns:
            None
        """
        new_hot_desk_request.save()
        token_id = new_user.token_id
        response = client.get(
            f'{BASE_URL}/history/{new_user.token_id}?pagination=false', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert isinstance(response_json, dict)
        assert response_json['message'] == SUCCESS_MESSAGES['fetched'].format(
            'Hot desk activity log')
        assert 'requester' in response_json['data']
        assert 'activityLog' in response_json['data']
        assert response_json['data']['meta'] == None

    def test_get_activity_log_of_a_none_existing_user_fails(
            self, client, auth_header, new_hot_desk_request):
        """Tests get activity log of a none existing user
        client (func): Flask test client
        auth_header (func): Authentication token
        new_hot_desk_request: a valid Hot_Desk_Request object
        Returns:
            None
        """
        new_hot_desk_request.save()
        response = client.get(
            f'{BASE_URL}/history/-LKDC632BDkH8cndsJ', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json['message'] == serialization_errors[
            'not_found'].format('User')
