"""Module to test attribute resource endpoint"""

from flask import json

from api.models.asset_category import AssetCategory
from api.models.attribute import Attribute
from api.utilities.constants import CHARSET

from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import database_errors

# app config
from config import AppConfig

api_base_url_v1 = AppConfig.API_BASE_URL_V1


class TestAttribute:
    """Attribute endpoint test"""

    def test_get_asset_category_attributes_with_valid_id(
            self, init_db, client, auth_header, new_user):
        """Should return attributes of an asset category"""
        new_user.save()
        asset_category = AssetCategory(name='HD Screen')
        asset_category.save()
        choices = ['red', 'blue']
        attributes = Attribute(
            label='color',
            _key='color',
            is_required=False,
            input_control='text-area',
            choices=','.join(choices),
            asset_category_id=asset_category.id)
        attributes.save()

        response = client.get(
            f'{api_base_url_v1}/asset-categories/{asset_category.id}/'
            f'attributes',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['data']['name'] == 'HD Screen'
        assert type(response_json['data']['customAttributes']) == list
        assert len(response_json['data']['customAttributes']) == 1
        assert response_json['data']['customAttributes'][0]['label'] == 'color'
        assert response_json['data']['customAttributes'][0][
            'inputControl'] == 'text-area'
        assert response_json['data']['customAttributes'][0][
            'choices'] == choices
        assert response_json['data']['customAttributes'][0][
            'isRequired'] == False

    def test_get_asset_category_attributes_with_invalid_id(
            self, init_db, client, auth_header):
        """Should raise an exception for invalid asset category id"""

        response = client.get(
            f'{api_base_url_v1}/asset-categories/@not-valid@/'
            f'attributes',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'Invalid id in parameter'

    def test_get_asset_category_attributes_with_non_exiting_or_deleted_id(
            self, init_db, client, auth_header):
        """Should raise an exception when asset category id is not found"""

        response = client.get(
            f'{api_base_url_v1}/asset-categories/-not-Found/'
            f'attributes',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'Asset category not found'

    def test_get_asset_category_deleted_attributes_succeeds(
                self, init_db, client, request_ctx, mock_request_obj_decoded_token,
                auth_header):
                
        """Should return attributes of an asset category"""

        asset_category = AssetCategory(name='HD Screen')
        asset_category.save()
        choices = ['red', 'blue']
        attributes = Attribute(
            label='color',
            _key='color',
            is_required=False,
            input_control='text-area',
            choices=','.join(choices),
            asset_category_id=asset_category.id)
        attributes.save()

        attributes.delete()

        response = client.get(
            f'{api_base_url_v1}/asset-categories/{asset_category.id}/attributes?include=deleted',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['data']['name'] == 'HD Screen'

    def test_delete_asset_category_attribute_succeeds(self, client, auth_header, init_db):
        """ Tests delete asset category attribute succeeds
    ​
            Args:
                client (object): Fixture to get flask test client.
                auth_header (dict): Fixture to get token.
                init_db (func): Initialises the database.
    ​
            """

        asset_category = AssetCategory(name='HD Screen')
        asset_category.save()
        choices = ['red', 'blue']
        attribute = Attribute(
            label='color',
            _key='color',
            is_required=False,
            input_control='text-area',
            choices=','.join(choices),
            asset_category_id=asset_category.id)
        attribute.save()
        response = client.delete(
            f'{api_base_url_v1}/attributes/{attribute.id}',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['deleted'].format(
            'Attribute')

    def test_delete_asset_category_attribute_with_non_existing_id_fails(self, client, auth_header, init_db):
        """ Tests delete asset category attribute with non existing fails
    ​
        Args:
            client (object): Fixture to get flask test client.
            auth_header (dict): Fixture to get token.
            init_db (object): Initialises the database.
    ​
        """

        response = client.delete(
            f'{api_base_url_v1}/attributes/fkndhinknef4nj',
            headers=auth_header)
            
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == database_errors[
            'non_existing'].format('Attribute') 
