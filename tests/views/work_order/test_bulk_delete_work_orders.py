"""Module for bulk delete work orders endpoint"""

# Standard Libraries
from os import getenv

# Flask
from flask import json

# Utilities
from api.models.database import db

from api.models import WorkOrder
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import (serialization_errors,
                                                   jwt_errors)
from api.utilities.constants import CHARSET, MIMETYPE

# Base url
BASE_URL = getenv('API_BASE_URL_V1')


class TestBulkWorkOrderDeleteEndpoint:
    """TestWorkOrder resource delete endpoint"""

    def check_delete_status(self):
        """Helper method to return the bulk deleted work orders"""
        deleted_work_order = db.session.query(WorkOrder).filter_by(deleted=True).all()
        return deleted_work_order

    def test_delete_work_orders_succeeds(
        self, init_db, client, new_user, auth_header, create_bulk_work_orders):
        """Tests deleting a work orders created.
        Only the creator of the work order can delete it

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            create_bulk_work_orders(object): fixture that contains the work orders
        """
        work_order_ids = [
            create_bulk_work_orders[0].save().id,
            create_bulk_work_orders[1].save().id,
            create_bulk_work_orders[2].save().id
        ]
        assert create_bulk_work_orders[0].title == 'Fuel Level'
        assert create_bulk_work_orders[1].title == 'work order 2'
        assert create_bulk_work_orders[2].title == 'work order 3'
        assert create_bulk_work_orders[0].deleted == False
        assert create_bulk_work_orders[1].deleted == False
        assert create_bulk_work_orders[2].deleted == False

        data = json.dumps(work_order_ids)
        response = client.delete(
            f'{BASE_URL}/work-orders', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert len(create_bulk_work_orders) == 3
        assert self.check_delete_status()[0].title == 'Fuel Level'
        assert self.check_delete_status()[0].deleted == True
        assert self.check_delete_status()[1].deleted == True
        assert self.check_delete_status()[2].deleted == True
        #schedule deleted asserts
        assert len(self.check_delete_status()[0].schedules) == 0
        assert len(self.check_delete_status()[1].schedules) == 0
        assert len(self.check_delete_status()[2].schedules) == 0
        assert response_json["status"] == "success"
        assert response_json["message"] == \
               SUCCESS_MESSAGES['deleted'].format(f'{len(work_order_ids)}'' work orders')
        assert response.status_code == 200

    def test_bulk_delete_work_orders_allow_single_delete(
            self, init_db, client, new_user, auth_header, new_work_order):
        """Tests deleting a single work order.
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_work_order(object): fixture that contains the work order
        """
        work_order_ids = [
            new_work_order.save().id,
        ]
        assert new_work_order.title == 'Fuel Level'

        assert new_work_order.deleted == False

        data = json.dumps(work_order_ids)
        response = client.delete(
            f'{BASE_URL}/work-orders', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert self.check_delete_status()[0].title == 'Fuel Level'
        assert self.check_delete_status()[0].deleted == True

        # schedule deleted asserts
        assert len(self.check_delete_status()[0].schedules) == 0
        assert response_json["message"] == \
               SUCCESS_MESSAGES['deleted'].format(f'{len(work_order_ids)}'' work orders')
        assert response.status_code == 200

    def test_bulk_delete_work_orders_with_invalid_ids_fail(
            self, init_db, client, new_user, auth_header):
        """Tests deleting work orders with invalid ids.
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        """
        work_order_ids = [
            'ljfvkdbjdj djdkkbj',
            '-LZyPcAkKgvIx0bg_6u x'
        ]

        data = json.dumps(work_order_ids)
        response = client.delete(
            f'{BASE_URL}/work-orders', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response_json["errors"][0] == \
               {'ljfvkdbjdj djdkkbj': serialization_errors['invalid_id_field'].format('Work order')}

        assert len(response_json["errors"]) == 2
        assert response_json["errors"]
        assert response.status_code == 400

    def test_bulk_delete_work_orders_with_no_work_orders_ids_fails(
            self, init_db, client, new_user, auth_header):
        """Tests deleting a work orders created.
        Only the creator of the work order can delete it
        new_work_order.created_by = new_user.token_id
        new_work_order.save()
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        """
        work_order_ids = []

        data = json.dumps(work_order_ids)
        response = client.delete(
            f'{BASE_URL}/work-orders', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response_json["status"] == "error"
        assert response_json["message"] == \
               serialization_errors['cannot_be_empty'].format('work orders')
        assert response.status_code == 400

    def test_delete_already_deleted_work_orders_fails(
            self, init_db, client, auth_header, create_bulk_work_orders):
        """Tests deleting already deleted work order.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            create_bulk_work_orders(object): fixture that contains the work orders
        """

        create_bulk_work_orders[0].deleted = True
        create_bulk_work_orders[1].deleted = True
        create_bulk_work_orders[2].deleted =True
        work_order = create_bulk_work_orders[0].save()

        work_order_ids = [
            create_bulk_work_orders[0].save().id,
            create_bulk_work_orders[1].save().id,
            create_bulk_work_orders[2].save().id
        ]
        data = json.dumps(work_order_ids)
        response = client.delete(
            f'{BASE_URL}/work-orders',
            headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == 'error'
        assert response_json["errors"][0] == \
               {work_order.id: serialization_errors['not_found'].format('Work order')}
        assert len(response_json["errors"]) == 3

    def test_delete_work_orders_not_existing_fails(
        self, init_db, client, auth_header, create_bulk_work_orders):
        """Tests deleting already deleted work order.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            create_bulk_work_orders(object): fixture that contains the work orders
        """
        work_order_ids = [
            '-LZyPcAkKgvIx0bg_6ux',
            create_bulk_work_orders[1].save().id,
            create_bulk_work_orders[2].save().id
        ]
        data = json.dumps(work_order_ids)
        response = client.delete(
            f'{BASE_URL}/work-orders',
            headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert len(create_bulk_work_orders) == 3
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert response_json["message"] == \
               SUCCESS_MESSAGES['deleted'].format(f'{len(work_order_ids)-1}'' work orders')

        assert response_json["errors"][0] == \
               {'-LZyPcAkKgvIx0bg_6ux':serialization_errors['not_found'].format('Work order')}


    def test_delete_bulk_work_orders_created_by_other_users_fails(
        self, init_db, client, new_user_two, auth_header,
            new_work_order_with_assignee_in_center, create_bulk_work_orders):
        """Tests deleting a work order created by a different user fails.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_work_order_with_assignee_in_center(object): fixture that contains the work order
        """

        new_user_two.save()
        new_work_order_with_assignee_in_center.created_by = new_user_two.token_id
        create_bulk_work_orders[2].created_by = new_user_two.token_id
        new_work_order_with_assignee_in_center.save()
        work_order_ids = [
            new_work_order_with_assignee_in_center.id,
            create_bulk_work_orders[2].save().id,
        ]
        data = json.dumps(work_order_ids)
        response = client.delete(
            f'{BASE_URL}/work-orders',
            headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response_json["status"] == "error"
        assert response_json["errors"][0] == \
               {new_work_order_with_assignee_in_center.id: serialization_errors['delete_not_allowed'].format('work order')}
        assert response.status_code == 400

    def test_delete_bulk_work_orders_with_no_token_fails(self, init_db, client,
                                                         create_bulk_work_orders):
        """Tests when token is not provided.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
           create_bulk_work_orders(object): fixture that contains the work orders
        """
        work_order_ids = [
            create_bulk_work_orders[0].save().id,
            create_bulk_work_orders[1].save().id,
            create_bulk_work_orders[2].save().id
        ]

        data = json.dumps(work_order_ids)
        response = client.delete(
            f'{BASE_URL}/work-orders', data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']
        assert response.status_code == 401

    def test_deleting_bulk_work_orders_with_invalid_token_fail(
        self, client, init_db, create_bulk_work_orders):
        """Should fail when invalid token is provided

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
           create_bulk_work_orders(object): fixture that contains the work orders
        """
        work_order_ids = [
            create_bulk_work_orders[0].save().id,
            create_bulk_work_orders[1].save().id,
            create_bulk_work_orders[2].save().id
        ]

        data = json.dumps(work_order_ids)

        response = client.get(
            f'{BASE_URL}/work-orders',
            headers={
                'Authorization': "Bearer XXXX",
                'Content-Type': MIMETYPE,
                'Accept': MIMETYPE
            }, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['INVALID_TOKEN_MSG']


