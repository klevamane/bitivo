"""Test for hotdesk reports"""
import json
from unittest import mock

from api.utilities.constants import CHARSET
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import serialization_errors
from api.utilities.messages.error_messages.jwt_errors import error_dict
from api.utilities.messages.error_messages.urls_errors import error_args_dict
from api.utilities.constants import HOT_DESK_QUERY_KEYS, HOT_DESK_REPORT_QUERY_PARAMS

from ...mocks.google_sheet import GoogleSheetHelper

# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestHotDeskCurrentReport:
    """ Used in testing current report hot_desk"""

    def test_get_current_hot_desk_report_fails(self, client, init_db):
        """ Will test that fetching of hotdesk is fails with no credentials
        Args:
            client(FlaskCLient) A mock of calling report endPoint
            init_db(Database connection) Initialize connection
        """
        response = client.get(
            f'{API_BASE_URL_V1}/hot-desks/analytics?report=currentallocations')
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json["message"] == error_dict["NO_TOKEN_MSG"]
        assert response_json["status"] == 'error'

    def test_get_current_hot_desk_report_with_wrong_filter_fails(
            self, client, init_db, auth_header, new_user):
        """ Will test that fetching of hotdesk is fails with no credentials
        Args:
            client(FlaskCLient) A mock of calling report endPoint
            init_db(Database connection) Initialize connection
        """
        new_user.save()
        response = client.get(
            f'{API_BASE_URL_V1}/hot-desks/analytics?repor=currentallocations',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["message"] == serialization_errors[
            'invalid_query_key'].format(HOT_DESK_QUERY_KEYS)
        assert response_json["status"] == 'error'

    @mock.patch(
        "api.views.hot_desk_analytics.GoogleSheetHelper",
        GoogleSheetHelper,
    )
    def test_get_current_hot_desk_report_succeeds(self, client, init_db,
                                                  auth_header):
        """ Will test that fetching of hotdesk is successful
        Args:
            mock_client(method) A mock for calling google Hotdesk
            client(FlaskCLient) A mock of calling report endPoint
            init_db(Database connection) Initialize connection
            auth_header(dict) Endpoint headers
        """
        response = client.get(
            f'{API_BASE_URL_V1}/hot-desks/analytics?report=currentallocations',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json["data"]["currentAllocations"]["available"] == 2
        assert response_json["data"]["currentAllocations"]["approved"] == 6
        assert response_json["message"] == SUCCESS_MESSAGES[
            'asset_report'].format('currentAllocations')
        assert response_json["status"] == "Success"

    def test_get_report_with_invalid_query_param_wrong_value_fails(
            self, client, init_db, auth_header):
        """
         Will test that fetching of report of analytics fails with
        nont existant args
        Args:
            mock_client(method) A mock for calling google Hotdesk
            client(FlaskCLient) A mock of calling report endPoint
            init_db(Database connection) Initialize connection
            auth_header(dict) Endpoint headers
        """
        response = client.get(
            f'{API_BASE_URL_V1}/hot-desks/analytics?report=currentallocation',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["message"] == serialization_errors[
            "invalid_request_param"].format(
                'report query', ', '.join(HOT_DESK_REPORT_QUERY_PARAMS))
        assert response_json["status"] == "error"
