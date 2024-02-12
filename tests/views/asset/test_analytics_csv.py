"""Tests for analytics report csv export"""

# Standard Library
import json
from datetime import date
import datetime as dt
from dateutil.relativedelta import *

# Local Module
from api.utilities.messages.error_messages import serialization_errors, jwt_errors
from api.utilities.constants import CHARSET, ASSET_REPORT_QUERIES, MIMETYPE, MIMETYPE_CSV
from api.models.asset_category import AssetCategory
from api.models.asset import Asset
from api.views.asset_analytics_csv import ExportAssetAnalyticsReportResource
from api.utilities.messages.error_messages import serialization_errors

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1
analytics_url = BASE_URL + '/assets/analytics/export?report={}'
inflow_url = analytics_url.format('assetinflow')
stock_level_url = analytics_url.format('stocklevel')

start_date = '2018-01-11'
end_date = '2019-09-29'


class TestExportAnalyticReportResource:
    """Test for exporting analytics in csv format"""

    def test_asset_analytics_export_should_error_with_invalid_token(
            self, client):
        """Tests that client request has no token

        Args:
            client (func): Flask test client

        Returns:
            None

        """
        response = client.get(analytics_url.format('assetFlow'))
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_asset_outflow_method_is_called(self, client, init_db,
                                            auth_header_two, new_user):
        """Tests that asset outflow method should be called

        Args:
            client (func): Flask test client
            auth_header_two (func): Authentication token

        Returns:
            None

        """
        new_user.save()
        response = client.get(
            analytics_url.format('assetOutflow'),
            headers=auth_header_two,
        )

        assert response.status_code == 200

    def test_stock_level_method_is_called(self, client, auth_header_two,
                                          init_db):
        """Tests that stock level method should be called

        Args:
            client (func): Flask test client
            auth_header_two (func): Authentication token

        Returns:
            None

        """

        response = client.get(
            analytics_url.format('stockLevel'),
            headers=auth_header_two,
        )

        assert response.status_code == 200

    def test_non_matching_query_value(self, client, auth_header_two):
        """Tests that wrong query value is passed

        Args:
            client (func): Flask test client
            auth_header_two (func): Authentication token

        Returns:
            None

        """

        response = client.get(
            analytics_url.format('stock'),
            headers=auth_header_two,
        )

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json[
            'message'] == serialization_errors['invalid_request_param'].format(
                'report query', ', '.join(ASSET_REPORT_QUERIES))

    def test_export_assetflows_as_csv_with_invalid_date_params_fails(
            self, init_db, client, auth_header_two):  # pylint: disable=W0613
        """Should return error for invalid date params

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header_two (dict): fixture to get token

        """

        response = client.get(
            analytics_url.format('assetflow') +
            '&endDate=201-2-4&startDate=201-2-1',
            headers=auth_header_two  # noqa
        )
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_date'].format('201-2-1')

    def test_export_asset_flows_with_start_date_greater_end_date_fails(
            self, init_db, client, auth_header_two):  # pylint: disable=W0613
        """Should return error for invalid date params

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header_two (dict): fixture to get token

        """

        response = client.get(
            analytics_url.format('assetflow') +
            '&startDate=2018-11-04&endDate=2018-11-01',
            headers=auth_header_two  # noqa
        )
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_date_range']

    def test_for_when_no_report_parameter_is_passed(self, client,
                                                    auth_header_two):
        """Tests for when no query parameter is passed

        Args:
            client (func): Flask test client
            auth_header_two (func): Authentication token

        Returns:
            None

        """

        response = client.get(
            analytics_url.format(''),
            headers=auth_header_two,
        )

        assert response.status_code == 200

    def test_export_asset_inflow_as_csv_succeed(
            self, init_db, client, auth_header_two, new_space_store):  # pylint: disable=W0613
        """Should return csv data file with asset inflow report"""

        new_space_store.save()
        asset_category = AssetCategory(name='Mac').save()
        date_assigned = '2018-11-03 00:00:00'
        asset = Asset(
            tag=f'AND/11/LAP',
            asset_category_id=asset_category.id,
            assignee_id=new_space_store.id,
            assignee_type='store',
            assigned_by='Mapopo',
            center_id=new_space_store.center_id,
            date_assigned='2018-11-03 00:00:00')
        asset.save()

        response = client.get(
            f'{inflow_url}&startDate={start_date}&endDate={end_date}',  # noqa
            headers=auth_header_two)

        assert response.status_code == 200
        assert response.headers['Content-Type'] == MIMETYPE_CSV
        assert b'Tag,Category,Store,Center,Assigned By,Date Assigned\r\nAND/11/LAP,Mac,ET Store,Lagos,Ayo,2018-11-03\r\n' \
               in response.data

    def test_export_asset_inflow_as_csv_with_no_date_succeed(
            self, init_db, client, auth_header_two):  # pylint: disable=W0613
        """Should return all asset inflow data in csv format when not date filter is specified"""

        response = client.get(
            inflow_url,  # noqa
            headers=auth_header_two)

        assert response.status_code == 200
        assert response.headers['Content-Type'] == MIMETYPE_CSV
        assert b'Tag,Category,Store,Center,Assigned By,Date Assigned\r\nAND/11/LAP,Mac,ET Store,Lagos,Ayo,2018-11-03\r\n' \
               in response.data

    def test_export_asset_inflow_with_inflow_in_date_range_succeed(
            self, init_db, client, auth_header_two):  # pylint: disable=W0613
        """Should export report with an empty content
        if specified date does not contain data"""

        response = client.get(
            f'{inflow_url}&startDate=2000-06-11&endDate=2000-09-30',  # noqa
            headers=auth_header_two)

        assert response.status_code == 200
        assert response.headers['Content-Type'] == MIMETYPE_CSV
        assert response.data == b''

    def test_export_asset_inflow_with_invalid_date_format_fails(
            self, init_db, client, auth_header_two):  # pylint: disable=W0613
        """Should return status code 400 with error message when date format is not valid"""

        response = client.get(
            f'{inflow_url}&startDate=20-9-9&endDate={start_date}',  # noqa
            headers=auth_header_two)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response.headers['Content-Type'] == MIMETYPE
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_date'].format('20-9-9')

    def test_export_asset_inflow_if_start_date_greater_than_end_date_fails(
            self, init_db, client, auth_header_two):  # pylint: disable=W0613
        """Should return status code 400 with error message if start date > end_date"""

        response = client.get(
            f'{inflow_url}&startDate={end_date}&endDate={start_date}',  # noqa
            headers=auth_header_two)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response.headers['Content-Type'] == MIMETYPE
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_date_range']

    def test_export_asset_flows_without_date_query_should_suceed(
            self, init_db, client, auth_header_two, asset_flows_data):  # pylint: disable=W0613
        """Should return csv data file with assetflow information

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header_two (dict): fixture to get token

        """

        inflow, outflow = asset_flows_data
        inflow.save()
        outflow.save()
        response = client.get(
            analytics_url.format('assetflow'), headers=auth_header_two)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/csv'
        assert b'Asset Inflow,Asset Outflow,Asset category requiring reconciliation\r\n2,1,1\r\n' \
               in response.data

    def test_export_asset_flows_as_csv_succeed(
            self, init_db, client, auth_header_two, asset_flows_data):  # pylint: disable=W0613
        """Should return csv data file with assetflow information

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header_two (dict): fixture to get token

        """

        inflow, outflow = asset_flows_data
        inflow.save()
        outflow.save()
        response = client.get(
            analytics_url.format('assetflow') +
            '&startDate=2018-11-01&endDate=2018-11-10',  # noqa
            headers=auth_header_two)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/csv'
        assert b'Asset Inflow,Asset Outflow,Asset category requiring reconciliation\r\n2,1,0\r\n' \
               in response.data

    def test_asset_outflow_method_returns_csv_succeed(
            self,
            client,
            auth_header_two,
    ):  # pylint: disable=W0613
        """Tests that asset outflow method should be called

        Args:
            client (func): Flask test client
            auth_header_two (func): Authentication token
            asset_for_analytics_export (func): pytest fixture

        Returns:
            None

        """

        response = client.get(
            analytics_url.format('assetOutflow') +
            f'&startDate={start_date}&endDate={end_date}',
            headers=auth_header_two,
        )

        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/csv'
        assert b'Tag,Category,Assignee,Center,Assigned By,Date Assigned\r\nAND/13/LAP,MacBook Pro,Ayo,Lagos,Ayo,2018-11-09\r\n' \
               in response.data

    def test_asset_outflow_method_returns_csv_without_date_range(
            self,
            client,
            auth_header_two,
    ):  # pylint: disable=W0613
        """Tests that asset outflow method should work without dates

        Args:
            client (func): Flask test client
            auth_header_two (func): Authentication token
            asset_for_analytics_export (func): pytest fixture

        Returns:
            None

        """

        response = client.get(
            analytics_url.format('assetOutflow'),
            headers=auth_header_two,
        )

        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/csv'
        assert b'Tag,Category,Assignee,Center,Assigned By,Date Assigned\r\nAND/13/LAP,MacBook Pro,Ayo,Lagos,Ayo,2018-11-09\r\n' \
               in response.data

    def test_asset_outflow_method_returns_csv_with_start_date(
            self,
            client,
            auth_header_two,
    ):  # pylint: disable=W0613
        """Tests that asset outflow method should work with start date

        Args:
            client (func): Flask test client
            auth_header_two (func): Authentication token
            asset_for_analytics_export (func): pytest fixture

        Returns:
            None

        """

        response = client.get(
            analytics_url.format('assetOutflow') + f'&startDate={start_date}',
            headers=auth_header_two,
        )

        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/csv'
        assert b'Tag,Category,Assignee,Center,Assigned By,Date Assigned\r\nAND/13/LAP,MacBook Pro,Ayo,Lagos,Ayo,2018-11-09\r\n' \
               in response.data

    def test_asset_outflow_method_works_with_only_end_date(
            self, client, auth_header_two):
        """Tests that asset outflow method should work with only end date

        Args:
            client (func): Flask test client
            auth_header_two (func): Authentication token
            asset_for_analytics_export (func): pytest fixture

        Returns:
            None

        """

        response = client.get(
            analytics_url.format('assetOutflow') + f'&endDate={date.today()}',
            headers=auth_header_two,
        )

        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/csv'

    def test_export_asset_stock_level_if_start_date_greater_than_end_date_fails(
            self, init_db, client, auth_header_two):  # pylint: disable=W0613
        """Test stock level when start date is greater than end date

        Should return status code 400 with error message if start date > end_date

        Args:
            client (func): Flask test client.
            init_db (func): Initialises the database.
            auth_header_two (func): Authentication token.

        Returns:
            None
        """

        response = client.get(
            f'{stock_level_url}&startDate={end_date}&endDate={start_date}',  # noqa
            headers=auth_header_two)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response.headers['Content-Type'] == 'application/json'
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_date_range']

    def test_export_asset_stock_level_as_csv_succeed(
            self, init_db, client, auth_header_two, new_stock_count):  # pylint: disable=W0613
        """Test stock level when export csv succeed

        Should return csv data file with stock level report.

        Args:
            client (func): Flask test client.
            init_db (func): Initialises the database.
            auth_header_two (func): Authentication token.
            new_stock_count (object): fixture for a new stock count.

        Returns:
            None
        """
        new_stock_count.save()
        response = client.get(
            f'{stock_level_url}&startDate={start_date}&endDate={end_date}',  # noqa
            headers=auth_header_two)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == MIMETYPE_CSV
        assert b'Name,Stock Count,Running Low,Low In Stock\r\nLaptop,10,0,0\r\nMacBook Pro,1,0,0\r\nMac,0,0,0\r\n' \
               in response.data

    def test_export_asset_outflow_analytics_in_desc_order_succeed(
            self, init_db, asset_out_flow):
        """Test Export Asset analytics  returns in desc order by date

        Should return assetoutlow in order of date created(current date)

         Args:
            init_db (func): Initialises the database.
            asset_out_flow (object): fixture for a asset outflow

        Returns:
            None

        """
        now = dt.datetime.now().date()
        outflow_start_date = dt.datetime.now() - relativedelta(months=2)

        e = ExportAssetAnalyticsReportResource()
        outflow = e.asset_outflow(outflow_start_date, now)

        first_date_assigned = outflow[0]['Date Assigned']
        second_date_assigned = outflow[1]['Date Assigned']

        assert first_date_assigned > second_date_assigned

    def test_export_asset_inflow_analytics_in_desc_order_succeed(
            self, init_db, asset_inflow_list):
        """Test Export Asset analytics  returns in desc order by date

        Should return assetInflow in order of date created(current date)

         Args:
            init_db (func): Initialises the database.
            asset_inflow_list (object): fixture for a new asset_in_flow

        Returns:
            None

        """
        now = dt.datetime.now().date()
        inflow_start_date = dt.datetime.now() - relativedelta(months=2)

        e = ExportAssetAnalyticsReportResource()
        inflow = e.asset_inflow(inflow_start_date, now)

        first_date_assigned = inflow[0]['Date Assigned']
        second_date_assigned = inflow[1]['Date Assigned']

        assert first_date_assigned > second_date_assigned
