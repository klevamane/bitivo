import json

# Local Module
from api.utilities.messages.error_messages import serialization_errors
from api.utilities.constants import CHARSET

# app config
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from config import AppConfig

# Enum
from api.utilities.enums import HotDeskRequestStatusEnum

BASE_URL = AppConfig.API_BASE_URL_V1


class TestGetSingleHotDesk:
    """Test Single hotdesk request"""

    def test_get_single_hot_desk_request_with_non_existent_id_fails(
            self, client, auth_header, new_hot_desk_request):
        """Tests that hot desk requests by a user is successfully fetched
        client (func): Flask test client
        auth_header (func): Authentication token
        new_hot_desk_request: a valid Hot_Desk_Request object
         Returns:
            None
        """
        new_hot_desk_request.save()
        response = client.get(
            f'{BASE_URL}/hot-desks/-LckIxOyx8SOD4hz1ed4a', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'not_found'].format('Hot desk request')

    def test_get_single_hot_desk_request_when_owner_succeeds(
            self, client, auth_header, new_hot_desk_request):
        """Tests that hot desk requests by a user is successfully fetched
        client (func): Flask test client
        auth_header (func): Authentication token
        new_hot_desk_request: a valid Hot_Desk_Request object
         Returns:
            None
        """
        new_hot_desk_request.save()
        response = client.get(
            f'{BASE_URL}/hot-desks/{new_hot_desk_request.id}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data']
        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == SUCCESS_MESSAGES[
            'successfully_fetched'].format('Hotdesk Request')
        assert response_data['id'] == new_hot_desk_request.id
        assert 'approver' in response_json['data']

    def test_get_single_hot_desk_request_when_not_owner_fails(
            self, client, auth_header, test_hot_desk_request):
        """Tests that hot desk requests by a user is successfully fetched
        client (func): Flask test client
        auth_header (func): Authentication token
        test_hot_desk_request: a valid Hot_Desk_Request object
         Returns:
            None
        """
        test_hot_desk_request.status = HotDeskRequestStatusEnum.pending
        new_hot_desk_request = test_hot_desk_request.save()
        response = client.get(
            f'{BASE_URL}/hot-desks/{new_hot_desk_request.id}',
            headers=auth_header)
        assert response.status_code == 403
        assert response.json['status'] == 'error'
        assert response.json['message'] == serialization_errors['cant_view']
