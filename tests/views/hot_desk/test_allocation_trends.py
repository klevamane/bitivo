"""Module of tests for hot desk allocation get endpoint"""
# System Imports
from flask import json
from datetime import datetime as dt

# Messages
from api.utilities.constants import CHARSET, HOT_DESK_QUERY_KEYS
from api.utilities.messages.error_messages import serialization_errors
from api.utilities.constants import HOT_DESK_REPORT_FREQUENCY

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1

START_DATE = dt.now().strftime("%Y-%m-%d")
END_DATE = dt.now().strftime("%Y-%m-%d")


class TestAllocationTrends(object):
    """TestGetHotDeskAllocationEndpoint resource with GET endpoint"""

    def test_get_all_weekly_allocation_trends_succeeds(
            self, client, auth_header, multiple_approved_hot_desk_request):
        """Should get all weekly allocation trends

        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
            multiple_approved_hot_desk_request (dict): dict to get multiple hot desk requests
        """
        response = client.get(
            f'{BASE_URL}/hot-desks/analytics?report=trendsAllocations&frequency=week&startDate={START_DATE}&endDate={END_DATE}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data']
        assert response.status_code == 200
        assert len(response_data['trendsAllocations'][0]) > 0
        assert 'floor' in response_data['trendsAllocations'][0]
        assert 'period' in response_data['trendsAllocations'][0]
        assert 'values' in response_data['trendsAllocations'][0]

    def test_get_all_monthly_allocation_trends_succeeds(
            self, client, auth_header, multiple_approved_hot_desk_request):
        """Should get all monthly allocation trends

        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
            multiple_approved_hot_desk_request (dict): dict to get multiple hot desk requests
        """
        response = client.get(
            f'{BASE_URL}/hot-desks/analytics?report=trendsAllocations&frequency=month&startDate={START_DATE}&endDate={END_DATE}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data']
        assert response.status_code == 200
        assert len(response_data['trendsAllocations'][0]) > 0
        assert 'floor' in response_data['trendsAllocations'][0]
        assert 'period' in response_data['trendsAllocations'][0]
        assert 'values' in response_data['trendsAllocations'][0]

    def test_get_all_yearly_allocation_trends_succeeds(
            self, client, auth_header, multiple_approved_hot_desk_request):
        """Should get all yearly allocation trends

        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
            multiple_approved_hot_desk_request (dict): dict to get multiple hot desk requests
        """
        response = client.get(
            f'{BASE_URL}/hot-desks/analytics?report=trendsAllocations&frequency=year&startDate={START_DATE}&endDate={END_DATE}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data']
        assert response.status_code == 200
        assert len(response_data['trendsAllocations'][0]) > 0
        assert 'floor' in response_data['trendsAllocations'][0]
        assert 'period' in response_data['trendsAllocations'][0]
        assert 'values' in response_data['trendsAllocations'][0]

    def test_get_all_quarterly_allocation_trends_succeeds(
            self, client, auth_header, multiple_approved_hot_desk_request):
        """Should get all quarterly allocation trends

        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
            multiple_approved_hot_desk_request (dict): dict to get multiple hot desk requests
        """
        response = client.get(
            f'{BASE_URL}/hot-desks/analytics?report=trendsAllocations&frequency=quarter&startDate={START_DATE}&endDate={END_DATE}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data']
        assert response.status_code == 200
        assert len(response_data['trendsAllocations'][0]) > 0
        assert 'floor' in response_data['trendsAllocations'][0]
        assert 'period' in response_data['trendsAllocations'][0]
        assert 'values' in response_data['trendsAllocations'][0]

    def test_get_all_allocation_trends_with_invalid_frequency_fails(
            self, client, auth_header):
        """Should fail when getting allocations with invalid frequency

        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
            multiple_approved_hot_desk_request (dict): dict to get multiple hot desk requests
        """
        response = client.get(
            f'{BASE_URL}/hot-desks/analytics?report=trendsAllocations&frequency=kamikaze&startDate={START_DATE}&endDate={END_DATE}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['message'] == serialization_errors[
            'invalid_choice'].format('frequency', HOT_DESK_REPORT_FREQUENCY)

    def test_get_all_allocation_trends_with_day_frequency_succeeds(
            self, client, auth_header, multiple_approved_hot_desk_request):
        """Should fail when getting allocations with invalid frequency

        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
            multiple_approved_hot_desk_request (dict): dict to get multiple hot desk requests
        """
        response = client.get(
            f'{BASE_URL}/hot-desks/analytics?report=trendsAllocations&frequency=day&startDate={START_DATE}&endDate={END_DATE}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data']
        assert response.status_code == 200
        assert len(response_data['trendsAllocations'][0]) > 0
        assert 'floor' in response_data['trendsAllocations'][0]
        assert 'period' in response_data['trendsAllocations'][0]
        assert 'values' in response_data['trendsAllocations'][0]

    def test_get_all_weekly_allocation_trends_of_a_user_succeeds(
            self, client, auth_header, new_user):
        """Should get all weekly allocation trends

        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
            new_user (str): the token_id of user
        """
        response = client.get(
            f'{BASE_URL}/hot-desks/analytics/{new_user.token_id}?report=trendsAllocations&frequency=week&startDate={START_DATE}&endDate={END_DATE}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data']
        assert response.status_code == 200
        assert len(response_data['trendsAllocations'][0]) > 0
        assert 'floor' in response_data['trendsAllocations'][0]
        assert 'period' in response_data['trendsAllocations'][0]
        assert 'values' in response_data['trendsAllocations'][0]

    def test_get_trends_of_a_user_without_query_param_succeeds(
            self, client, auth_header, new_user):
        """Should get all weekly allocation trends

        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
            new_user (str): the token_id of user
        """
        response = client.get(
            f'{BASE_URL}/hot-desks/analytics/{new_user.token_id}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['message']
        assert response.status_code == 400
        assert response_data == serialization_errors['invalid_request_param'].format(\
            'query param', ' or '.join(HOT_DESK_QUERY_KEYS))

    def test_get_all_monthly_allocation_trends_of_a_user_succeeds(
            self, client, auth_header, new_user):
        """Should get all monthly allocation trends

        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
            new_user (str): the token_id of user
        """
        response = client.get(
            f'{BASE_URL}/hot-desks/analytics/{new_user.token_id}?report=trendsAllocations&frequency=month&startDate={START_DATE}&endDate={END_DATE}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data']
        assert response.status_code == 200
        assert len(response_data['trendsAllocations'][0]) > 0
        assert 'floor' in response_data['trendsAllocations'][0]
        assert 'period' in response_data['trendsAllocations'][0]
        assert 'values' in response_data['trendsAllocations'][0]

    def test_get_all_yearly_allocation_trends_of_a_user_succeeds(
            self, client, auth_header, new_user):
        """Should get all yearly allocation trends

        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
            new_user (str): the token_id of user
        """
        response = client.get(
            f'{BASE_URL}/hot-desks/analytics/{new_user.token_id}?report=trendsAllocations&frequency=year&startDate={START_DATE}&endDate={END_DATE}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data']
        assert response.status_code == 200
        assert len(response_data['trendsAllocations'][0]) > 0
        assert 'floor' in response_data['trendsAllocations'][0]
        assert 'period' in response_data['trendsAllocations'][0]
        assert 'values' in response_data['trendsAllocations'][0]

    def test_get_all_quarterly_allocation_trends_of_a_user_succeeds(
            self, client, auth_header, new_user):
        """Should get all quarterly allocation trends

        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
            new_user (str): the token_id of user
        """
        response = client.get(
            f'{BASE_URL}/hot-desks/analytics/{new_user.token_id}?report=trendsAllocations&frequency=quarter&startDate={START_DATE}&endDate={END_DATE}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data']
        assert response.status_code == 200
        assert len(response_data['trendsAllocations'][0]) > 0
        assert 'floor' in response_data['trendsAllocations'][0]
        assert 'period' in response_data['trendsAllocations'][0]
        assert 'values' in response_data['trendsAllocations'][0]

    def test_get_all_allocation_trends_of_a_user_with_invalid_frequency_fails(
            self, client, auth_header, new_user):
        """Should fail when getting allocations with invalid frequency

        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
            new_user (str): the token_id of user
        """
        response = client.get(
            f'{BASE_URL}/hot-desks/analytics/{new_user.token_id}?report=trendsAllocations&frequency=thriller&startDate={START_DATE}&endDate={END_DATE}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['message'] == serialization_errors[
            'invalid_choice'].format('frequency', HOT_DESK_REPORT_FREQUENCY)

    def test_get_all_allocation_trends_of_a_user_with_day_frequency_succeeds(
            self, client, auth_header, new_user):
        """Should fail when getting allocations with invalid frequency

        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
            new_user (str): the token_id of user
        """
        response = client.get(
            f'{BASE_URL}/hot-desks/analytics/{new_user.token_id}?report=trendsAllocations&frequency=day&startDate={START_DATE}&endDate={END_DATE}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data']
        assert response.status_code == 200
        assert len(response_data['trendsAllocations'][0]) > 0
        assert 'floor' in response_data['trendsAllocations'][0]
        assert 'period' in response_data['trendsAllocations'][0]
        assert 'values' in response_data['trendsAllocations'][0]
