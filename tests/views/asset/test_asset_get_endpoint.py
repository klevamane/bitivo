"""Module for asset resource get endpoint."""
from flask import json

from api.utilities.constants import CHARSET
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import (serialization_errors,
                                                   jwt_errors)

# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestAssetGetEndpoint:
    """Class for Asset resource GET endpoint."""

    def test_get_asset_with_valid_asset_id_should_succeed(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            asset_with_attrs):
        """
        Should return a 200 status code and a success message if
        a valid asset id is provided

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            asset_with_attrs(BaseModel): fixture for creating an asset
        """

        asset = asset_with_attrs.save()
        response = client.get(
            f'{API_BASE_URL_V1}/assets/{asset.id}', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        asset_data = response_json['data']

        assert asset_data['id'] == asset.id
        assert asset_data['tag'] == asset.tag
        assert asset_data['centerId'] == asset.center_id
        assert asset_data['status'] == asset.status
        assert asset_data['assetCategoryId'] == asset.asset_category_id
        assert asset_data['customAttributes'] == asset.custom_attributes

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == \
            SUCCESS_MESSAGES['fetched'].format('Asset')

    def test_get_asset_with_invalid_asset_id_should_fail(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header):
        """
        Should return a 400 status code and an error message if an invalid
        asset id is provided

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            asset_with_attrs (BaseModel): fixture for creating an asset
        """

        response = client.get(
            f'{API_BASE_URL_V1}/assets/-LM3$u$2p$^o&C@#', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors['invalid_id']

    def test_get_asset_with_nonexistent_asset_id_should_fail(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header):
        """
        Should return a 404 status code and an error message if the
        asset id provided does not exist

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """

        response = client.get(
            f'{API_BASE_URL_V1}/assets/-LM3u2poCwe4jyQ0UbPN',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'not_found'].format('Asset')

    def test_get_asset_with_no_token_should_fail(  #pylint: disable=C0103
            self,
            client,
            init_db  #pylint: disable=W0613
    ):
        """
        Should return a 401 status code and an error message if authorization
        token is not provided in the request header

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """

        response = client.get(f'{API_BASE_URL_V1}/assets/-LM3u2poCwe4jyQ0UbPN')
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_get_sorted_assets_with_json_column_should_succeed(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            asset_with_attrs):
        """
        Test sorting assets with a json(datatype) column

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            asset_with_attrs(BaseModel): fixture for creating an asset
        """

        asset_with_attrs.save()

        response = client.get(
            f'{API_BASE_URL_V1}/assets?sort=customAttributes',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert isinstance(response_json['data'][0]['customAttributes'], dict)

    def test_get_deleted_assets_with_params(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            asset_with_attrs):
        """
        Should return a 200 status code and a success message if
        a valid asset id is provided

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            asset_with_attrs(BaseModel): fixture for creating an asset
        """

        asset_ = asset_with_attrs.save()
        res = client.delete(
            f'{API_BASE_URL_V1}/assets/{asset_.id}', headers=auth_header)
        response = client.get(
            f'{API_BASE_URL_V1}/assets?include=deleted', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        asset_data = response_json['data']

        for asset in asset_data:
            assert asset['assignee']['name'] == asset_.assignee.name
            assert asset['assignee']['email'] == asset_.assignee.email
            assert asset['assignee']['role'][
                'description'] == asset_.assignee.role.description
            assert asset['deleted'] is True or not asset['deleted']
            assert isinstance(asset['tag'], str)
            assert isinstance(asset['tag'], str)
            assert isinstance(asset['centerId'], str)
            assert isinstance(asset['status'], str)
            assert isinstance(asset['assetCategoryId'], str)
            assert isinstance(asset['customAttributes'], dict)
