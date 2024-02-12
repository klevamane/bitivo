"""Module of tests for hot desk response counts endpoint"""
# System Imports
from flask import json

# app config
from config import AppConfig

# Messages
from api.utilities.constants import CHARSET, HOT_DESK_TRUE_VALUE, HOT_DESK_QUERY_PARAMS
from api.utilities.messages.error_messages import serialization_errors
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.models import HotDeskRequest

# enum
from api.utilities.enums import HotDeskRequestStatusEnum

BASE_URL = AppConfig.API_BASE_URL_V1


class TestResponseCountEndpoint:
    """TestResponseCountEndpoint resource with GET endpoint"""

    def test_request_response_count_endpoint_without_token_fails(self, client):
        """Should return an error when an unauthenticated user access the endpoint
         Args:
            client(FlaskCLient) A mock of calling report endPoint
        """

        response = client.get(
            f'{BASE_URL}/hot-desks?count=True',
            headers={'Authorization': 'Bearer invalid_token'})
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json[
            'message'] == 'Authorization failed due to an Invalid token.'
        assert response_json['status'] == 'error'

    def test_get_current_hot_desk_response_count_details_with_wrong_filter_fails(
            self, client, init_db, auth_header, new_user):
        """ Will test that fetching of response counts
            hotdesk  with wrong filter params fails
        Args:
            client(FlaskCLient) A mock of calling report endPoint
            init_db(Database connection) Initialize connection
            auth_header(dict) Endpoint headers
        """
        new_user.save()
        response = client.get(
            f'{BASE_URL}/hot-desks?coun=True', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json[
            "message"] == serialization_errors['invalid_request_param'].format(
                'query param', ', '.join(HOT_DESK_QUERY_PARAMS))
        assert response_json["status"] == 'error'

    def test_get_response_count_with_invalid_query_param_wrong_value_fails(
            self, client, init_db, auth_header):
        """
        test response count with invalid query params
        Args:
            client(FlaskCLient) A mock of calling report endPoint
            init_db(Database connection) Initialize connection
            auth_header(dict) Endpoint headers
        """
        response = client.get(
            f'{BASE_URL}/hot-desks?count=rue', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json[
            "message"] == serialization_errors["invalid_request_param"].format(
                'param value', ', '.join(HOT_DESK_TRUE_VALUE))
        assert response_json["status"] == "error"

    def test_get_hot_desk_response_count_succeeds(
            self, client, init_db, new_hot_desk_request_two,
            new_hot_desk_request_three, auth_header, new_hot_desk_request):
        """ Will test that fetching of response counts hotdesk is successful
        Args:
            client(FlaskCLient) A mock of calling report endPoint
            init_db(Database connection) Initialize connection
            auth_header(dict) Endpoint headers
            new_hot_desk_request(Hotdesk): Fixture to create pending hot desk
            new_hot_desk_request_two(Hotdesk): Fixture to create pending hot desk
            new_hot_desk_request_three(Hotdesk): Fixture to another create pending hot desk
        """
        new_hot_desk_request.save()
        new_hot_desk_request_two.save()
        new_hot_desk_request_three.save()
        hot_desk = HotDeskRequest.query_().filter_by(
            hot_desk_ref_no=new_hot_desk_request.hot_desk_ref_no).first()
        hot_desk.update_(status=HotDeskRequestStatusEnum.approved)
        hot_desk = HotDeskRequest.query_().filter_by(
            hot_desk_ref_no=new_hot_desk_request.hot_desk_ref_no).first()
        hot_desk.update_(status=HotDeskRequestStatusEnum.cancelled)
        hot_desk_two = HotDeskRequest.query_().filter_by(
            hot_desk_ref_no=new_hot_desk_request_two.hot_desk_ref_no).first()
        hot_desk_two.update_(status=HotDeskRequestStatusEnum.rejected)

        response = client.get(
            f'{BASE_URL}/hot-desks?count=True', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["data"]["responseCounts"][0]["assignee"][
            'tokenId'] == new_hot_desk_request.assignee_id
        assert response_json["data"]["responseCounts"][0][
            "approvalsCount"] == 1
        assert response_json["data"]["responseCounts"][0][
            "rejectionsCount"] == 1
        assert response_json["data"]["responseCounts"][0]["missedCount"] == 0

        assert response_json["message"] == SUCCESS_MESSAGES[
            'successfully_fetched'].format('responseCounts')
        assert response_json["status"] == "success"

    def test_get_hotdesk_response_count_endpoint_pagination_succeeds(
            self, client, auth_header):
        """Test get hot desk response counts endpoint pagination Should return paginated
            list
        """
        response = client.get(
            f'{BASE_URL}/hot-desks?count=True', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert 'meta' in response_json['data']
        assert response_json['data']['meta']['page'] == 1
        assert 'pagesCount' in response_json['data']['meta']
        assert 'totalCount' in response_json['data']['meta']
        assert response_json['status'] == 'success'
