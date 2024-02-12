# Standard Library
import json


# Local Module
from api.utilities.constants import CHARSET
from api.utilities.messages.error_messages import (
    serialization_error, jwt_errors
)

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1


class TestGetHotDeskComplaints:
    """Test hotdesk complaints endpoints"""

    def test_get_user_hot_desk_complaints_without_query_params_succeeds(
        self, client, auth_header, new_hot_desk_request, new_user
    ):
        """
        Tests that making the request with a valid user-id without query params
        succeeds

        Args:
            client (FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get token
            new_hot_desk_request: fixture to create hot desk
            new_user: fixture to create new user

        """
        new_hot_desk_request.save()
        response = client.get(
            BASE_URL + '/hot-desks/complaints/{}'.format(new_user.token_id),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == "success"
        assert response_json['data']['requester']['email'] == new_user.email
        assert response_json['data']['requester']['name'] == new_user.name
        assert response_json['data']['requester']['tokenId'] == new_user.token_id
        assert response_json['meta'] is not None

    def test_get_user_hot_desk_complaints_with_query_params_succeeds(
        self, client, auth_header, new_hot_desk_request_with_complaint, new_user
    ):
        """
        Test that making the request with the right query params succeeds

        Args:
            client (FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get token
            new_hot_desk_request_with_complaint: fixture to create hot desk
            new_user: fixture to create new user

        """
        url = BASE_URL + '/hot-desks/complaints/{}?startDate={}&pagination=false' \
            .format(
                new_user.token_id,
                new_hot_desk_request_with_complaint.complaint_created_at.strip(' 00:00')
            )
        complaint = new_hot_desk_request_with_complaint.complaint
        new_hot_desk_request_with_complaint.save()
        response = client.get(
            url,
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == "success"
        assert response_json['data']['hotDesksWithComplaints'][0]['complaint'] == complaint
        assert response_json['meta'] is None
        assert isinstance(response_json['data']['hotDesksWithComplaints'], list)

    def test_get_user_hot_desk_complaints_reverse_dates_fails(
        self, client, auth_header, new_hot_desk_request, new_user
    ):
        """
        Test that supplying a start-date greater than the end-date fails

        Args:
            client (FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get token
            new_hot_desk_request: fixture to create hot desk
            new_user: fixture to create new user

        """
        response = client.get(
            BASE_URL + '/hot-desks/complaints/{}?startDate={}&endDate={}'
            .format(new_user.token_id, '2019-4-1', '2019-3-1'),
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == "error"
        assert response_json['message'] == serialization_error \
            .error_dict['invalid_date_range']


    def test_get_user_hot_desk_complaints_when_token_not_passed_fails(
            self, client, new_hot_desk_request, new_user):
        """
        Test get users hotdesk complaints when token not passed

        Args:
            client (FlaskClient): fixture to get flask test client
            new_hot_desk_request: fixture to create hot desk
            new_user: fixture to create new user

        """
        new_hot_desk_request.save()
        response = client.get(
            BASE_URL + '/hot-desks/complaints/{}'.format(new_user.token_id)
            )
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_get_user_hot_desk_complaints_invalid_user_id_fails(
            self, client, auth_header, new_hot_desk_request):
        """
        Test get users hotdesk complaints when user id does not exist.

        Args:
            client (FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get token
            new_hot_desk_request: fixture to create hot desk
        """
        response = client.get(
            BASE_URL + '/hot-desks/complaints/{}'.format('wrong_id'),
            headers=auth_header
            )
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_error \
            .error_dict['not_found'].format('User')
