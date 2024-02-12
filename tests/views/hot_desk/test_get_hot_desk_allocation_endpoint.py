"""Module of tests for hot desk allocation get endpoint"""
# System Imports
from flask import json
from unittest import mock

# app config
from config import AppConfig

# Messages
from api.utilities.constants import CHARSET, HOT_DESK_REPORT_QUERY_PARAMS, HOT_DESK_QUERY_KEYS
from api.utilities.messages.error_messages import serialization_errors

from ...mocks.google_sheet import GoogleSheetHelper

BASE_URL = AppConfig.API_BASE_URL_V1


class TestGetHotDeskAllocationEndpoints(object):
    """TestGetHotDeskAllocationEndpoint resource with GET endpoint"""

    def test_user_without_a_token(self, client):
        """Should return an error when an unauthenticated user access the endpoint"""
        response = client.get(
            f'{BASE_URL}/hot-desks/analytics',
            headers={'Authorization': 'Bearer invalid_token'})
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json[
                   'message'] == 'Authorization failed due to an Invalid token.'
        assert response_json['status'] == 'error'

    @mock.patch(
        "api.views.hot_desk_analytics.GoogleSheetHelper",
        GoogleSheetHelper,
    )
    def test_get_all_hotdesk_allocation_succeeds(self, client, auth_header,
                                                 approved_hot_desk_request):
        """Should pass when the hot desk allocations is fetched
        successfully

        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
        """
        hotdesk_allocation = approved_hot_desk_request.save()
        response = client.get(
            f'{BASE_URL}/hot-desks/analytics', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data']
        assert response.status_code == 200
        assert len(response_data['approvedRequests']['data']) > 0
        assert hotdesk_allocation.requester_id == \
               response_data['approvedRequests']['data'][0]['requester_id']

    def test_get_hotdesk_allocation_with_report_query_param_eql_approved_requests_succeeds(
        self, client, auth_header, new_hot_desk_request):
        """Should get all hotdesk allocation which has the status \
        column equal to the report param provided

        Args:
            client(FlaskClient): fixture to get flask test client.
            auth_header(dict): fixture to get token.
        """
        new_hot_desk_request.save()
        response = client.get(
            f'{BASE_URL}/hot-desks/analytics?report=approvedRequests',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data']
        assert response.status_code == 200
        assert len(response_data['approvedRequests']) > 0

    def test_invalid_query_param_passed(self, client, auth_header,
                                        new_hot_desk_request):
        """Should throw an error when an invalid query param is passed"""
        new_hot_desk_request.save()
        response = client.get(
            f'{BASE_URL}/hot-desks/analytics?invalid_query_param=approvedRequests',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_query_key'].format(HOT_DESK_QUERY_KEYS)

    def test_invalid_query_param_value_passed(self, client, auth_header,
                                              new_hot_desk_request):
        """Should throw an error when an invalid value is passed to the query parameter"""
        new_hot_desk_request.save()
        response = client.get(
            f'{BASE_URL}/hot-desks/analytics?report=invalid_value_for_query_param',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_request_param'].format('report query',
                                            ', '.join(HOT_DESK_REPORT_QUERY_PARAMS))

    @mock.patch(
        "api.views.hot_desk_analytics.GoogleSheetHelper",
        GoogleSheetHelper,
    )
    def test_get_hotdesk_allocation_endpoint_pagination_succeeds(
        self, client, new_hot_desk_request, auth_header):
        """Test get hot desk allocations endpoint pagination Should return paginated list
        of hot desk allocations
        """
        response = client.get(
            f'{BASE_URL}/hot-desks/analytics', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert 'meta' in response_json['data']['approvedRequests']
        assert response_json['data']['approvedRequests']['meta']['page'] == 1
        assert 'pagesCount' in response_json['data']['approvedRequests'][
            'meta']
        assert 'totalCount' in response_json['data']['approvedRequests'][
            'meta']
        assert response_json['status'] == 'Success'
