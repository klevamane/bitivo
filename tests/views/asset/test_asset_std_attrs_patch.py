"""Module for asset patch endpoint."""
# pylint: skip-file
from flask import json

from api.utilities.helpers.random_string_gen import gen_string
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import jwt_errors
from api.utilities.messages.error_messages import serialization_errors

from tests.mocks.asset import ASSET_INVALID_CATEGORY_ID

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1


class TestAssetPatchEndpointWithStandardAttributes:
    """Test class for Asset resource standard attributes in PATCH endpoint."""

    def test_patch_asset_with_no_auth_token_returns_401(
            self, client, init_db, asset_without_attributes):
        """
        Test PATCH tag only on an asset with no auth token in request header
        fails and returns 401
        """
        data = dict(tag=gen_string())
        response = client.patch(
            f'{BASE_URL}/assets/{asset_without_attributes.id}',
            data=json.dumps(data))
        assert response.status_code == 401
        assert json.loads(
            response.data)['message'] == jwt_errors['NO_TOKEN_MSG']
        assert asset_without_attributes.tag != data['tag']

    def test_patch_asset_with_correct_tag_only_returns_200(
            self, client, init_db, auth_header, asset_without_attributes):
        """
        Test PATCH asset with only a correct tag in data succeeds and
        returns 200
        """
        data = dict(tag=gen_string())
        response = client.patch(
            f'{BASE_URL}/assets/{asset_without_attributes.id}',
            headers=auth_header,
            data=json.dumps(data))
        assert response.status_code == 200
        assert json.loads(
            response.data)['message'] == SUCCESS_MESSAGES['edited'].format(
                'Asset')
        assert asset_without_attributes.tag == data['tag']

    def test_patch_asset_with_only_null_tag_returns_400(
            self, client, init_db, auth_header, asset_without_attributes):
        """
        Test PATCH asset with only a null tag in data fails and returns 400
        """
        data = dict(tag=None)
        response = client.patch(
            f'{BASE_URL}/assets/{asset_without_attributes.id}',
            headers=auth_header,
            data=json.dumps(data))
        assert response.status_code == 400
        assert json.loads(response.data)['message'] == 'An error occurred'
        assert asset_without_attributes.tag != None

    def test_patch_asset_with_duplicate_tag_returns_400(
            self, client, init_db, auth_header, asset_without_attributes, asset_with_attrs):
        """
        Test PATCH asset with only a null tag in data fails and returns 400
        """
        data = dict(tag=asset_with_attrs.tag)
        response = client.patch(
            f'{BASE_URL}/assets/{asset_without_attributes.id}',
            headers=auth_header, data=json.dumps(data))
        response_data = json.loads(response.data)
        assert response.status_code == 400
        assert response_data['message'] == 'An error occurred'
        assert response_data['errors']['tag'][0] == serialization_errors['duplicate_asset'].format(
            asset_with_attrs.tag)

    def test_patch_asset_with_only_null_asset_category_returns_400(
            self, client, init_db, auth_header, asset_without_attributes):
        """
        Test PATCH asset with only a null asset category in data fails
        and returns 400
        """
        data = dict(assetCategoryId=None)
        response = client.patch(
            f'{BASE_URL}/assets/{asset_without_attributes.id}',
            headers=auth_header,
            data=json.dumps(data))
        assert response.status_code == 400
        assert json.loads(response.data)['message'] == 'An error occurred'
        assert asset_without_attributes.asset_category_id != None

    def test_patch_asset_with_only_nonexistent_asset_category_id_returns_400(
            self, client, init_db, auth_header, asset_without_attributes):
        """
        Test PATCH asset with only a nonexistent asset category id in data
        fails and returns a 400
        """
        data = dict(assetCategoryId=gen_string())
        response = client.patch(
            f'{BASE_URL}/assets/{asset_without_attributes.id}',
            headers=auth_header,
            data=json.dumps(data))
        assert response.status_code == 400
        assert json.loads(response.data)['message'] == 'An error occurred'
        assert asset_without_attributes.asset_category_id != data[
            'assetCategoryId']

    def test_patch_asset_with_only_existing_asset_category_id_returns_200(
            self, client, init_db, auth_header, asset_without_attributes,
            new_asset_category):
        """
        Test PATCH asset with only an existing asset category in data
        succeeds and returns 200
        """
        new_asset_category.save()
        data = dict(assetCategoryId=new_asset_category.id)
        response = client.patch(
            f'{BASE_URL}/assets/{asset_without_attributes.id}',
            headers=auth_header,
            data=json.dumps(data))
        assert response.status_code == 200
        assert json.loads(
            response.data)['message'] == SUCCESS_MESSAGES['edited'].format(
                'Asset')
        assert asset_without_attributes.asset_category_id == data[
            'assetCategoryId']

    def test_patch_asset_with_only_null_center_id_returns_200(
            self, client, init_db, auth_header, asset_without_attributes):
        """
        Test PATCH asset with only a null center id in data succeeds and
        returns 200
        """
        data = dict(centerId=None)
        response = client.patch(
            f'{BASE_URL}/assets/{asset_without_attributes.id}',
            headers=auth_header,
            data=json.dumps(data))
        assert response.status_code == 200
        assert json.loads(
            response.data)['message'] == SUCCESS_MESSAGES['edited'].format(
                'Asset')
        assert asset_without_attributes.center_id is None

    def test_patch_asset_with_nonexistent_center_id_returns_400(
            self, client, init_db, auth_header, asset_without_attributes):
        """
        Test PATCH asset with only a nonexistent center id fails
        and returns 400
        """
        data = dict(centerId=gen_string())
        response = client.patch(
            f'{BASE_URL}/assets/{asset_without_attributes.id}',
            headers=auth_header,
            data=json.dumps(data))
        assert response.status_code == 400
        assert json.loads(response.data)['message'] == 'An error occurred'
        assert asset_without_attributes.asset_category_id != data['centerId']

    def test_patch_asset_with_only_valid_center_id_returns_200(
            self, client, init_db, auth_header, asset_without_attributes,
            test_center_without_users):
        """
        Test PATCH asset with only a valid center id succeeds and returns 200
        """
        data = dict(centerId=test_center_without_users.id)
        response = client.patch(
            f'{BASE_URL}/assets/{asset_without_attributes.id}',
            headers=auth_header,
            data=json.dumps(data))
        assert response.status_code == 200
        assert json.loads(
            response.data)['message'] == SUCCESS_MESSAGES['edited'].format(
                'Asset')
        assert asset_without_attributes.center_id == data['centerId']

    def test_patch_asset_with_valid_new_std_attributes_returns_200(
            self, client, init_db, auth_header, asset_without_attributes,
            test_center_without_users, new_asset_category):
        """
        Test PATCH asset with valid new standard attributes succeeds
        and returns 200
        """
        new_asset_category.save()
        data = dict(
            centerId=test_center_without_users.id,
            assetCategoryId=new_asset_category.id,
            tag=gen_string())
        response = client.patch(
            f'{BASE_URL}/assets/{asset_without_attributes.id}',
            headers=auth_header,
            data=json.dumps(data))
        assert response.status_code == 200
        assert json.loads(
            response.data)['message'] == SUCCESS_MESSAGES['edited'].format(
                'Asset')
        assert asset_without_attributes.center_id == data['centerId']
        assert asset_without_attributes.asset_category_id == data[
            'assetCategoryId']
        assert asset_without_attributes.tag == data['tag']

    def test_patch_asset_with_invalid_category_id_fails(
            self, client, init_db, auth_header, asset_without_attributes):
        """Test PATCH asset with invalid category id fails

        Should return a 400 response code

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            asset_without_attributes: fixture to get a test asset without attributes

        Returns:
            None
        """
        data = ASSET_INVALID_CATEGORY_ID
        response = client.patch(
            f'{BASE_URL}/assets/{asset_without_attributes.id}',
            headers=auth_header,
            data=json.dumps(data))

        assert response.status_code == 400
        assert json.loads(
            response.data
        )['errors']['assetCategoryId'][0] == serialization_errors['invalid_id']

    def test_patch_asset_with_empty_tag_fails(self, client, init_db,
                                              auth_header, asset_with_attrs):
        """Test PATCH asset with an empty tag fails

        Should return a 400 response code

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            asset_with_attrs: fixture to get a test asset with attributes

        Returns:
            None
        """
        data = dict(tag='')
        response = client.patch(
            f'{BASE_URL}/assets/{asset_with_attrs.id}',
            headers=auth_header,
            data=json.dumps(data))

        assert response.status_code == 400
        assert json.loads(
            response.data
        )['errors']['tag'][0] == serialization_errors['field_required']
