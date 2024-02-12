"""Module for testing updating an asset insurance policy"""
from flask import json
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import serialization_errors, jwt_errors
from api.utilities.constants import CHARSET
from tests.mocks.asset_insurance import UPDATE_ASSET_INSURANCE_POLICY, \
    UPDATE_ASSET_INSURANCE_POLICY_WITH_INVALID_START_DATE, \
    UPDATE_ASSET_INSURANCE_POLICY_WITH_INVALID_END_DATE, \
    UPDATE_ASSET_INSURANCE_POLICY_WITH_START_DATE_PAST_END_DATE
import copy

# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestUpdateAssetInsurancePolicy:
    """Class for testing the update asset insurance policy."""

    def test_update_asset_insurance_policy_succeeds(
            self, auth_header, client, new_asset_insurance, new_user):
        """
        Tests successfully updating an asset insurance policy
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            new_asset_insurance: Fixture to update an asset insurance policy
         Returns:
            None
        """
        new_user.save()
        new_asset_insurance.save()
        new_user.save()
        asset_insurance_id = new_asset_insurance.id
        update_data = UPDATE_ASSET_INSURANCE_POLICY
        data = json.dumps(update_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/insurance/{asset_insurance_id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert isinstance(response_json['data'], dict)
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['edited'].format(
            'Asset insurance policy')

    def test_update_asset_insurance_policy_succeeds_with_initial_start_date(
            self, auth_header, client, new_asset_insurance):
        """
        Tests successfully updating an asset insurance policy
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            new_asset_insurance: Fixture to update an asset insurance policy
         Returns:
            None
        """
        new_asset_insurance.save()
        asset_insurance_id = new_asset_insurance.id
        update_data = UPDATE_ASSET_INSURANCE_POLICY
        update_data = copy.deepcopy(update_data)
        del update_data["startDate"]
        data = json.dumps(update_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/insurance/{asset_insurance_id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert isinstance(response_json['data'], dict)
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['edited'].format(
            'Asset insurance policy')

    def test_update_asset_insurance_policy_succeeds_with_initial_end_date(
            self, auth_header, client, new_asset_insurance):
        """
        Tests successfully updating an asset insurance policy
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            new_asset_insurance: Fixture to update an asset insurance policy
         Returns:
            None
        """
        new_asset_insurance.save()
        asset_insurance_id = new_asset_insurance.id
        update_request_body = UPDATE_ASSET_INSURANCE_POLICY
        update_request_body = copy.deepcopy(update_request_body)
        del update_request_body["endDate"]
        data = json.dumps(update_request_body)
        response = client.patch(
            f'{API_BASE_URL_V1}/insurance/{asset_insurance_id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert isinstance(response_json['data'], dict)
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['edited'].format(
            'Asset insurance policy')

    def test_update_asset_insurance_policy_invalid_insurance_id_fails(
            self, auth_header, client, new_asset_insurance):
        """
        Tests failure to update an asset insurance policy with an invalid insurance id
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            new_asset_insurance: Fixture to create an asset insurance policy
         Returns:
            None
        """
        new_asset_insurance.save()
        insurance_id = new_asset_insurance.id + '@sdsdsdsd'
        update_data = UPDATE_ASSET_INSURANCE_POLICY
        data = json.dumps(update_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/insurance/{insurance_id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert isinstance(response_json, dict)
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors['invalid_id']

    def test_update_asset_insurance_policy_with_no_token_fails(
            self, client, new_asset_insurance):
        """
        Tests updating an asset insurance policy without an authentication token
        Args:
            client (func): Flask test client
            new_asset_insurance: Fixture to create an asset insurance policy
         Returns:
            None
        """
        new_asset_insurance.save()
        insurance_id = new_asset_insurance.id
        update_data = UPDATE_ASSET_INSURANCE_POLICY
        data = json.dumps(update_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/insurance/{insurance_id}',
            headers=None,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_update_non_existent_asset_insurance_policy_fails(
            self, auth_header, client, new_asset_insurance):
        """
        Tests updating an asset insurance policy that does not exist
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            new_asset_insurance: Fixture to create an asset insurance policy
         Returns:
            None
        """
        new_asset_insurance.save()
        insurance_id = new_asset_insurance.id + 'qwqsas'
        update_data = UPDATE_ASSET_INSURANCE_POLICY
        data = json.dumps(update_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/insurance/{insurance_id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert isinstance(response_json, dict)
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'not_found'].format('Asset insurance')

    def test_update_fails_if_start_date_is_invalid(self, auth_header, client,
                                                   new_asset_insurance):
        """
        Tests updating an asset insurance policy failure if start date is invalid
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            new_asset_insurance: Fixture to create an asset insurance policy
         Returns:
            None
        """
        new_asset_insurance.save()
        insurance_id = new_asset_insurance.id
        update_data = UPDATE_ASSET_INSURANCE_POLICY_WITH_INVALID_START_DATE
        data = json.dumps(update_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/insurance/{insurance_id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert isinstance(response_json, dict)
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_date'].format(update_data['startDate'])

    def test_update_fails_if_end_date_is_invalid(self, auth_header, client,
                                                 new_asset_insurance):
        """
        Tests updating an asset insurance policy failure if end date is invalid
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            new_asset_insurance: Fixture to create an asset insurance policy
         Returns:
            None
        """
        new_asset_insurance.save()
        insurance_id = new_asset_insurance.id
        update_data = UPDATE_ASSET_INSURANCE_POLICY_WITH_INVALID_END_DATE
        data = json.dumps(update_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/insurance/{insurance_id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert isinstance(response_json, dict)
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_date'].format(update_data['endDate'])

    def test_update_fails_if_start_date_is_past_end_date(
            self, auth_header, client, new_asset_insurance):
        """
        Tests updating an asset insurance policy failure if start date is past end date
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            new_asset_insurance: Fixture to create an asset insurance policy
         Returns:
            None
        """
        new_asset_insurance.save()
        insurance_id = new_asset_insurance.id
        update_data = UPDATE_ASSET_INSURANCE_POLICY_WITH_START_DATE_PAST_END_DATE
        data = json.dumps(update_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/insurance/{insurance_id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert isinstance(response_json, dict)
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_date_range'].format(update_data['startDate'])
