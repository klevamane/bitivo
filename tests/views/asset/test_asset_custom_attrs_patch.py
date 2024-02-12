"""Module for testing asset custom attributes patch"""
# pylint: skip-file
from flask import json

from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import serialization_errors

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1


class TestAssetPatchEndpointCustomAttributes:
    """Test class for Asset resource custom attributes in PATCH endpoint."""

    def test_patch_asset_with_null_required_custom_attr_returns_400(
            self, client, init_db, auth_header, asset_with_attrs):
        """
        Test PATCH asset with only a required single attribute set to null
        in data fails and returns 400
        """
        data = dict(customAttributes={'warranty': None})
        response = client.patch(
            f'{BASE_URL}/assets/{asset_with_attrs.id}',
            headers=auth_header,
            data=json.dumps(data))
        assert response.status_code == 400
        assert json.loads(response.data)['message'] == serialization_errors[
            'attribute_required'].format('warranty')
        assert asset_with_attrs.custom_attributes['warranty'] != None

    def test_patch_asset_with_valid_required_custom_attr_returns_200(
            self, client, init_db, auth_header, asset_with_attrs):
        """
        Test PATCH asset with only a valid required single attribute
        in data fails and returns 200
        """
        data = dict(customAttributes={'warranty': 'New value'})
        response = client.patch(
            f'{BASE_URL}/assets/{asset_with_attrs.id}',
            headers=auth_header,
            data=json.dumps(data))
        assert response.status_code == 200
        assert json.loads(
            response.data)['message'] == SUCCESS_MESSAGES['edited'].format(
                'Asset')
        assert asset_with_attrs.custom_attributes['warranty'] == data[
            'customAttributes']['warranty']

    def test_patch_asset_with_null_optional_custom_attr_returns_200(
            self, client, init_db, auth_header, asset_with_attrs):
        """
        Test PATCH asset with an optional single custom attribute set to null
        in data succeeds and returns 200
        """
        data = dict(customAttributes={'color': None})
        response = client.patch(
            f'{BASE_URL}/assets/{asset_with_attrs.id}',
            headers=auth_header,
            data=json.dumps(data))
        assert response.status_code == 200
        assert json.loads(
            response.data)['message'] == SUCCESS_MESSAGES['edited'].format(
                'Asset')
        assert 'color' not in asset_with_attrs.custom_attributes

    def test_patch_asset_with_custom_attr_set_to_valid_choice_returns_200(
            self, client, init_db, auth_header, asset_with_attrs):
        """
        Test PATCH asset with a single custom attribute with restricted
        choices set to a valid choice in data succeeds and returns 200
        """
        data = dict(customAttributes={'screen size': 'Yellow'})
        response = client.patch(
            f'{BASE_URL}/assets/{asset_with_attrs.id}',
            headers=auth_header,
            data=json.dumps(data))
        assert response.status_code == 200
        assert json.loads(
            response.data)['message'] == SUCCESS_MESSAGES['edited'].format(
                'Asset')
        assert asset_with_attrs.custom_attributes['screen size'] == 'Yellow'

    def test_patch_asset_with_custom_attr_set_to_invalid_choice_returns_400(
            self, client, init_db, auth_header, asset_with_attrs):
        """
        Test PATCH asset with a single custom attribute with restricted
        choices set to an invalid choice in data succeeds and returns 400
        """
        data = dict(customAttributes={'screen size': 'Pink'})
        response = client.patch(
            f'{BASE_URL}/assets/{asset_with_attrs.id}',
            headers=auth_header,
            data=json.dumps(data))
        assert response.status_code == 400
        assert json.loads(
            response.data
        )['message'] == serialization_errors['invalid_choice'].format(
            'screen size', 'Yellow,Purple')
        assert asset_with_attrs.custom_attributes['screen size'] == 'Red'

    def test_patch_asset_with_custom_attr_with_an_invalid_attribute_fails(
            self, client, init_db, auth_header, asset_with_attrs):
        """Test for when an invalid attribute is provided

            Should raise a 400 error with an error message when
            an invalid attribute is provided

            Args:
                self (class):  Instance of this class
                client (func): Flask test client
                auth_header (func): Authentication token
                asset_with_attrs (Asset): an Asset that is in the db

            Returns:
                None
        """

        unknown_attribute = 'unknownAttribute'
        data = dict(customAttributes={'unknownAttribute': 'Pink'})
        response = client.patch(
            f'{BASE_URL}/assets/{asset_with_attrs.id}',
            headers=auth_header,
            data=json.dumps(data))
        assert response.status_code == 400
        assert json.loads(response.data)['message'] == serialization_errors[
            'unrelated_attribute'].format(unknown_attribute)
        assert json.loads(response.data)['status'] == 'error'
