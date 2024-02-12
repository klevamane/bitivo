"""Module for work order get endpoint."""

# Flask
from flask import json

# Utilities
from api.utilities.constants import CHARSET, MIMETYPE
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import jwt_errors

# app config
from config import AppConfig

api_v1_base_url = AppConfig.API_BASE_URL_V1


class TestGetWorkOrderEndpoints:
    """Class for work order GET endpoint."""

    def test_get_work_order_by_id_succeeds(
            self, init_db, client, auth_header,
            new_work_order_with_assignee_in_center):
        """Tests when request is valid.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_work_order_with_assignee_in_center: fixture that contains the work order

        """
        new_work_order_with_assignee_in_center.save()
        response = client.get(
            f'{api_v1_base_url}/work-orders/{new_work_order_with_assignee_in_center.id}',
            headers=auth_header)
        response_data = json.loads(response.data.decode(CHARSET))
        data = response_data.get('data')
        assert response_data['status'] == 'success'
        assert response_data['message'] == SUCCESS_MESSAGES[
            'successfully_fetched'].format('Work order')
        assert data.get(
            'title') == new_work_order_with_assignee_in_center.title
        assert data.get('description'
                        ) == new_work_order_with_assignee_in_center.description
        assert response.status_code == 200

    def test_get_work_order_without_pagination_succeeds(
            self, init_db, client, auth_header,
            new_work_order_with_assignee_in_center):
        """Tests when request is valid.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_work_order_with_assignee_in_center: fixture that contains the work order

        """
        new_work_order_with_assignee_in_center.save()
        response = client.get(
            f'{api_v1_base_url}/work-orders?pagination=false',
            headers=auth_header)
        response_data = json.loads(response.data.decode(CHARSET))
        data = response_data.get('data')
        assert response_data['status'] == 'success'
        assert response_data['message'] == SUCCESS_MESSAGES['fetched'].format(
            'Work Orders')
        assert response_data['meta'] is None
        assert response.status_code == 200

    def test_get_all_work_orders_with_pagination_succeeds(
            self, init_db, client, auth_header,
            new_work_order_with_assignee_in_center):
        """Tests when request is valid.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_work_order_with_assignee_in_center: fixture that contains the work order

        """
        new_work_order_with_assignee_in_center.save()
        response = client.get(
            f'{api_v1_base_url}/work-orders', headers=auth_header)
        response_data = json.loads(response.data.decode(CHARSET))
        data = response_data.get('data')
        assert response_data['status'] == 'success'
        assert response_data['message'] == SUCCESS_MESSAGES['fetched'].format(
            'Work Orders')
        assert response_data['meta'] is not None
        assert response_data['meta']['totalCount'] == 1
        assert response.status_code == 200

    def test_get_with_invalid_work_order_by_id_fails(
            self, init_db, client, auth_header,
            new_work_order_with_assignee_in_center):
        """Tests when id is invalid.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_work_order_with_assignee_in_center: fixture that contains the work order

        """
        response = client.get(
            f'{api_v1_base_url}/work-orders/fake-id', headers=auth_header)
        response_data = json.loads(response.data.decode(CHARSET))
        assert response_data.get('status') == 'error'
        assert response_data.get('message') == 'Work order not found'
        assert response.status_code == 404

    def test_get_work_order_with_no_token_fails(
            self, init_db, client, auth_header,
            new_work_order_with_assignee_in_center):
        """Tests when token is not provided.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_work_order_with_assignee_in_center: fixture that contain work order


        """
        response = client.get(
            f'{api_v1_base_url}/work-orders/{new_work_order_with_assignee_in_center.id}'
        )
        response_data = json.loads(response.data.decode(CHARSET))
        assert response_data.get('status') == 'error'
        assert response_data.get('message') == jwt_errors['NO_TOKEN_MSG']
        assert response.status_code == 401

    def test_get_existing_work_order_should_fail_with_invalid_token(
            self, client, init_db, new_work_order_with_assignee_in_center):
        """
        Should fail when invalid token is provided

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            new_work_order_with_assignee_in_center: fixture that contain work order

        """

        new_work_order_with_assignee_in_center.save()
        response = client.get(
            f'{api_v1_base_url}/work-orders/{new_work_order_with_assignee_in_center.id}',
            headers={
                'Authorization': "Bearer XXXX",
                'Content-Type': MIMETYPE,
                'Accept': MIMETYPE
            })
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['INVALID_TOKEN_MSG']
