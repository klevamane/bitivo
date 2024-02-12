# Flask
from flask import json

# app config
from config import AppConfig

# Utilities
from api.utilities.constants import CHARSET
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import (serialization_errors,
                                                   jwt_errors)

api_v1_base_url = AppConfig.API_BASE_URL_V1

work_order_query_text = 'fuel'
asset_tag_query_text = 'AND/345/EWRD'


class TestSearchEndpoint:
    """ Class for search GET endpoint."""

    def test_get_search_unauthorized(self, client, init_db, asset_with_attrs):
        """
        Should return jwt error when token is not provided

        Args:
            client (object): Fixture to get flask test client
            init_db (object): Fixture for initializing test database
            new_search(object): Fixture for creating a new asset insurance
        """
        asset = asset_with_attrs.save()
        response = client.get(
            f'{api_v1_base_url}/search?q={asset_tag_query_text}')

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json["status"] == "error"
        assert response_json["message"] == jwt_errors['NO_TOKEN_MSG']

    def test_search_endpoint_with_valid_params_succeeds(
            self, init_db, client, auth_header,
            new_work_order):
        """Tests when request is valid.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_work_order: fixture that contains the work order

        """
        new_work_order.save()
        response = client.get(
            f'{api_v1_base_url}/search?q={work_order_query_text}',
            headers=auth_header)
        response_data = json.loads(response.data.decode(CHARSET))
        data = response_data.get('data')
        assert response_data['status'] == 'success'
        assert response_data['data'][3]['workorders'][0]['description'] \
            == 'change the fuel of the car'
        assert response_data['message'] == SUCCESS_MESSAGES[
            'successfully_fetched'].format('search results')

    def test_search_endpoint_with_invalid_query_param_fails(
            self, init_db, client, auth_header,
            new_work_order):
        """Tests when request is invalid by providing wrong query param.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_work_order: fixture that contains the work order

        """
        new_work_order.save()
        response = client.get(
            f'{api_v1_base_url}/search?qrr={work_order_query_text}',
            headers=auth_header)
        response_data = json.loads(response.data.decode(CHARSET))
        data = response_data.get('data')
        assert response_data['status'] == 'error'
        assert response_data['message'] == serialization_errors[
            'required_param_key'
        ].format('q')

    def test_search_endpoint_with_empty_query_param_value_fails(
            self, init_db, client, auth_header,
            new_work_order):
        """Tests when request is invalid by providing empty query param value.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_work_order: fixture that contains the work order

        """
        new_work_order.save()
        response = client.get(
            f'{api_v1_base_url}/search?q=',
            headers=auth_header)
        response_data = json.loads(response.data.decode(CHARSET))
        data = response_data.get('data')
        assert response_data['status'] == 'error'
        assert response_data['message'] == serialization_errors[
            'empty_query_param_value'
        ]
