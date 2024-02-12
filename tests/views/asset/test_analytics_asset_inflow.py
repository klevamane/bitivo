import json
import datetime
from dateutil.relativedelta import relativedelta

# Local modules
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.constants import CHARSET
from api.utilities.messages.error_messages import serialization_errors

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1
ASSET_FLOW_URL = BASE_URL + '/assets/analytics?report='

now = datetime.datetime.now()
today = datetime.datetime.today()
two_weeks_from_now = today + relativedelta(weeks=2)
tomorrow = today + relativedelta(days=1)
one_month_before_now = today + relativedelta(months=-1)
asset_start_date = now.strftime("%Y-%m-%d")

end_date = today + relativedelta(days=2)
INVALID_DATE = '2019-11-07-11'
ASSET_INFLOW_URL = ASSET_FLOW_URL + 'assetInflow'
INVALID_END_DATE_ONLY = ASSET_FLOW_URL + 'assetInflow&endDate={}'.format(
    end_date.strftime("%Y-%m-%d"))
VALID_END_DATE = ASSET_FLOW_URL + 'assetInflow&endDate={}'.format(
    today.strftime("%Y-%m-%d"))
INVALID_START_DATE = ASSET_FLOW_URL + 'assetInflow&startDate=2019-11-07-11'
INVALID_END_DATE = ASSET_FLOW_URL + 'assetInflow&endDate={}'.format(
    INVALID_DATE)
END_DATE_LESSER_THAN_START_DATE = ASSET_FLOW_URL + 'assetInflow&endDate={}'\
    .format(one_month_before_now.strftime("%Y-%m-%d"))
start_date_greater_than_end_date = ASSET_FLOW_URL + 'assetInflow&startDate={}'\
    .format(two_weeks_from_now.strftime("%Y-%m-%d"))


class TestAssetInflowSchema:
    """ Test Asset Inflow schema"""

    def asset_inflow_test_success_method(self, response, new_user):
        """Asset inflow test assertion on success.
                   Total number of assets that came into the store

                   Args:
                       response (datetime): response from api endpoint.

                   Returns :
                        None
                   """
        new_user.save()
        response_json = json.loads(response.data.decode(CHARSET))
        data = json.loads(response.data.decode(CHARSET))['data']
        inflow_response = data['assetInflow'][0]
        status = response_json['status']
        asset_in_store = inflow_response['assets'][0]['assignee']
        assert SUCCESS_MESSAGES['asset_report'].format(
            'assetInflow') == response_json['message']
        assert response.status_code == 200
        assert 'message' in response_json
        assert 'status' in response_json
        assert 'assetInflow' in data
        assert 'category' in inflow_response
        assert 'assignedBy' in inflow_response
        assert 'quantity' in inflow_response
        assert 'dateAssigned' in inflow_response
        assert 'name' in asset_in_store
        assert status == 'Success'

    def asset_inflow_test_fails_method(self, response):
        """Asset inflow test assertion on failure.
                           Total number of assets that came into the store

                           Args:
                               response (datetime): response from api endpoint.

                           Returns :
                                None
                           """
        response_json = json.loads(response.data.decode(CHARSET))
        status = response_json['status']
        assert response.status_code == 400
        assert 'message' in response_json
        assert 'status' in response_json
        assert status == 'error'

    def test_asset_inflow_with_no_start_or_end_date_succeeds(
            self, init_db, client, auth_header_two, asset_inflow, new_user):
        """Tests the asset inflow response with no start or end date.

         Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header_two(dict): fixture to get token
            asset_inflow: fixture to get an asset object with assignee_type of store

         Returns:
             None
        """
        response = client.get(ASSET_INFLOW_URL, headers=auth_header_two)
        self.asset_inflow_test_success_method(response, new_user)

    def test_asset_outflow_with_invalid_start_date_fails(
            self, init_db, client, auth_header_two, asset_inflow):
        """Tests the asset inflow response with invalid start date.
             Args:  
                   client(FlaskClient): fixture to get flask test client
                   init_db(SQLAlchemy): fixture to initialize the test database
                   auth_header_two(dict): fixture to get token
                   asset_inflow: fixture to get an asset object with assignee_type of store

             Returns:
                None
        """
        response = client.get(INVALID_START_DATE, headers=auth_header_two)
        self.asset_inflow_test_fails_method(response)

    def test_asset_inflow_with_invalid_end_date_fails(
            self, init_db, client, auth_header_two, asset_inflow):
        """Tests the asset inflow response with invalid end date.
             Args:
                   client(FlaskClient): fixture to get flask test client
                   init_db(SQLAlchemy): fixture to initialize the test database
                   auth_header_two(dict): fixture to get token
                   asset_inflow: fixture to get an asset object with assignee_type of store

             Returns:
                None
        """
        response = client.get(INVALID_END_DATE, headers=auth_header_two)
        response_json = json.loads(response.data.decode(CHARSET))
        assert serialization_errors['invalid_date'].format(
            INVALID_DATE) == response_json['message']
        self.asset_inflow_test_fails_method(response)

    def test_asset_inflow_with_end_date_lesser_than_start_date_fails(
            self, init_db, client, auth_header_two, asset_inflow):
        """Tests the asset inflow response with end date lesser than the start date.
             Args:
                   client(FlaskClient): fixture to get flask test client
                   init_db(SQLAlchemy): fixture to initialize the test database
                   auth_header_two(dict): fixture to get token
                   asset_inflow: fixture to get an asset object with assignee_type of store

             Returns:
                None
               """
        response = client.get(
            END_DATE_LESSER_THAN_START_DATE, headers=auth_header_two)
        self.asset_inflow_test_fails_method(response)

    def test_asset_inflow_with_start_date_greater_than_end_date_fails(
            self, init_db, client, auth_header_two, asset_inflow):
        """Tests the asset inflow response with start date greater than end date .
             Args:
                   client(FlaskClient): fixture to get flask test client
                   init_db(SQLAlchemy): fixture to initialize the test database
                   auth_header_two(dict): fixture to get token
                   asset_inflow: fixture to get an asset object with assignee_type of store

             Returns:
                None
               """
        response = client.get(
            start_date_greater_than_end_date, headers=auth_header_two)
        response_json = json.loads(response.data.decode(CHARSET))
        assert serialization_errors['invalid_start_date'] == response_json[
            'message']
        self.asset_inflow_test_fails_method(response)

    def test_asset_inflow_with_end_date_greater_than_today_fails(
            self, init_db, client, auth_header_two, asset_inflow):
        """Tests the asset inflow response with start date greater than end date .
             Args:
                   client(FlaskClient): fixture to get flask test client
                   init_db(SQLAlchemy): fixture to initialize the test database
                   auth_header_two(dict): fixture to get token
                   asset_inflow: fixture to get an asset object with assignee_type of store

             Returns:
                None
               """
        response = client.get(INVALID_END_DATE_ONLY, headers=auth_header_two)
        response_json = json.loads(response.data.decode(CHARSET))
        assert serialization_errors['invalid_end_date'] == response_json[
            'message']
        self.asset_inflow_test_fails_method(response)

    def test_asset_inflow_with_only_start_date_only_succeeds(
            self, init_db, client, auth_header_two, asset_inflow, new_user):
        """Tests the asset inflow response with no start or end date.
             Args:
                   client(FlaskClient): fixture to get flask test client
                   init_db(SQLAlchemy): fixture to initialize the test database
                   auth_header_two(dict): fixture to get token
                   asset_inflow: fixture to get an asset object with assignee_type of store

             Returns:
                None
               """
        response = client.get(ASSET_INFLOW_URL, headers=auth_header_two)
        self.asset_inflow_test_success_method(response, new_user)

    def test_asset_inflow_with_valid_end_date_only_succeeds(
            self, init_db, client, auth_header_two, asset_inflow, new_user):
        """Tests the asset inflow response with no start or end date.
             Args:
                   client(FlaskClient): fixture to get flask test client
                   init_db(SQLAlchemy): fixture to initialize the test database
                   auth_header_two(dict): fixture to get token
                   asset_inflow: fixture to get an asset object with assignee_type of store

             Returns:
                None
               """
        response = client.get(VALID_END_DATE, headers=auth_header_two)
        self.asset_inflow_test_success_method(response, new_user)
