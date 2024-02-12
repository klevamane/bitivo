"""Module of tests for work order delete endpoint"""

# Flask
from flask import json

# Utilities
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import (serialization_errors,
                                                   jwt_errors)
from api.utilities.constants import CHARSET, MIMETYPE
from tests.mocks.user import user_one

# app config
from config import AppConfig

# Base url
BASE_URL = AppConfig.API_BASE_URL_V1


class TestWorkOrderDeleteEndpoints:
    """TestWorkOrder resource delete endpoint"""

    def test_delete_work_order_by_id_succeeds(self, init_db, client, new_user,
                                              auth_header, new_work_order):
        """Tests deleting a work order created.
        Only the creator of the work order can delete it

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_work_order(object): fixture that contains the work order
        """

        new_user.token_id = user_one.token_id
        new_user.save()
        new_work_order.created_by = new_user.token_id
        new_work_order.save()
        response = client.delete(
            f'{BASE_URL}/work-orders/{new_work_order.id}', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response_json["status"] == "success"
        assert response_json["message"] == \
           SUCCESS_MESSAGES['deleted'].format('work order')
        assert response.status_code == 200

    def test_delete_already_deleted_work_order_fails(
            self, init_db, client, auth_header, new_work_order_duplicate, new_user):
        """Tests deleting already deleted work order.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_work_order_duplicate(object): fixture that contains the work order
        """
        new_user.token_id = user_one.token_id
        new_user.save()
        new_work_order_duplicate.deleted = True
        new_work_order_duplicate.save()
        response = client.delete(
            f'{BASE_URL}/work-orders/{new_work_order_duplicate.id}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json["status"] == "error"
        assert response_json["message"] == \
           serialization_errors['not_found'].format('Work order')

    def test_delete_work_order_created_by_different_user_fails(
            self, init_db, client, new_user_two, auth_header,
            new_work_order_with_assignee_in_center, new_user):
        """Tests deleting a work order created by a different user fails.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_work_order_with_assignee_in_center(object): fixture that contains the work order
        """

        new_user_two.save()
        new_work_order_with_assignee_in_center.created_by = new_user_two.token_id
        new_work_order_with_assignee_in_center.save()
        response = client.delete(
            f'{BASE_URL}/work-orders/{new_work_order_with_assignee_in_center.id}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response_json["status"] == "error"
        assert response_json["message"] == \
           serialization_errors['cannot_delete'].format('work order')
        assert response.status_code == 403

    def test_delete_work_order_with_no_token_fails(self, init_db, client,
                                                   new_work_order):
        """Tests when token is not provided.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            new_work_order(object): fixture that contain work order
        """

        response = client.get(f'{BASE_URL}/work-orders/{new_work_order.id}')
        response_data = json.loads(response.data.decode(CHARSET))
        assert response_data['status'] == 'error'
        assert response_data['message'] == jwt_errors['NO_TOKEN_MSG']
        assert response.status_code == 401

    def test_deleting_work_order_with_invalid_token_fail(
            self, client, init_db, new_work_order_duplicate):
        """Should fail when invalid token is provided
    
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_work_order_duplicate(object): fixture that contains the work order
        """

        new_work_order_duplicate.save()
        response = client.get(
            f'{BASE_URL}/work-orders/{new_work_order_duplicate.id}',
            headers={
                'Authorization': "Bearer XXXX",
                'Content-Type': MIMETYPE,
                'Accept': MIMETYPE
            })
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['INVALID_TOKEN_MSG']

    def test_delete_work_order_by_id_with_schedule_succeeds(
            self, init_db, client, new_user, auth_header, new_work_order,
            new_schedule):
        """Tests deleting a work order created alongside it's schedules

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_work_order(object): fixture that contains the work order
        """
        new_work_order.created_by = new_user.token_id
        new_work_order.deleted = False
        new_work_order.save()
        new_schedule.work_order_id = new_work_order.id
        new_schedule.save()
        response = client.delete(
            f'{BASE_URL}/work-orders/{new_work_order.id}', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response_json["status"] == "success"
        assert response_json["message"] == \
           SUCCESS_MESSAGES['deleted'].format('work order')
        assert response.status_code == 200
