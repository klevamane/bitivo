"""module of tests for asset endpoints
"""
# Third-party libraries
from flask import json

# Constants
from api.utilities.constants import CHARSET, MIMETYPE

# Mocks
from tests.mocks.work_order import VALID_WORK_ORDER_UPDATE, VALID_WORK_ORDER_WITH_SAME_TITLE_UPDATE

# Messages
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import (serialization_errors,
                                                   jwt_errors)

# app config
from config import AppConfig

api_v1_base_url = AppConfig.API_BASE_URL_V1


class TestUpdateWorkOrderEndpoints:
    """Test class for work order endpoints"""

    def test_update_existing_work_order_succeeds(
            self, client, init_db, auth_header,
            new_work_order_with_assignee_in_center):
        """Tests update existing work order with valid data.
            Args:
                    client (FlaskClient): fixture to get flask test client
                    init_db (SQLAlchemy): fixture to initialize the test database
                    auth_header (dict): fixture to get token
                    new_work_order_with_assignee_in_center: fixtures that contains work_order assignee in center
        """

        new_work_order_with_assignee_in_center.save()

        VALID_WORK_ORDER_UPDATE[
            'assigneeId'] = new_work_order_with_assignee_in_center.assignee_id
        VALID_WORK_ORDER_UPDATE['maintenanceCategoryId'] = \
            new_work_order_with_assignee_in_center.maintenance_category_id

        data_update = json.dumps(VALID_WORK_ORDER_UPDATE)
        response = client.patch(
            f'{api_v1_base_url}/work-orders/{new_work_order_with_assignee_in_center.id}',
            headers=auth_header,
            data=data_update)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert response_json["message"] == SUCCESS_MESSAGES['updated'].format(
            'Work Order')
        assert response_json['data']['title'] == VALID_WORK_ORDER_UPDATE[
            'title']
        assert response_json['data']['description'] == VALID_WORK_ORDER_UPDATE[
            'description']
        assert response_json['data']['frequency'] == VALID_WORK_ORDER_UPDATE[
            'frequency']
        assert response_json['data']['assignee'][
            'tokenId'] == VALID_WORK_ORDER_UPDATE['assigneeId']
        assert response_json['data']['maintenanceCategory'][
            'id'] == VALID_WORK_ORDER_UPDATE['maintenanceCategoryId']

    def test_update_existing_work_order_only_one_field_succeeds(
            self, client, init_db, auth_header,
            new_work_order_with_assignee_in_center):
        """Tests update existing work order with valid data.
			Args:
					client (FlaskClient): fixture to get flask test client
					init_db (SQLAlchemy): fixture to initialize the test database
					auth_header (dict): fixture to get token
					new_work_order_with_assignee_in_center: fixtures that contains work_order assignee in center
		"""

        new_work_order_with_assignee_in_center.save()

        work_order_object = {"title": "edited work order"}

        data_update = json.dumps(work_order_object)
        response = client.patch(
            f'{api_v1_base_url}/work-orders/{new_work_order_with_assignee_in_center.id}',
            headers=auth_header,
            data=data_update)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert response_json["message"] == SUCCESS_MESSAGES['updated'].format(
            'Work Order')
        assert response_json['data']['title'] == work_order_object['title']
        assert response_json['data'][
            'description'] == new_work_order_with_assignee_in_center.description
        assert response_json['data']['assignee'][
            'tokenId'] == new_work_order_with_assignee_in_center.assignee_id
        assert response_json['data']['maintenanceCategory'][
            'id'] == new_work_order_with_assignee_in_center.maintenance_category_id

    def test_update_existing_work_order_when_start_date_is_greater_than_end_date_fails(
            self, client, init_db, auth_header,
            new_work_order_with_assignee_in_center):
        """Tests update existing work order with non existing work
		order id in the database.
			 Args:
				client (FlaskClient): fixture to get flask test client
				init_db (SQLAlchemy): fixture to initialize the test database
				auth_header (dict): fixture to get token
				new_work_order_with_assignee_in_center: fixtures that contains work_order assignee in center
		"""
        new_work_order_with_assignee_in_center.save()
        valid_work_order = VALID_WORK_ORDER_UPDATE.copy()
        valid_work_order[
            'assigneeId'] = new_work_order_with_assignee_in_center.assignee_id
        valid_work_order['maintenanceCategoryId'] = \
            new_work_order_with_assignee_in_center.maintenance_category_id
        valid_work_order['startDate'] = "2019-08-17 21:00:00"
        data_update = json.dumps(valid_work_order)

        response = client.patch(
            f'{api_v1_base_url}/work-orders/{new_work_order_with_assignee_in_center.id}',
            headers=auth_header,
            data=data_update)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'invalid_date_range']

    def test_update_existing_work_order_with_invalid_id_fails(
            self, client, init_db, auth_header,
            new_work_order_with_assignee_in_center):
        """Tests update existing work order with non existing work
        order id in the database.
             Args:
                client (FlaskClient): fixture to get flask test client
                init_db (SQLAlchemy): fixture to initialize the test database
                auth_header (dict): fixture to get token
                new_work_order_with_assignee_in_center: fixtures that contains work_order assignee in center
        """
        new_work_order_with_assignee_in_center.save()

        VALID_WORK_ORDER_UPDATE[
            'assigneeId'] = new_work_order_with_assignee_in_center.assignee_id
        VALID_WORK_ORDER_UPDATE['maintenanceCategoryId'] = \
            new_work_order_with_assignee_in_center.maintenance_category_id
        data_update = json.dumps(VALID_WORK_ORDER_UPDATE)
        response = client.patch(
            f'{api_v1_base_url}/work-orders/-LW35jPhgFVJ__fCFGey',
            headers=auth_header,
            data=data_update)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'not_found'].format('Work order')

    #
    def test_update_existing_work_order_should_fail_with_unsuccessful_authentication(
            self, client, init_db, new_work_order_with_assignee_in_center):
        """Should return a 401 error response when token is not provided
        or invalid
             Args:
                    client (FlaskClient): fixture to get flask test client
                    init_db (SQLAlchemy): fixture to initialize the test database
                    new_work_order_with_assignee_in_center: fixtures that contains work_order  assignee in center
        """
        new_work_order_with_assignee_in_center.save()

        VALID_WORK_ORDER_UPDATE[
            'assigneeId'] = new_work_order_with_assignee_in_center.assignee_id
        VALID_WORK_ORDER_UPDATE['maintenanceCategoryId'] = \
            new_work_order_with_assignee_in_center.maintenance_category_id
        response = client.patch(
            f'{api_v1_base_url}/work-orders/{new_work_order_with_assignee_in_center.id}',
            data=json.dumps(VALID_WORK_ORDER_UPDATE))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_update_existing_work_order_should_fail_with_invalid_token(
            self, client, init_db, new_work_order_with_assignee_in_center):
        """
        Should fail when invalid token is provided
             Args:
                    client (FlaskClient): fixture to get flask test client
                    init_db (SQLAlchemy): fixture to initialize the test database
                    new_work_order_with_assignee_in_center: fixtures that contains work_order assignee  in center
        """
        new_work_order_with_assignee_in_center.save()
        response = client.patch(
            f'{api_v1_base_url}/work-orders/{new_work_order_with_assignee_in_center.id}',
            headers={
                'Authorization': "Bearer XXXX",
                'Content-Type': MIMETYPE,
                'Accept': MIMETYPE
            },
            data=json.dumps(VALID_WORK_ORDER_UPDATE))
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['INVALID_TOKEN_MSG']

    def test_update_existing_work_order_when_title_exist_suceeds(
            self, client, init_db, auth_header,
            new_work_order_with_assignee_in_center):
        """Tests update existing work order with valid data.
			Args:
					client (FlaskClient): fixture to get flask test client
					init_db (SQLAlchemy): fixture to initialize the test database
					auth_header (dict): fixture to get token
					new_work_order_with_assignee_in_center: fixtures that contains work_order assignee in center
		"""

        new_work_order_with_assignee_in_center.save()
        VALID_WORK_ORDER_WITH_SAME_TITLE_UPDATE[
            'title'] = new_work_order_with_assignee_in_center.title
        VALID_WORK_ORDER_WITH_SAME_TITLE_UPDATE[
            'assigneeId'] = new_work_order_with_assignee_in_center.assignee_id
        VALID_WORK_ORDER_WITH_SAME_TITLE_UPDATE['maintenanceCategoryId'] = \
            new_work_order_with_assignee_in_center.maintenance_category_id

        data_update = json.dumps(VALID_WORK_ORDER_WITH_SAME_TITLE_UPDATE)
        response = client.patch(
            f'{api_v1_base_url}/work-orders/{new_work_order_with_assignee_in_center.id}',
            headers=auth_header,
            data=data_update)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert response_json["message"] == SUCCESS_MESSAGES['updated'].format(
            'Work Order')
        assert response_json['data'][
            'title'] == VALID_WORK_ORDER_WITH_SAME_TITLE_UPDATE['title']
        assert response_json['data'][
            'description'] == VALID_WORK_ORDER_WITH_SAME_TITLE_UPDATE[
                'description']
        assert response_json['data'][
            'frequency'] == VALID_WORK_ORDER_WITH_SAME_TITLE_UPDATE[
                'frequency']
        assert response_json['data']['assignee'][
            'tokenId'] == VALID_WORK_ORDER_WITH_SAME_TITLE_UPDATE['assigneeId']
        assert response_json['data']['maintenanceCategory'][
            'id'] == VALID_WORK_ORDER_WITH_SAME_TITLE_UPDATE[
                'maintenanceCategoryId']

    def test_update_existing_work_order_when_assignee_not_in_center_fails(
            self, client, init_db, auth_header,
            new_work_order_with_assignee_not_in_center):
        """Tests update existing work order when assignee does not exist in
        the work order center fails.
            Args:
                client (FlaskClient): fixture to get flask test client
                init_db (SQLAlchemy): fixture to initialize the test database
                auth_header (dict): fixture to get token
                new_work_order_with_assignee_not_in_center: fixtures that contains work_order assignee not  in center
        """
        new_work_order_with_assignee_not_in_center.save()

        VALID_WORK_ORDER_UPDATE[
            'assigneeId'] = new_work_order_with_assignee_not_in_center.assignee_id
        VALID_WORK_ORDER_UPDATE['maintenanceCategoryId'] = \
            new_work_order_with_assignee_not_in_center.maintenance_category_id
        VALID_WORK_ORDER_UPDATE['title'] = "calory is updating"

        data_update = json.dumps(VALID_WORK_ORDER_UPDATE)
        response = client.patch(
            f'{api_v1_base_url}/work-orders/{new_work_order_with_assignee_not_in_center.id}',
            headers=auth_header,
            data=data_update)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'assignee_not_found'].format('assignee')
