""" Testing comments resource endpoints."""

# Third party libraries
from flask import json
import pytest
import json
# Utilities
from api.utilities.constants import CHARSET

# models
from api.models import History

# Mocks
from tests.mocks.maintenance_category import (
    VALID_MAINTENANCE_CATEGORY_DATA, 
    VALID_MAINTENANCE_CATEGORY_DATA_WITH_WORK_ORDER,
    VALID_UPDATE_MAINTENANCE_CATEGORY_DATA)

# app config
from config import Config

API_BASE_URL_V1 = Config.API_BASE_URL_V1


class TestMaintenanceCategoryPostEndpoint:
    """ Tests create maintenance category history."""

    def test_tracking_for_update_maintenance_category_with_valid_data_and_no_work_orders_succeeds(
            self, client, init_db, auth_header, new_user, test_asset_category,
            new_maintenance_category):
        """ Test history is updated when maintenance category with valid data and no work orders is updated
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user (dict): fixture to create a new user
            test_asset_category (dict): fixture to get an asset category
            new_maintenance_category(object): fixture with maintenance category
        """
        new_user.save()
        maintenance_category = new_maintenance_category.save()
        VALID_UPDATE_MAINTENANCE_CATEGORY_DATA['centerId'] = new_user.center_id
        VALID_UPDATE_MAINTENANCE_CATEGORY_DATA[
            "assetCategoryId"] = test_asset_category.id
        data = json.dumps(VALID_UPDATE_MAINTENANCE_CATEGORY_DATA)
        response = client.patch(
            f'{API_BASE_URL_V1}/maintenance-categories/{maintenance_category.id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        id = response_json['data']["id"]
 
        history = History.query_().filter_by(resource_id=id).first()

        assert history.action == 'Edit'


    def test_tracking_for_create_history_maintenance_category_with_valid_data_succeeds(
            self, client, init_db, auth_header, new_user, test_asset_category):
        """Test history is generated when new maintenance category is created

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
        id = response_json['data']["id"]
 
        history = History.query_().filter_by(resource_id=id).first()

        assert history.action == 'Add'
        assert history.activity == 'Added to Activo'

    def test_tracking_for_create_maintenance_category_with_work_order_succeeds(
            self, client, init_db, auth_header, new_user, test_asset_category):
        """Should add to history when maintenance category with no work orders is created

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
        id = response_json['data']["id"]
 
        history = History.query_().filter_by(resource_id=id).first()

        assert history.action == 'Add'
        assert history.activity == 'Added to Activo'

    def test_tracking_for_delete_maintenance_category_succeeds(
            self, client, auth_header, duplicate_maintenance_category):
        """Should add to history when maintenance category delete succeeds
        
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get a token
            duplicate_maintenance_category (obj): fixture for creating a maintenance category
        """
        duplicate_maintenance_category.save()
        id = duplicate_maintenance_category.id
        response = client.delete(
            f'{API_BASE_URL_V1}/maintenance-categories/{id}',
            headers=auth_header)
 
        history = History.query_().filter_by(resource_id=id).first()
        assert history.action == 'Delete'
        assert history.activity == 'Removed from Activo'
