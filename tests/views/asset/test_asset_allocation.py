"""Tests for asset allocation"""

import json
import datetime as dt
import jwt
from api.models import Asset
from api.models.asset import AssigneeType
from api.utilities.messages.error_messages import serialization_errors
from api.utilities.constants import CHARSET

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1
URL = f'{BASE_URL}/assets'


class TestAssetAllocation:
    @staticmethod
    def assert_bad_request(response, field, error_key, *args):
        """Helper function to assert a 400 Bad request

        Args:
            response (obj): The request response
            field (str): The field containing the error
            error_key (str): The serialization errors dict key
            *args: Additional arguments taken by the error message
        """
        error_msg = json.loads(response.data)['errors'][field][0]
        assert error_msg == serialization_errors[error_key].format(*args)
        assert response.status_code == 400

    def test_asset_allocation_with_valid_assignee_id_and_type_succeeds(
            self, init_db, client, auth_header, save_assignees, asset_details):
        """Should succeed with valid assigneeId and assigneeType

        Args:
            init_db (func):  Initializes the test database
            client (func): Flask test client
            auth_header (func): Authentication token
            asset_details (func): Generate asset details
            save_assignees (func): Save new_user and new_space to the
                database
        """

        # user assignee
        asset_payload = asset_details()
        response = client.post(
            URL, headers=auth_header, data=json.dumps(asset_payload))
        asset_data = json.loads(response.data.decode(CHARSET))['data']
        assert response.status_code == 201
        assert asset_data['tag'] == asset_payload['tag']
        assert asset_data['assigneeType'] == AssigneeType.user.value
        assert 'assignee' in asset_data
        assert asset_data['assignee']['tokenId'] == asset_details(
        )['assigneeId']

        # space assignee
        asset_payload = asset_details('space', tag='new')
        response = client.post(
            URL, headers=auth_header, data=json.dumps(asset_payload))
        asset_data = json.loads(response.data.decode(CHARSET))['data']
        assert response.status_code == 201
        assert 'assignee' in asset_data
        assert asset_data['tag'] == asset_payload['tag']
        assert asset_data['assigneeType'] == AssigneeType.space.value
        assert asset_data['assignee']['id'] == asset_details(
            'space')['assigneeId']

    def test_update_asset_allocation_with_valid_assignee_id_and_type_succeeds(
            self, init_db, client, auth_header, assignee_details, save_assignees,
        new_asset, new_space):
        """Should succeed with valid assigneeId and assigneeType

        Args:
            init_db (func):  Initializes the test database
            client (func): Flask test client
            auth_header (func): Authentication token
            asset_details (func): Generate asset details
            save_assignees (func): Save new_user and new_space to the
                database
        """

        # user assignee
        asset_payload = assignee_details()
        response = client.patch(
            f'{URL}/{new_asset.id}',
            headers=auth_header,
            data=json.dumps(asset_payload))
        asset_data = json.loads(response.data.decode(CHARSET))['data']
        assert response.status_code == 200
        assert asset_data['tag'] == new_asset.tag
        assert 'assignee' in asset_data
        assert asset_data['assigneeType'] == AssigneeType.user.value
        assert asset_data['assignee']['tokenId'] == \
            assignee_details()['assigneeId']

        # space assignee
        asset_payload = assignee_details('space')
        response = client.patch(
            f'{URL}/{new_asset.id}',
            headers=auth_header,
            data=json.dumps(asset_payload))
        asset_data = json.loads(response.data.decode(CHARSET))['data']
        assert response.status_code == 200
        assert asset_data['tag'] == new_asset.tag
        assert 'assignee' in asset_data
        assert asset_data['assigneeType'] == AssigneeType.space.value
        assert asset_data['assignee']['id'] == \
            assignee_details('space')['assigneeId']

    def test_asset_allocation_with_invalid_assignee_id_fails(
            self, init_db, client, auth_header, asset_details):
        """Should fail with a 400 error when the assignee id is invalid

        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            asset_details (func): Generate asset details
        """
        asset_payload = asset_details(assigneeId='-LL%^*&^hb')
        response = client.post(
            URL, headers=auth_header, data=json.dumps(asset_payload))
        self.assert_bad_request(response, 'assigneeId', 'invalid_assignee_id')

    def test_update_asset_allocation_with_invalid_assignee_id_fails(
            self, init_db, client, auth_header, assignee_details, asset_without_attributes):
        """Should fail with a 400 error when the assignee id is invalid

        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            assignee_details (func): Generate assignee details
            asset_without_attributes (func): Generate an asset without
                attributes
        """
        asset_payload = assignee_details(assigneeId='^%^$$^%&%&')
        response = client.patch(
            f'{URL}/{asset_without_attributes.id}',
            headers=auth_header,
            data=json.dumps(asset_payload))
        self.assert_bad_request(
            response, 'assigneeId', 'invalid_assignee_id')
    
    def test_asset_allocation_with_invalid_assignee_type_fails(
            self, init_db,client, auth_header, asset_details):
        """Should fail with a 400 error when the assignee type is invalid

        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            asset_details (func): Generate asset details
        """
        asset_payload = asset_details(assigneeType='invalid')
        response = client.post(
            URL, headers=auth_header, data=json.dumps(asset_payload))
        self.assert_bad_request(response, 'assigneeType',
                                'invalid_assignee_type', 'invalid')

    def test_update_asset_allocation_with_invalid_assignee_type_fails(
            self, init_db, client, auth_header, assignee_details, asset_without_attributes):
        """Should fail with a 400 error when the assignee type is invalid

        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            assignee_details (func): Generate assignee details
            asset_without_attributes (func): Generate an asset without
                attributes
        """
        asset_payload = assignee_details(assigneeType='invalid')
        response = client.patch(
            f'{URL}/{asset_without_attributes.id}',
            headers=auth_header,
            data=json.dumps(asset_payload))
        self.assert_bad_request(response, 'assigneeType',
                                'invalid_assignee_type', 'invalid')

    def test_asset_allocation_with_non_existent_assignee_id_fails(
            self, init_db, client, asset_details, auth_header):
        """Should fail when the assignee id does not exist

        Args:
            client (func): Flask test client
            asset_details (func): Generate asset details
            auth_header (func): Authentication token
        """
        asset_payload = asset_details(assigneeId='nonexistent')
        response = client.post(
            URL, headers=auth_header, data=json.dumps(asset_payload))
        self.assert_bad_request(response, 'assigneeId', 'assignee_not_found')

    def test_update_asset_allocation_with_non_existent_assignee_id_fails(
            self, client, init_db, asset_without_attributes, assignee_details, auth_header):
        """Should fail when the assignee id does not exist

        Args:
            client (func): Flask test client
            asset_without_attributes (func): Generate an asset without
                attributes
            assignee_details (func): Generate assignee details
            auth_header (func): Authentication token
        """
        asset_payload = assignee_details(assigneeId='nonexistent')
        response = client.patch(
            f'{URL}/{asset_without_attributes.id}',
            headers=auth_header,
            data=json.dumps(asset_payload))
        self.assert_bad_request(response, 'assigneeId', 'assignee_not_found')

    def test_allocation_with_non_matching_assignee_id_and_type_fails(
            self, init_db, client, auth_header, asset_details):
        """Should fail if the assignee id does not match the assignee type

        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            asset_details (func): Generate asset details
        """
        asset_payload = asset_details(assigneeType='space')
        response = client.post(
            URL, headers=auth_header, data=json.dumps(asset_payload))
        self.assert_bad_request(response, 'assigneeType',
                                'non_matching_assignee_type')

    def test_update_asset_allocation_with_non_matching_assignee_id_and_type_fails(
            self, init_db,client, auth_header, assignee_details, asset_without_attributes):
        """Should fail if the assignee_id does not match the assignee type

        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            assignee_details (func): Generate assignee details
            asset_without_attributes (func): Generate an asset without
                attributes
        """
        asset_payload = assignee_details(assigneeType='space')
        response = client.patch(
            f'{URL}/{asset_without_attributes.id}',
            headers=auth_header,
            data=json.dumps(asset_payload))
        self.assert_bad_request(response, 'assigneeType',
                                'non_matching_assignee_type')

    def test_asset_allocation_with_assignee_id_or_type_missing_fails(
            self, init_db, client, asset_details, auth_header):
        """Should fail if the assignee id or the assignee type are missing

        Args:
            client (func): Flask test client
            asset_details(func): Generate asset details
            auth_header (func): Authentication token
        """
        asset_payload = asset_details()
        asset_payload.pop('assigneeType')
        response = client.post(
            URL, headers=auth_header, data=json.dumps(asset_payload))
        self.assert_bad_request(response, 'assigneeType', 'field_required')
        asset_payload = asset_details()
        asset_payload.pop('assigneeId')
        response = client.post(
            URL, headers=auth_header, data=json.dumps(asset_payload))
        self.assert_bad_request(response, 'assigneeId', 'field_required')

    def test_update_asset_allocation_with_with_assignee_id_or_type_missing_fails(
            self, init_db, client, asset_without_attributes, new_user, auth_header):
        """Should fail if the assignee id or the assignee type are missing

        Args:
            client (func): Flask test client
            asset_without_attributes (func): Generate an asset without
                attributes
            new_user (func): Generate a new user
            auth_header (func): Authentication token
        """
        asset_details = {'assigneeType': 'space'}
        response = client.patch(
            f'{URL}/{asset_without_attributes.id}',
            headers=auth_header,
            data=json.dumps(asset_details))
        self.assert_bad_request(response, 'assigneeId',
                                'assignee_id_and_type_required')
        asset_details = {'assigneeId': new_user.token_id}
        response = client.patch(
            f'{URL}/{asset_without_attributes.id}',
            headers=auth_header,
            data=json.dumps(asset_details))
        self.assert_bad_request(response, 'assigneeType',
                                'assignee_id_and_type_required')

    def test_asset_allocation_with_space_assignee_not_in_center_fails(
            self, init_db, client, asset_details, save_assignees, test_center_without_users, auth_header):
        """Should fail if a space assignee is not in center id provided

        Args:
            client (func): Flask test client
            test_center_without_users (fixture): generate a center without
                users
            auth_header (func): Authentication token
        """
        asset_payload = asset_details(
            'space', centerId=test_center_without_users.id)
        response = client.post(
            URL, headers=auth_header, data=json.dumps(asset_payload))
        self.assert_bad_request(response, 'assigneeId', 'not_in_center')

    def test_update_asset_allocation_with_space_assignee_not_in_center_fails(
            self, init_db, client, assignee_details, asset_without_attributes,
            test_center_without_users, auth_header, save_assignees):
        """Should fail if space not in the center the asset belongs to

        Args:
            client (func): Flask test client
            asset_without_attributes (func): Generate an asset without
                attributes
            test_center_without_users (fixture): generate a center without
                users
            assignee_details (func):  Generate assignee details
            auth_header (func): Authentication token
        """
        asset_payload = assignee_details(
            'space', centerId=test_center_without_users.id)
        response = client.patch(
            f'{URL}/{asset_without_attributes.id}',
            headers=auth_header,
            data=json.dumps(asset_payload))
        self.assert_bad_request(response, 'assigneeId', 'not_in_center')

    def test_asset_allocation_fails_on_invalid_center_id(
            self, init_db, client, asset_details, auth_header):
        """Should fail if the center_id provided is invalid

        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            asset_details (func): Generate asset details
        """
        asset_payload = asset_details(centerId='&^$&&W(#')
        response = client.post(
            URL, headers=auth_header, data=json.dumps(asset_payload))
        self.assert_bad_request(response, 'centerId', 'invalid_id_field')

    def test_update_asset_allocation_fails_on_invalid_center_id(
            self, init_db, client, assignee_details, asset_without_attributes, auth_header):
        """Should fail if the center_id provided is invalid

        Args:
            client (func): Flask test client
            asset_without_attributes (func): Generate an asset without
                attributes
            auth_header (func): Authentication token
            assignee_details (func): Generate assignee details
        """
        asset_payload = assignee_details(centerId='**&%$&%&')
        response = client.patch(
            f'{URL}/{asset_without_attributes.id}',
            headers=auth_header,
            data=json.dumps(asset_payload))
        self.assert_bad_request(response, 'centerId', 'invalid_id_field')

    def test_asset_allocation_records_assigned_by_and_date_assigned(
            self, init_db, asset_details, auth_header, client, save_assignees):
        """Test that assigned_by and date_assigned are successfully recorded

        Args:
            init_db (func): Initializes the test database
            asset_details (func): Generate asset details
            auth_header (func): Authentication token
            client (func): Flask test client
        """
        asset_payload = asset_details()
        response = client.post(
            URL, headers=auth_header, data=json.dumps(asset_payload))
        asset_data = json.loads(response.data.decode(CHARSET))['data']
        token = str(auth_header['Authorization']).split()[1]
        assigned_by = jwt.decode(token, verify=False)['UserInfo']['name']
        assert asset_data['assignedBy'] == assigned_by
        assert 'dateAssigned' in asset_data
        asset = Asset.get(asset_data['id'])
        assert asset.assigned_by == assigned_by
        assert asset.date_assigned.date() == dt.datetime.now().date()

    def test_update_asset_allocation_records_assigned_by_and_date_assigned(
            self, init_db, assignee_details, auth_header, client,
            asset_without_attributes, new_center, save_assignees):
        """Test that assigned_by and date_assigned are successfully recorded

        Args:
            init_db (func): Initializes the test database
            assignee_details: Generate assignee details
            auth_header (func): Authentication token
            client (func): Flask test client
            asset_without_attributes (func): Generate an asset without
                attributes
            new_center (func): Generate a new center
            save_assignees (func): Save new_user and new_space to the
                database
        """
        asset_payload = assignee_details('space', centerId=new_center.id)
        response = client.patch(
            f'{URL}/{asset_without_attributes.id}',
            headers=auth_header,
            data=json.dumps(asset_payload))
        asset_data = json.loads(response.data.decode(CHARSET))['data']
        token = str(auth_header['Authorization']).split()[1]
        assigned_by = jwt.decode(token, verify=False)['UserInfo']['name']

        assert asset_data['assignedBy'] == assigned_by
        assert 'dateAssigned' in asset_data
        asset = Asset.get(asset_data['id'])
        assert asset.assigned_by == assigned_by

        assert asset.date_assigned.date() == dt.datetime.utcnow().date()
