""" Testing comments resource endpoints."""

# Third party libraries
from flask import json
import pytest

# Utilities
from api.utilities.constants import CHARSET, MIMETYPE
from api.utilities.messages.error_messages import serialization_errors, database_errors, jwt_errors
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.helpers.maintenance_category import create_maintenance_category
from api.middlewares.base_validator import ValidationError

# Mocks
from tests.mocks.maintenance_category import (
    VALID_MAINTENANCE_CATEGORY_DATA, DUPLICATE_MAINTENANCE_CATEGORY_DATA,
    MAINTENANCE_CATEGORY_WITH_MISSING_FIELDS,
    MAINTENANCE_CATEGORY_WITH_EMPTY_FIELDS,
    VALID_MAINTENANCE_CATEGORY_DATA_WITH_WORK_ORDER)
import json

# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestMaintenanceCategoryPostEndpoint:
    """ Tests create maintenance category endpoints."""

    def test_create_maintenance_category_with_valid_data_succeeds(
            self, client, init_db, auth_header, new_user, test_asset_category):
        """Should successfully create a new maintenance category with valid data provided

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user (dict): fixture to create a new user
            test_asset_category (dict): fixture to get an asset category
        """
        new_user.save()
        VALID_MAINTENANCE_CATEGORY_DATA['centerId'] = new_user.center_id
        VALID_MAINTENANCE_CATEGORY_DATA['assigneeId'] = new_user.token_id
        VALID_MAINTENANCE_CATEGORY_DATA[
            "assetCategoryId"] = test_asset_category.id
        data = json.dumps(VALID_MAINTENANCE_CATEGORY_DATA)
        response = client.post(
            f'{API_BASE_URL_V1}/maintenance-categories',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 201
        assert response_json["status"] == "success"
        assert response_json["message"] == \
           SUCCESS_MESSAGES["created"].format("Maintenance Category")
        assert response_json['data'][
            'title'] == VALID_MAINTENANCE_CATEGORY_DATA['title']
        assert response_json['data']['centerId'] == new_user.center_id
        assert response_json['data']['assetCategory'][
            'id'] == test_asset_category.id

    def test_create_maintenance_category_with_work_order_succeeds(
            self, client, init_db, auth_header, new_user, test_asset_category):
        """Should successfully create a new maintenance category with valid data provided

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user (dict): fixture to create a new user
            test_asset_category (dict): fixture to get an asset category
        """
        new_user.save()
        VALID_MAINTENANCE_CATEGORY_DATA_WITH_WORK_ORDER[
            'centerId'] = new_user.center_id
        VALID_MAINTENANCE_CATEGORY_DATA_WITH_WORK_ORDER[
            'assigneeId'] = new_user.token_id
        VALID_MAINTENANCE_CATEGORY_DATA_WITH_WORK_ORDER[
            "assetCategoryId"] = test_asset_category.id
        VALID_MAINTENANCE_CATEGORY_DATA_WITH_WORK_ORDER['workOrders'][0][
            "assigneeId"] = new_user.token_id
        data = json.dumps(VALID_MAINTENANCE_CATEGORY_DATA_WITH_WORK_ORDER)
        response = client.post(
            f'{API_BASE_URL_V1}/maintenance-categories',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 201
        assert response_json["status"] == "success"
        assert response_json["message"] == \
           SUCCESS_MESSAGES["created"].format("Maintenance Category")
        assert response_json['data'][
            'title'] == VALID_MAINTENANCE_CATEGORY_DATA_WITH_WORK_ORDER[
                'title']
        assert response_json['data']['centerId'] == new_user.center_id
        assert response_json['data']['assetCategory'][
            'id'] == test_asset_category.id

    def test_create_maintenance_category_that_already_exists_fails(
            self, client, init_db, auth_header, new_maintenance_category):
        """This test checks for creating a duplicate maintennace category in a center

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_work_order_duplicate (object): fixture with created work order
        """
        new_maintenance_category.save()
        DUPLICATE_MAINTENANCE_CATEGORY_DATA[
            'centerId'] = new_maintenance_category.center_id
        DUPLICATE_MAINTENANCE_CATEGORY_DATA[
            'assetCategoryId'] = new_maintenance_category.asset_category_id
        data = json.dumps(DUPLICATE_MAINTENANCE_CATEGORY_DATA)
        response = client.post(
            f'{API_BASE_URL_V1}/maintenance-categories',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 409
        assert response_json["status"] == "error"
        assert response_json["message"] == \
            serialization_errors['maintenance_category_exists'].format(DUPLICATE_MAINTENANCE_CATEGORY_DATA['title'])

    def test_creating_maintenance_category_with_no_token_fails(
            self, init_db, client, new_maintenance_category):
        """This test checks for creating a maintenance category with no auth token

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
           new_maintenance_category(object): fixture with maintenance category
        """
        new_maintenance_category.save()
        VALID_MAINTENANCE_CATEGORY_DATA[
            'centerId'] = new_maintenance_category.center_id
        VALID_MAINTENANCE_CATEGORY_DATA[
            'assetCategoryId'] = new_maintenance_category.asset_category_id
        data = json.dumps(VALID_MAINTENANCE_CATEGORY_DATA)
        response = client.post(
            f'{API_BASE_URL_V1}/maintenance-categories', data=data)
        response_data = json.loads(response.data.decode(CHARSET))
        assert response_data['status'] == 'error'
        assert response_data['message'] == jwt_errors['NO_TOKEN_MSG']
        assert response.status_code == 401

    def test_creating_maintenance_category_with_invalid_token_fail(
            self, client, init_db, new_maintenance_category):
        """This test checks for creating a work order with invalid token

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            new_work_order_duplicate(object): fixture that contains the work order

        """
        new_maintenance_category.save()
        VALID_MAINTENANCE_CATEGORY_DATA[
            'centerId'] = new_maintenance_category.center_id
        VALID_MAINTENANCE_CATEGORY_DATA[
            'assetCategoryId'] = new_maintenance_category.asset_category_id
        data = json.dumps(VALID_MAINTENANCE_CATEGORY_DATA)
        response = client.post(
            f'{API_BASE_URL_V1}/maintenance-categories',
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

    def test_create_maintenance_category_with_empty_fields_fails(
            self,
            client,
            auth_header,
    ):
        """This test creating a maintenance category with empty fields

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user (dict): fixture to create a new user
            test_asset_category (dict): fixture to get an asset category
        """
        data = json.dumps(MAINTENANCE_CATEGORY_WITH_EMPTY_FIELDS)
        response = client.post(
            f'{API_BASE_URL_V1}/maintenance-categories',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response.json['message'] == 'An error occurred'
        assert response.json['errors']['title'][0] == serialization_errors[
            'not_empty']
        assert response.json['errors']['centerId'][0] == serialization_errors[
            'invalid_id_field']
        assert response.json['errors']['assetCategoryId'][
            0] == serialization_errors['invalid_id']

    def test_create_maintenance_category_with_missing_fields_fails(
            self, client, auth_header):
        """ Should fail when assetCategoryId is missing in data.
        Args:
            client (object): Fixture to get flask test client
            init_db (object): Used to create the database structure using the models
            auth_header (dict): Fixture to get token
        """

        data = json.dumps(MAINTENANCE_CATEGORY_WITH_MISSING_FIELDS)
        response = client.post(
            f'{API_BASE_URL_V1}/maintenance-categories',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response.json['errors']['assetCategoryId'][
            0] == serialization_errors['field_required']
        assert response.json['errors']['centerId'][0] == serialization_errors[
            'field_required']

    def test_create_maintenance_category_helper_fails(self):
        """Should fail when data is invalid"""

        data = {}
        with pytest.raises(ValidationError):
            create_maintenance_category(data, data)
