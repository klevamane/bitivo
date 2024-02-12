# Standard Library
import json
import datetime

# Local Module
from api.utilities.messages.error_messages import serialization_errors, jwt_errors
from api.utilities.constants import HOT_DESK_REPORT_QUERIES, CHARSET, MIMETYPE_CSV

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1
analytics_url = BASE_URL + '/hot-desks/analytics/export?report={}'


class TestExportHotDeskAnalyticsEndpoints:
    """Test hotdesk analytics endpoints"""

    def test_hot_desk_analytics_report_is_called(self, client, init_db,
                                                 auth_header, new_user):
        """Should return status code 200

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token

        """
        new_user.save()
        response = client.get(
            analytics_url.format('requests'), headers=auth_header)
        assert response.status_code == 200

    def test_non_matching_query_value(self, client, auth_header):
        """Test with an invalid report query

        Args:
            client (FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get token

        """
        response = client.get(
            analytics_url.format('random'),
            headers=auth_header,
        )

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json[
            'message'] == serialization_errors['invalid_request_param'].format(
                'report query', ', '.join(HOT_DESK_REPORT_QUERIES))

    def test_hot_desk_analytics_report_invalid_token_fails(self, client):
        """Test with invalid token

        Args:
            client (FlaskClient): fixture to get flask test client

        """
        response = client.get(analytics_url.format('requests'))
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_hot_desk_analytics_report_with_invalid_date_params_fails(
            self, init_db, client, auth_header):
        """Test with invalid date params

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token

        """

        response = client.get(
            analytics_url.format('requests') +
            '&endDate=201-1-3&startDate=201-12-1',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_date'].format('201-12-1')

    def test_hot_desk_analytics_report_with_start_date_greater_end_date_fails(
            self, init_db, client, auth_header):
        """Test with invalid date params

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token

        """

        response = client.get(
            analytics_url.format('requests') +
            '&startDate=2019-03-12&endDate=2019-03-10',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_date_range']

    def test_for_when_no_parameters_are_passed_succeeds(
            self, client, auth_header):
        """Tests for when no query parameter is passed. Should return status
            code 200 and a message.

        Args:
            client (func): Flask test client
            auth_header (func): Authentication token

        Returns:
            None

        """

        response = client.get(
            analytics_url.format(''),
            headers=auth_header,
        )

        assert response.status_code == 200

        assert b'to_be_implemented\r\nEndpoint yet to be implemented\r\n' \
            in response.data

    def test_export_hot_desk_report_as_csv_succeeds(
            self, init_db, client, auth_header, new_hot_desk_request):
        """Tests for when no query parameter is passed

        Args:
            init_db (SQLAlchemy): fixture to initialize the test database
            client (func): Flask test client
            auth_header (func): Authentication token
            new_hot_desk_request: a valid Hot_Desk_Request object

        Returns:
            None

        """
        yesterday_date = datetime.datetime.strftime(
            datetime.datetime.today() + datetime.timedelta(-1), '%Y-%m-%d')
        today_date = datetime.datetime.strftime(
            datetime.datetime.today() + datetime.timedelta(0), '%Y-%m-%d')
        tomorrow_date = datetime.datetime.strftime(
            datetime.datetime.today() + datetime.timedelta(1), '%Y-%m-%d')
        new_hot_desk_request.save()

        response = client.get(
            analytics_url.format('requests') +
            '&startDate={}&endDate={}'.format(yesterday_date, tomorrow_date),
            headers=auth_header)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == MIMETYPE_CSV
        response = response.data.decode()
        assert 'createdAt,status,hotDeskRefNo,email' in response
        assert 'pending,1G 65,testemail@andela.com' in response
        assert '{}'.format(today_date) in response
