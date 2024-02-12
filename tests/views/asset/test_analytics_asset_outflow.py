"""Tests for analytics asset outflow report"""

# Standard Library
import json
from datetime import datetime, date, timedelta

# Local Module
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import serialization_errors
from api.utilities.constants import CHARSET, ASSET_REPORT_QUERIES

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1
ANALYTICS_URL = BASE_URL + '/assets/analytics'
ASSET_FLOW_URL = BASE_URL + '/assets/analytics?report='
ASSET_OUTFLOW_URL_WITH_QUERY = ASSET_FLOW_URL + 'assetOutflow'
ASSET_OUTFLOW_URL_WITH_QUERY_AND_START_DATE = ASSET_FLOW_URL + 'assetOutflow&startDate={}'

ASSET_OUTFLOW_URL_WITH_QUERY_AND_DATES = ASSET_FLOW_URL + 'assetOutflow&startDate={}' \
                                        '&endDate={}'

ASSET_OUTFLOW_URL_WITH_QUERY_AND_END_DATE = ASSET_FLOW_URL + 'assetOutflow&endDate={}'

START_DATE_STRING = date.today() - timedelta(days=7)
END_DATE_STRING = date.today()


class TestAssetAnalyticsAssetOutflowEndpoints:
    """Test for asset analytics asset outflow endpoint"""

    def test_for_asset_outflow_report_is_grouped(self, client, init_db,
                                                 auth_header, asset_out_flow):
        """The response data should be properly grouped

        Args:
            init_db (func): Initialize test database
            client (func): Flask test client
            asset_out_flow (func): Saves asset outflow record
            auth_header (func): Authentication token
        """
        response = client.get(
            ASSET_OUTFLOW_URL_WITH_QUERY, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        data = json.loads(response.data.decode(CHARSET))['data']
        outflow_response = data['assetOutflow'][0]
        status = response_json['status']
        asset_in_store = outflow_response['assets'][0]['assignee']
        assert SUCCESS_MESSAGES['asset_report'].format(
            'assetOutflow') == response_json['message']
        assert response.status_code == 200
        assert 'message' in response_json
        assert 'status' in response_json
        assert 'assetOutflow' in data
        assert 'category' in outflow_response
        assert 'assignedBy' in outflow_response
        assert 'quantity' in outflow_response
        assert 'dateAssigned' in outflow_response
        assert 'name' in asset_in_store
        assert status == 'Success'

    def test_for_asset_outflow_report_is_grouped_with_start_and_end_date_succeeds(
            self, client, init_db, auth_header, asset_out_flow):
        """The response data should be properly grouped

        Args:
            init_db (func): Initialize test database
            client (func): Flask test client
            sset_out_flow (func): Saves asset outflow record
            auth_header (func): Authentication token
        """
        response = client.get(
            ASSET_OUTFLOW_URL_WITH_QUERY_AND_DATES.format(
                START_DATE_STRING, END_DATE_STRING),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = json.loads(response.data)['data']
        assert len(response_data) == 1
        assert response.status_code == 200
        assert response_json['message'] == SUCCESS_MESSAGES[
            'asset_report'].format('assetOutflow')
        assert isinstance(response_data['assetOutflow'], list)
        for item in json.loads(response.data)['data']['assetOutflow']:
            assert 'category' in item
            assert 'name' in item['category']
            assert 'name' in item['category']
            assert 'assignedBy' in item
            assert 'quantity' in item
            assert 'dateAssigned' in item
            assert 'assets' in item
            assets = item['assets'][0]
            for asset in assets:
                assert 'createdAt' in assets
                assert 'assigneeType' in assets
                assert 'tag' in assets
                assert 'assignee' in assets
            assignees = assets['assignee']
            for assignee in assignees:
                assert 'id' in assignees
                assert 'name' in assignees
                assert 'spaceType' in assignees
            spaceTypes = assignees['spaceType']
            for spaceType in spaceTypes:
                assert 'id' in spaceTypes
                assert 'color' in spaceTypes
                assert 'type' in spaceTypes

    def test_for_asset_outflow_report_pagination_succeeds(
            self, client, init_db, auth_header):
        """Should succeed when page and limit queries are provided

        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
        """
        response = client.get(
            ASSET_OUTFLOW_URL_WITH_QUERY_AND_DATES.format(
                START_DATE_STRING, END_DATE_STRING),
            headers=auth_header)
        response_data = json.loads(response.data.decode(CHARSET))['data']
        response_meta = json.loads(response.data.decode(CHARSET))['meta']
        assert response.status_code == 200
        assert response_meta['firstPage'].endswith('page=1&limit=10')
        assert (response_meta['nextPage'].endswith('')
                or response_meta['nextPage'].endswith('limit=10'))
        assert response_meta['previousPage'] == ''
        assert response_meta['page'] >= 1
        assert response_meta['pagesCount'] >= 1
        assert response_meta['totalCount'] >= 0
        assert len(response_data) >= 1
        assert len(response_meta) >= 1

    def test_for_asset_outflow_report_with_only_start_date_succeeds(
            self, client, init_db, auth_header):
        """Should succeed when only start query is provided

        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
        """

        response = client.get(
            ASSET_OUTFLOW_URL_WITH_QUERY_AND_START_DATE.format(
                START_DATE_STRING),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = json.loads(response.data)['data']
        assert len(response_data) == 1
        assert response.status_code == 200
        assert response_json['message'] == SUCCESS_MESSAGES[
            'asset_report'].format('assetOutflow')
        assert isinstance(response_data['assetOutflow'], list)
        for item in json.loads(response.data)['data']['assetOutflow']:
            assert 'category' in item
            assert 'name' in item['category']
            assert 'name' in item['category']
            assert 'assignedBy' in item
            assert 'quantity' in item
            assert 'dateAssigned' in item
            assert 'assets' in item
            assets = item['assets'][0]
            for asset in assets:
                assert 'createdAt' in assets
                assert 'assigneeType' in assets
                assert 'tag' in assets
                assert 'assignee' in assets
            assignees = assets['assignee']
            for assignee in assignees:
                assert 'id' in assignees
                assert 'name' in assignees
                assert 'spaceType' in assignees
            spaceTypes = assignees['spaceType']
            for spaceType in spaceTypes:
                assert 'id' in spaceTypes
                assert 'color' in spaceTypes
                assert 'type' in spaceTypes

    def test_for_asset_outflow_report_with_only_end_date_succeeds(
            self, client, init_db, auth_header):
        """Should succeed when only start query is provided

        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
        """

        response = client.get(
            ASSET_OUTFLOW_URL_WITH_QUERY_AND_END_DATE.format(END_DATE_STRING),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = json.loads(response.data)['data']
        assert len(response_data) == 1
        assert response.status_code == 200
        assert response_json['message'] == SUCCESS_MESSAGES[
            'asset_report'].format('assetOutflow')
        assert isinstance(response_data['assetOutflow'], list)
        for item in json.loads(response.data)['data']['assetOutflow']:
            assert 'category' in item
            assert 'name' in item['category']
            assert 'name' in item['category']
            assert 'assignedBy' in item
            assert 'quantity' in item
            assert 'dateAssigned' in item
            assert 'assets' in item
            assets = item['assets'][0]
            for asset in assets:
                assert 'createdAt' in assets
                assert 'assigneeType' in assets
                assert 'tag' in assets
                assert 'assignee' in assets
            assignees = assets['assignee']
            for assignee in assignees:
                assert 'id' in assignees
                assert 'name' in assignees
                assert 'spaceType' in assignees
            spaceTypes = assignees['spaceType']
            for spaceType in spaceTypes:
                assert 'id' in spaceTypes
                assert 'color' in spaceTypes
                assert 'type' in spaceTypes

    def test_for_asset_outflow_report_without_query_string_succeeds(
            self, client, init_db, auth_header):
        """The response data should be all analytics report without query string

        Args:
            init_db (func): Initialize test database
            client (func): Flask test client
            sset_out_flow (func): Saves asset outflow record
            auth_header (func): Authentication token
        """
        response = client.get(ANALYTICS_URL, headers=auth_header)
        response_data = json.loads(response.data.decode(CHARSET))['data']
        assert len(response_data) >= 4
        assert response.status_code == 200
        assert 'assetFlow' in response_data
        assert 'assetInflow' in response_data
        assert 'assetOutflow' in response_data
        assert 'stockLevel' in response_data

    def test_for_asset_outflow_report_with_invalid_end_date_fails(
            self, client, init_db, auth_header):
        """The response data should return a 400 status code when the end_date is greater than  current date

        Args:
            init_db (func): Initialize test database
            client (func): Flask test client
            sset_out_flow (func): Saves asset outflow record
            auth_header (func): Authentication token
        """
        URL = BASE_URL + '/assets/analytics?report=assetOutflow' \
                                        '&endDate={}'
        response = client.get(
            URL.format(date.today() - timedelta(days=2)), headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_end_date']

    def test_for_asset_outflow_report_with_invalid_start_date_fails(
            self, client, init_db, auth_header):
        """The response data should return a 400 status code when the end_date is greater than  current date

        Args:
            init_db (func): Initialize test database
            client (func): Flask test client
            sset_out_flow (func): Saves asset outflow record
            auth_header (func): Authentication token
        """
        response = client.get(
            ASSET_OUTFLOW_URL_WITH_QUERY_AND_START_DATE.format(
                date.today() + timedelta(days=2)),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_start_date']

    def test_for_asset_outflow_report_with_invalid_start_date_and_end_date_fails(
            self, client, init_db, auth_header):
        """The response data should return a 400 status code when the start_date is greater than the end_date

        Args:
            init_db (func): Initialize test database
            client (func): Flask test client
            asset_out_flow (func): Saves asset outflow record
            auth_header (func): Authentication token
        """
        today = datetime.now()
        response = client.get(
            ASSET_OUTFLOW_URL_WITH_QUERY_AND_DATES.format(
                date.today(),
                date.today() - timedelta(days=7)),
            headers=auth_header,
        )
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_date_range']
