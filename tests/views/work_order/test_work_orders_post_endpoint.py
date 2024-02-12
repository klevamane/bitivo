"""Module of tests for work order post endpoint"""

# Flask
from flask import json

# Utilities
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import (serialization_errors,
                                                   jwt_errors)
from api.utilities.constants import CHARSET, MIMETYPE

# Mock
from tests.mocks.work_order import (
    VALID_WORK_ORDER, DUPLICATE_WORK_ORDER, WORK_ORDER_WITH_MISSING_FIELDS,
    WORK_ORDER_WITH_INVALID_CUSTOM_OCCURRENCE,
    WORK_ORDER_WITH_INVALID_REPEAT_DAYS, WORK_ORDER_SCHEMA_MESSAGES,
    INVALID_WORK_ORDER_DATETIME)

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1


class TestWorkOrderPostEndpoints:
    """TestWorkOrder resource POST endpoint"""

    def test_create_work_order_valid_data_succeeds(self, client, init_db,
                                                   auth_header, new_user,
                                                   new_maintenance_category):
        """Should successfully create a new work order with valid data provided

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user (dict): fixture to create a new user
            new_maintenance_category (dict): fixture to get an maintenance category
        """
        new_user.save()
        new_maintenance_category.save()
        VALID_WORK_ORDER['centerId'] = new_maintenance_category.center_id
        VALID_WORK_ORDER['assigneeId'] = new_user.token_id
        VALID_WORK_ORDER["maintenanceCategoryId"] = new_maintenance_category.id
        data = json.dumps(VALID_WORK_ORDER)
        response = client.post(
            f'{BASE_URL}/work-orders', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 201
        assert response_json["status"] == "success"
        assert response_json["message"] == \
           SUCCESS_MESSAGES["created"].format("Work Order")
        assert response_json['data']['title'] == VALID_WORK_ORDER['title']
        assert response_json['data']['description'] == VALID_WORK_ORDER[
            'description']
        assert response_json['data']['frequency'] == VALID_WORK_ORDER[
            'frequency']

    def test_create_work_order_with_an_assignee_with_different_center_id_fails(
            self, client, init_db, auth_header, new_user,
            new_maintenance_category):
        """This test checks for assigning a work order to an assignee in a correct center

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user (dict): fixture to create a new user
            new_maintenance_category (dict): fixture to get an maintenance category
        """
        new_user.save()
        new_maintenance_category.save()
        VALID_WORK_ORDER['assigneeId'] = new_user.token_id
        VALID_WORK_ORDER["maintenanceCategoryId"] = new_maintenance_category.id
        data = json.dumps(VALID_WORK_ORDER)
        response = client.post(
            f'{BASE_URL}/work-orders', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 409
        assert response_json["status"] == "error"

    def test_create_work_order_that_already_exists_fails(
            self, client, init_db, auth_header, new_work_order_duplicate):
        """This test checks for creating a duplicate work order in a center

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_work_order_duplicate (object): fixture with created work order
        """
        new_work_order_duplicate.save()
        DUPLICATE_WORK_ORDER[
            'assigneeId'] = new_work_order_duplicate.assignee_id
        DUPLICATE_WORK_ORDER[
            'maintenanceCategoryId'] = new_work_order_duplicate.maintenance_category_id
        data = json.dumps(DUPLICATE_WORK_ORDER)
        response = client.post(
            f'{BASE_URL}/work-orders', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 409
        assert response_json["status"] == "error"
        assert response_json["message"] == \
            serialization_errors['work_order_exists'].format(DUPLICATE_WORK_ORDER['title'])

    def test_creating_work_order_with_no_token_fails(self, init_db, client,
                                                     new_work_order_duplicate):
        """This test checks for creating a work order with no auth token

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            new_work_order_duplicate (object): fixture with work order
        """
        new_work_order_duplicate.save()
        DUPLICATE_WORK_ORDER[
            'assigneeId'] = new_work_order_duplicate.assignee_id
        DUPLICATE_WORK_ORDER[
            'maintenanceCategoryId'] = new_work_order_duplicate.maintenance_category_id
        data = json.dumps(DUPLICATE_WORK_ORDER)
        response = client.post(f'{BASE_URL}/work-orders', data=data)
        response_data = json.loads(response.data.decode(CHARSET))
        assert response_data['status'] == 'error'
        assert response_data['message'] == jwt_errors['NO_TOKEN_MSG']
        assert response.status_code == 401

    def test_creating_work_order_with_invalid_token_fail(
            self, client, init_db, new_work_order_duplicate):
        """This test checks for creating a work order with invalid token

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            new_work_order_duplicate(object): fixture that contains the work order

        """
        new_work_order_duplicate.save()
        DUPLICATE_WORK_ORDER[
            'assigneeId'] = new_work_order_duplicate.assignee_id
        DUPLICATE_WORK_ORDER[
            'maintenanceCategoryId'] = new_work_order_duplicate.maintenance_category_id
        data = json.dumps(DUPLICATE_WORK_ORDER)
        response = client.post(
            f'{BASE_URL}/work-orders',
            headers={
                'Authorization': "Bearer XXXX",
                'Content-Type': MIMETYPE,
                'Accept': MIMETYPE
            },
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['INVALID_TOKEN_MSG']

    def test_create_work_order_with_empty_fields_fails(
            self, client, init_db, auth_header, new_user,
            new_maintenance_category):
        """This test creating a work order with empty fields

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user (dict): fixture to create a new user
            new_maintenance_category (dict): fixture to get an maintenance category
        """
        data = json.dumps(WORK_ORDER_WITH_MISSING_FIELDS)
        response = client.post(
            f'{BASE_URL}/work-orders', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response.json['message'] == 'An error occurred'
        assert response.json['errors']['description'][
            0] == serialization_errors['not_empty']
        assert response.json['errors']['title'][0] == serialization_errors[
            'not_empty']
        assert response.json['errors']['assigneeId'][
            0] == serialization_errors['invalid_assignee_id']
        assert response.json['errors']['endDate'][
            0] == WORK_ORDER_SCHEMA_MESSAGES['date'].format('endDate')
        assert response.json['errors']['startDate'][
            0] == WORK_ORDER_SCHEMA_MESSAGES['date'].format('startDate')
        assert response.json['errors']['frequency'][
            0] == WORK_ORDER_SCHEMA_MESSAGES['frequency']
        assert response.json['errors']['maintenanceCategoryId'][
            0] == serialization_errors[
                'invalid_id_field'], WORK_ORDER_SCHEMA_MESSAGES[
                    'maintenanceCategoryId']

    def test_create_work_order_with_invalid_custom_occurrence(
            self, client, init_db, auth_header, new_user,
            new_maintenance_category):
        """Should successfully create a new work order with valid data provided

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user (dict): fixture to create a new user
            new_maintenance_category (dict): fixture to get an maintenance category
        """
        new_user.save()
        new_maintenance_category.save()
        WORK_ORDER_WITH_INVALID_CUSTOM_OCCURRENCE[
            'centerId'] = new_maintenance_category.center_id
        WORK_ORDER_WITH_INVALID_CUSTOM_OCCURRENCE[
            'assigneeId'] = new_user.token_id
        WORK_ORDER_WITH_INVALID_CUSTOM_OCCURRENCE[
            "maintenanceCategoryId"] = new_maintenance_category.id
        data = json.dumps(WORK_ORDER_WITH_INVALID_CUSTOM_OCCURRENCE)
        response = client.post(
            f'{BASE_URL}/work-orders', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == \
           'An error occurred'
        assert response_json["errors"]["customOccurrence"]["repeat_frequency"][0]  == \
            'Please provide one of daily, weekly, monthly, yearly'
        assert response_json["errors"]["customOccurrence"]["repeat_units"][0]  == \
            'Value must be greater than 0'
        assert response_json["errors"]["customOccurrence"]["ends"]['after'][0]  == \
            'Value must be greater than 0'

    def test_create_work_order_with_invalid_repeat_days(
            self, client, init_db, auth_header, new_user,
            new_maintenance_category):
        """Should successfully create a new work order with valid data provided

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user (dict): fixture to create a new user
            new_maintenance_category (dict): fixture to get an maintenance category
        """
        new_user.save()
        new_maintenance_category.save()
        WORK_ORDER_WITH_INVALID_REPEAT_DAYS[
            'centerId'] = new_maintenance_category.center_id
        WORK_ORDER_WITH_INVALID_REPEAT_DAYS['assigneeId'] = new_user.token_id
        WORK_ORDER_WITH_INVALID_REPEAT_DAYS[
            "maintenanceCategoryId"] = new_maintenance_category.id
        data = json.dumps(WORK_ORDER_WITH_INVALID_REPEAT_DAYS)
        response = client.post(
            f'{BASE_URL}/work-orders', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == \
           'Please provide one of this Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday in repeat days'

    def test_create_work_order_with_invalid_datetime_fields(
            self, client, init_db, auth_header):
        """This test creating a work order with invalid datetime fields

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        invalid_work_order = VALID_WORK_ORDER.copy()
        invalid_work_order['endDate'] = "2019-02-11"
        data = json.dumps(invalid_work_order)
        response = client.post(
            f'{BASE_URL}/work-orders', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response.json['errors']['endDate'][0] == serialization_errors[
            'invalid_date_time'].format('endDate')
