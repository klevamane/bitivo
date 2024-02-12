"""Tests for analytics for incidence reporting"""

# Standard Library
import json

# Local Module
from api.utilities.messages.error_messages import serialization_errors, jwt_errors
from api.utilities.constants import CHARSET, ASSET_REPORT_QUERIES

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1
ANALYTICS_URL = BASE_URL + '/assets/analytics'
INCIDENCE_REPORTING_URL = ANALYTICS_URL + '?report={}'


class TestAnalyticsIncidenceReporting:
    def test_get_analytics_for_incidence_report_succeeds(
            self, client, init_db, auth_header, open_request,
            new_expired_request, in_progress_request, closed_request,
            completed_request):
        """Test getting analytics for incidence report succeeds

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            open_request: fixture for an open request
            new_expired_request: fixture for an expired request
            in_progress_request: fixture for a request that is in progress
            closed_request: fixture for a closed request
            completed_request: fixture for a completed request
        """
        open_request.save()
        new_expired_request.save()
        in_progress_request.save()
        closed_request.save()
        completed_request.save()

        response = client.get(
            INCIDENCE_REPORTING_URL.format('incidencereport'),
            headers=auth_header)
        response_json = json.loads(
            response.data.decode(CHARSET))['data']['incidenceReport']
        total = response_json['total']

        assert response.status_code == 200
        assert type(response_json['categories']) == list
        assert 'totalOpenRequests' in total
        assert 'totalInProgressRequests' in total
        assert 'totalCompletedRequests' in total
        assert 'totalClosedRequests' in total
        assert 'totalOverdueRequests' in total

    def test_get_analytics_for_incidence_report_not_super_user_succeeds(
            self, client, init_db, auth_header_two, open_request,
            new_expired_request, in_progress_request, closed_request,
            completed_request, new_user):
        """Test getting analytics for incidence report by a non `super_user` succeeds

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header_three(dict): fixture to get token
            open_request: fixture for an open request
            new_expired_request: fixture for an expired request
            in_progress_request: fixture for a request that is in progress
            closed_request: fixture for a closed request
            completed_request: fixture for a completed request
        """
        open_request.save()
        new_expired_request.save()
        in_progress_request.save()
        closed_request.save()
        completed_request.save()

        new_user.save()
        response = client.get(
            INCIDENCE_REPORTING_URL.format('incidencereport'),
            headers=auth_header_two)
        response_json = json.loads(
            response.data.decode(CHARSET))['data']['incidenceReport']
        assert type(response_json['categories']) == list
        total = response_json['total']
        assert response.status_code == 200
        assert 'totalOpenRequests' in total
        assert 'totalInProgressRequests' in total
        assert 'totalCompletedRequests' in total
        assert 'totalClosedRequests' in total
        assert 'totalOverdueRequests' in total

    def test_get_analytics_for_incidence_report_with_invalid_query_param_value_fails(
            self, client, init_db, auth_header):
        """Test getting analytics for incidence report succeeds

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """

        response = client.get(
            INCIDENCE_REPORTING_URL.format('reportincidence'),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response_json['message'] == serialization_errors[
            'invalid_request_param'].format('report query', ', '.join(ASSET_REPORT_QUERIES))
        assert response.status_code == 400

        # Make sure 'incidencereport' exists in the ASSET_REPORT_QUERIES constants
        # as it's the basis for this test
        assert 'incidencereport' in ASSET_REPORT_QUERIES

    def test_get_analytics_for_incidence_report_with_no_token_fails(
            self, client, init_db):
        """Test getting analytics for incidence report succeeds

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        response = client.get(
            INCIDENCE_REPORTING_URL.format('incidencereport'))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_get_all_analytics_include_incidence_report_succeeds(
            self, client, init_db, auth_header):
        """Test getting analytics for incidence report succeeds

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        response = client.get(ANALYTICS_URL, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))['data']

        assert 'incidenceReport' in response_json
        assert 'assetFlow' in response_json
        assert 'assetOutflow' in response_json
        assert 'assetInflow' in response_json
        assert 'stockLevel' in response_json
