import json

# Local Module
from api.utilities.messages.error_messages import serialization_errors
from api.utilities.constants import CHARSET

# app config
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from config import AppConfig
from tests.mocks.hot_desk import VALID_HOT_DESK_COMPLAINT,\
    INVALID_HOT_DESK_COMPLAINT, INVALID_HOT_DESK_EMPTY_COMPLAINT

BASE_URL = AppConfig.API_BASE_URL_V1


class TestCreateHotdeskComplaint:
    """Test Patch endpoint to create a hotdesk complaint """

    def test_create_hotdesk_complaint_succeeds(self, client, auth_header,
                                               new_hot_desk_request):
        """Tests create a hotdesk complaint succeeds
                client (func): Flask test client
                auth_header (func): Authentication token
                new_hot_desk_request: a valid Hot_Desk_Request object
                 Returns:
                    None
                """
        new_hot_desk_request.save()
        data = json.dumps(VALID_HOT_DESK_COMPLAINT)
        response = client.patch(
            f'{BASE_URL}/hot-desks/{new_hot_desk_request.id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert response_json["message"] == SUCCESS_MESSAGES['updated'].format(
            'Hotdesk Request')
        assert response_json['data']['id'] == new_hot_desk_request.id
        assert response_json['data']['complaint'] == VALID_HOT_DESK_COMPLAINT[
            'complaint']
        assert response_json['data']['complaintCreatedAt'] is not None

    def test_create_hotdesk_complaint_with_less_than_5_characters_fails(
            self, client, auth_header, new_hot_desk_request):
        """Tests create a hotdesk complaint with less than 5 characters fails
                client (func): Flask test client
                auth_header (func): Authentication token
                new_hot_desk_request: a valid Hot_Desk_Request object
                 Returns:
                    None
                """
        new_hot_desk_request.save()
        data = json.dumps(INVALID_HOT_DESK_COMPLAINT)
        response = client.patch(
            f'{BASE_URL}/hot-desks/{new_hot_desk_request.id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == 'An error occurred'
        assert response_json['errors']['complaint'][0] == serialization_errors[
            'field_length'].format('5')

    def test_create_hotdesk_complaint_with_empty_compliant_field_fails(
            self, client, auth_header, new_hot_desk_request):
        """Tests create a hotdesk complaint with empty complaint fails
                      client (func): Flask test client
                      auth_header (func): Authentication token
                      new_hot_desk_request: a valid Hot_Desk_Request object
                       Returns:
                          None
                      """
        new_hot_desk_request.save()
        data = json.dumps(INVALID_HOT_DESK_EMPTY_COMPLAINT)
        response = client.patch(
            f'{BASE_URL}/hot-desks/{new_hot_desk_request.id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == 'An error occurred'
        assert response_json['errors']['complaint'][1] == serialization_errors[
            'not_empty']

    def test_create_hotdesk_complaint_when_not_owner_fails(
            self, client, auth_header, test_hot_desk_request):
        """Tests create a hotdesk complaint when not owner fails
                              client (func): Flask test client
                              auth_header (func): Authentication token
                              approved_hot_desk_request: a valid approved Hot_Desk_Request object
                               Returns:
                                  None
                              """
        new_hot_desk_request = test_hot_desk_request.save()
        data = json.dumps(VALID_HOT_DESK_COMPLAINT)
        response = client.patch(
            f'{BASE_URL}/hot-desks/{new_hot_desk_request.id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 403
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'request_status_update'].format('complaint')
