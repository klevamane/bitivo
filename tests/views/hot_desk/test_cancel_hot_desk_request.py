# Standard Library
import json
from datetime import datetime as dt
from unittest.mock import Mock

# Local Module
from api.utilities.constants import CHARSET
from tests.mocks.hot_desk import VALID_REASON, INVALID_REASON
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import serialization_errors, serialization_error
from api.utilities.messages.error_messages import jwt_errors 

# bot imports
from bot.tasks.slack_bot import BotTasks

# App config
from config import AppConfig


BASE_URL = AppConfig.API_BASE_URL_V1


class TestCancelHotDeskRequest:
    """Test cancel hotdesk request"""

    def test_cancel_hot_desk_request_succeeds(
            self, client, auth_header, new_hot_desk_request, new_user):
        """Test that the requester can cancel hotdesk successfully
        client (func): Flask test client
        auth_header (func): Authentication token
        new_hot_desk_request: a valid Hot_Desk_Request object
        new_user:create a new user
        Returns:
            None
        """
        BotTasks.update_google_sheet = Mock(return_value=True)
        new_hot_desk_request.save()
        hotdesk_ref_no = new_hot_desk_request.hot_desk_ref_no
        reason = json.dumps(VALID_REASON)
        response = client.patch(
            f'{BASE_URL}/hot-desks/{new_hot_desk_request.id}/cancel',
            data=reason, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == \
            SUCCESS_MESSAGES['successfully_cancelled'].format(
                'test user', hotdesk_ref_no)

    def test_cancel_hot_desk_request_with_non_existent_id_fails(
            self, client, auth_header):
        """Test cancel hotdesk with non existent id fails
           that does not exist
        client (func): Flask test client
        auth_header (func): Authentication token
        Returns:
            None
        """
        reason = json.dumps(VALID_REASON)
        response = client.patch(
            f'{BASE_URL}/hot-desks/LksnHv68hjnkvfd/cancel', data=reason,
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json['message'] == serialization_errors['not_found'].format(
            'Hot desk request')

    def test_cancel_hot_desk_request_when_status_not_pending_or_approved_fails(
            self, client, auth_header, new_hot_desk_request, new_user):
        """Test cancel when status not pending or approved_fails
           that is not pending or approved
        client (func): Flask test client
        auth_header (func): Authentication token
        new_hot_desk_request: a valid Hot_Desk_Request object
        Returns:
            None
        """
        new_hot_desk_request.save()
        reason = json.dumps(VALID_REASON)
        response = client.patch(
            f'{BASE_URL}/hot-desks/{new_hot_desk_request.id}/cancel', data=reason, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json['message'] == \
            serialization_errors['invalid_hotdesk_status'].format(
                'hot desk')

    def test_cancel_hot_desk_request_when_not_owner_fails(
            self, client, auth_header, approved_hot_desk_request, new_user_three):
        """Test cancel hot desk request when not the owner fails
        client (func): Flask test client
        auth_header (func): Authentication token
        approved_hot_desk_request: a valid Hot_Desk_Request object
        Returns:
            None
        """
        new_user_three.save()
        approved_hot_desk_request.requester_id = new_user_three.token_id
        approved_hot_desk_request.save()
        reason = json.dumps(VALID_REASON)
        response = client.patch(
            f'{BASE_URL}/hot-desks/{approved_hot_desk_request.id}/cancel',
            data=reason, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 403
        assert response_json['status'] == 'error'
        assert response_json['message'] == \
            serialization_errors['cant_cancel'].format(
                'hot desk')

    def test_cancel_hot_desk_request_when_no_reason_passed_fails(
            self, client, auth_header, new_hot_desk_request, new_user):
        """Test cancel hot desk request when no reason passed fails
        client (func): Flask test client
        auth_header (func): Authentication token
        new_hot_desk_request: a valid Hot_Desk_Request object
        new_user:create a new user
        Returns:
            None
        """
        new_hot_desk_request.save()
        reason = json.dumps(INVALID_REASON)
        response = client.patch(
            f'{BASE_URL}/hot-desks/{new_hot_desk_request.id}/cancel',
            data=reason, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == \
            serialization_error.error_dict['select_reason'].format('cancellation reason')
    
    def test_cancel_hot_desk_request_when_token_not_passed(
            self, client, new_hot_desk_request, new_user):
        """Test cancel hot desk request when token not passed
        client (func): Flask test client
        new_hot_desk_request: a valid Hot_Desk_Request object
        new_user:create a new user
        Returns:
            None
        """
        new_hot_desk_request.save()
        reason = json.dumps(INVALID_REASON)
        response = client.patch(
            f'{BASE_URL}/hot-desks/{new_hot_desk_request.id}/cancel',
            data=reason)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == \
            jwt_errors["NO_TOKEN_MSG"].format('Reason')
