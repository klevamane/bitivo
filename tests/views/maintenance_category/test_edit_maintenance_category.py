# Third party libraries
import json
from flask import json

# Utilities
from api.utilities.constants import CHARSET, MIMETYPE
from api.utilities.messages.error_messages import serialization_errors, database_errors, jwt_errors

# Mocks
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from tests.mocks.maintenance_category import (
    VALID_MAINTENANCE_CATEGORY_DATA,
    VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA,
    VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDERS_DATA,
    MAINTENANCE_CATEGORY_WITH_EMPTY_FIELDS,
    VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA_WITH_INVALID_ENDS_FIELD)

# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestEditMaintenanceCategory:
    def test_update_maintenance_category_with_valid_data_and_no_work_orders_succeeds(
            self, client, init_db, auth_header_two, new_user, test_asset_category,
            new_maintenance_category):
        """ Test to Update maintenance category with no work orders
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header_two(dict): fixture to get token
            new_user (dict): fixture to create a new user
            test_asset_category (dict): fixture to get an asset category
            new_maintenance_category(object): fixture with maintenance category
        """
        new_user.save()
        maintenance_category = new_maintenance_category.save()
        VALID_MAINTENANCE_CATEGORY_DATA['centerId'] = new_user.center_id
        VALID_MAINTENANCE_CATEGORY_DATA[
            "assetCategoryId"] = test_asset_category.id
        data = json.dumps(VALID_MAINTENANCE_CATEGORY_DATA)
        response = client.patch(
            f'{API_BASE_URL_V1}/maintenance-categories/{maintenance_category.id}',
            headers=auth_header_two,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert response_json['data'][
            'title'] == VALID_MAINTENANCE_CATEGORY_DATA['title']
        assert response_json['data']['centerId'] == new_user.center_id

    def test_update_maintenance_category_with_duplicate_title_fails(
            self, client, init_db, auth_header_two, new_user, test_asset_category,
            new_maintenance_category):
        """Test to Update maintenance category with duplicate title
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header_two(dict): fixture to get token
            new_user (dict): fixture to create a new user
            test_asset_category (dict): fixture to get an asset category
            new_maintenance_category(object): fixture with maintenance category
        """
        new_user.save()
        maintenance_category = new_maintenance_category.save()
        VALID_MAINTENANCE_CATEGORY_DATA['centerId'] = new_user.center_id
        VALID_MAINTENANCE_CATEGORY_DATA[
            "assetCategoryId"] = test_asset_category.id
        data = json.dumps(VALID_MAINTENANCE_CATEGORY_DATA)
        response = client.patch(
            f'{API_BASE_URL_V1}/maintenance-categories/{maintenance_category.id}',
            headers=auth_header_two,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 409
        assert response_json["status"] == "error"
        assert response_json['message'] == serialization_errors[
            'maintenance_category_exists'].format(
                VALID_MAINTENANCE_CATEGORY_DATA['title'])

    def test_update_maintenance_category_with_both_work_orders_and_maintenance_category_succeeds(
            self, client, init_db, auth_header_two, new_user, test_asset_category,
            new_maintenance_category):  # pylint: disable=R0201,W0613
        """Test to Update maintenance category with work orders
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header_two(dict): fixture to get token
            new_user (dict): fixture to create a new user
            test_asset_category (dict): fixture to get an asset category
            new_maintenance_category(object): fixture with maintenance category
        """
        new_user.save()
        maintenance_category = new_maintenance_category.save()
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA[
            'centerId'] = new_user.center_id
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA[
            "assetCategoryId"] = test_asset_category.id
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA["workOrders"][0][
            'assigneeId'] = new_user.token_id

        data = json.dumps(VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA)
        response = client.patch(
            f'{API_BASE_URL_V1}/maintenance-categories/{maintenance_category.id}',
            headers=auth_header_two,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert response.json['message'] == SUCCESS_MESSAGES['updated'].format(
            'Maintenance category')

    def test_update_maintenance_category_with_invalid_id_fails(
            self, client, init_db, auth_header_two, new_user, test_asset_category,
            new_maintenance_category):  # pylint: disable=R0201,W0613
        """
            Test Update maintenance category with invalid maintenance category id
        """
        new_user.save()

        VALID_MAINTENANCE_CATEGORY_DATA['centerId'] = new_user.center_id
        VALID_MAINTENANCE_CATEGORY_DATA[
            "assetCategoryId"] = test_asset_category.id
        data = json.dumps(VALID_MAINTENANCE_CATEGORY_DATA)
        response = client.patch(
            f'{API_BASE_URL_V1}/maintenance-categories/-lxvd',
            headers=auth_header_two,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json["status"] == "error"
        assert response_json['message'] == serialization_errors[
            'not_found'].format('Maintenance category')

    def test_update_maintenance_category_with_invalid_token_fail(
            self, client, init_db, auth_header_two, new_user, test_asset_category,
            new_maintenance_category):  # pylint: disable=R0201,W0613
        """This test checks for creating a maintenance category with invalid token
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header_two(dict): fixture to get token
            new_user (dict): fixture to create a new user
            test_asset_category (dict): fixture to get an asset category
            new_maintenance_category(object): fixture with maintenance category
        """
        new_user.save()
        maintenance_category = new_maintenance_category.save()
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA[
            'centerId'] = new_user.center_id
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA[
            "assetCategoryId"] = test_asset_category.id
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA["workOrders"][0][
            'assigneeId'] = new_user.token_id

        data = json.dumps(VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA)
        response = client.patch(
            f'{API_BASE_URL_V1}/maintenance-categories/{maintenance_category.id}',
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
            self, client, auth_header_two, new_maintenance_category):
        """This test creating a maintenance category with empty fields
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header_two(dict): fixture to get token
            new_maintenance_category(object): fixture with maintenance category
        """
        maintenance_category = new_maintenance_category.save()
        data = json.dumps(MAINTENANCE_CATEGORY_WITH_EMPTY_FIELDS)
        response = client.patch(
            f'{API_BASE_URL_V1}/maintenance-categories/{maintenance_category.id}',
            headers=auth_header_two,
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

    def test_update_maintenance_category_with_duplicate_work_orders_fails(
            self, client, init_db, auth_header_two, new_user, test_asset_category,
            new_maintenance_category):  # pylint: disable=R0201,W0613
        """
            Test to Update maintenance category with duplicate work orders
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header_two(dict): fixture to get token
            new_user (dict): fixture to create a new user
            test_asset_category (dict): fixture to get an asset category
            new_maintenance_category(object): fixture with maintenance category
        """
        new_user.save()
        maintenance_category = new_maintenance_category.save()
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA[
            'centerId'] = new_user.center_id
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA[
            "assetCategoryId"] = test_asset_category.id
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA["workOrders"][0][
            'assigneeId'] = new_user.token_id

        data = json.dumps(VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA)
        response = client.patch(
            f'{API_BASE_URL_V1}/maintenance-categories/{maintenance_category.id}',
            headers=auth_header_two,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 409
        assert response_json["status"] == "error"

    def test_update_maintenance_category_with_many_work_orders_succeeds(
            self, client, init_db, auth_header_two, new_user, test_asset_category,
            new_maintenance_category, new_work_order):  # pylint: disable=R0201,W0613
        """Tests Updating maintenance category with several work orders
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header_two(dict): fixture to get token
            new_user (dict): fixture to create a new user
            test_asset_category (dict): fixture to get an asset category
            new_maintenance_category(object): fixture with maintenance category
            new_work_order (object): fixture to create a maintenance category

        """
        new_user.save()
        maintenance_category = new_maintenance_category.save()
        work_order = new_work_order.save()
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDERS_DATA[
            'centerId'] = new_user.center_id
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDERS_DATA[
            "assetCategoryId"] = test_asset_category.id
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDERS_DATA["workOrders"][0][
            'assigneeId'] = new_user.token_id
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDERS_DATA["workOrders"][0][
            "workOrderId"] = work_order.id
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDERS_DATA["workOrders"][0][
            "title"] = "new tests title oo"

        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDERS_DATA[
            'centerId'] = new_user.center_id
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDERS_DATA[
            "assetCategoryId"] = test_asset_category.id
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDERS_DATA["workOrders"][1][
            'assigneeId'] = new_user.token_id
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDERS_DATA["workOrders"][1][
            "title"] = "maintain cameras"

        data = json.dumps(VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDERS_DATA)
        response = client.patch(
            f'{API_BASE_URL_V1}/maintenance-categories/{maintenance_category.id}',
            headers=auth_header_two,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response_json["status"] == "success"
        assert response_json['data'][
            'title'] == VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDERS_DATA[
                'title']
        assert isinstance(response_json, dict) is True

    def test_exception_raised_with_invalid_data(
            self, client, init_db, auth_header_two, new_user, test_asset_category,
            new_maintenance_category):  # pylint: disable=R0201,W0613
        """Test exception raised if an error occurs
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header_two(dict): fixture to get token
            new_user (dict): fixture to create a new user
            test_asset_category (dict): fixture to get an asset category
            new_maintenance_category(object): fixture with maintenance category
        """
        new_user.save()
        maintenance_category = new_maintenance_category.save()
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA[
            'centerId'] = new_user.center_id
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA[
            "assetCategoryId"] = test_asset_category.id
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA["workOrders"][0][
            'assigneeId'] = new_user.token_id
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA["workOrders"][0][
            "workOrderId"] = ""
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA["workOrders"][0][
            "title"] = "maintain jests"

        data = json.dumps(VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA)
        response = client.patch(
            f'{API_BASE_URL_V1}/maintenance-categories/{maintenance_category.id}',
            headers=auth_header_two,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 501
        assert response_json["status"] == "error"
        assert response.json['message'] == serialization_errors[
            'cannot_update']

    def test_update_maintenance_category_with_invalid_format_fails(
            self, client, init_db, auth_header_two, new_user, test_asset_category,
            new_maintenance_category):
        """ Test invalid data format fails
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header_two(dict): fixture to get token
            new_user (dict): fixture to create a new user
            test_asset_category (dict): fixture to get an asset category
            new_maintenance_category(object): fixture with maintenance category
        """
        new_user.save()
        maintenance_category = new_maintenance_category.save()
        valid_data = VALID_MAINTENANCE_CATEGORY_DATA.copy()
        valid_data['centerId'] = new_user.center_id
        valid_data["assetCategoryId"] = test_asset_category.id
        valid_data['title'] = "new title...*"
        data = json.dumps(valid_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/maintenance-categories/{maintenance_category.id}',
            headers=auth_header_two,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json['errors']['title'][0] == serialization_errors[
            'string_characters']

    def test_update_maintenance_category_with_valid_maintenance_category_and_invalid_work_order_fails(
            self, client, init_db, auth_header_two, new_user, test_asset_category,
            new_maintenance_category):  # pylint: disable=R0201,W0613
        """Test to Update maintenance category with valid maintenance category and invalid work orders
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header_two(dict): fixture to get token
            new_user (dict): fixture to create a new user
            test_asset_category (dict): fixture to get an asset category
            new_maintenance_category(object): fixture with maintenance category
        """
        new_user.save()
        maintenance_category = new_maintenance_category.save()
        valid_data = VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA.copy()
        valid_data['centerId'] = new_user.center_id
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA[
            "assetCategoryId"] = test_asset_category.id
        valid_data["workOrders"][0]['centerId'] = new_user.center_id
        valid_data["workOrders"][0]['assigneeId'] = new_user.token_id
        valid_data["workOrders"][0]["assetCategoryId"] = test_asset_category.id
        valid_data["workOrders"][0]["title"] = '*@(@YE^*T@(&'
        data = json.dumps(valid_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/maintenance-categories/{maintenance_category.id}',
            headers=auth_header_two,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json['errors']['work_orders']['0']['title'][
            0] == serialization_errors['string_characters']

    def test_update_maintenance_category_and_work_with_valid_maintenance_category_and_invalid_work_order_fails(
            self, client, init_db, auth_header_two, new_user, test_asset_category,
            new_maintenance_category, new_work_order):  # pylint: disable=R0201,W0613
        """Test to Update maintenance category with valid maintenance category and invalid work orders
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header_two(dict): fixture to get token
            new_user (dict): fixture to create a new user
            test_asset_category (dict): fixture to get an asset category
            new_maintenance_category(object): fixture with maintenance category
            new_work_order(object): fixture with work order
        """
        new_user.save()
        work_order = new_work_order.save()
        maintenance_category = new_maintenance_category.save()
        valid_data = VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA.copy()
        valid_data['centerId'] = new_user.center_id
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA[
            "assetCategoryId"] = test_asset_category.id
        valid_data["workOrders"][0]['centerId'] = new_user.center_id

        valid_data["workOrders"][0]['workOrderId'] = work_order.id
        valid_data["workOrders"][0]['assigneeId'] = new_user.token_id
        valid_data["workOrders"][0]["assetCategoryId"] = test_asset_category.id
        valid_data["workOrders"][0]["title"] = 'invalid title &*#*>>>>'

        data = json.dumps(valid_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/maintenance-categories/{maintenance_category.id}',
            headers=auth_header_two,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json['errors']['work_orders']['0']['title'][
            0] == serialization_errors['string_characters']

    def test_update_maintenance_category_and_work_with_valid_maintenance_category_and_work_order_succeeds(
            self, client, init_db, auth_header_two, new_user, test_asset_category,
            new_maintenance_category, new_work_order):  # pylint: disable=R0201,W0613
        """Test to Update maintenance category with valid maintenance category and invalid work orders
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header_two(dict): fixture to get token
            new_user (dict): fixture to create a new user
            test_asset_category (dict): fixture to get an asset category
            new_maintenance_category(object): fixture with maintenance category
            new_work_order(object): fixture with work order
        """
        new_user.save()
        work_order = new_work_order.save()
        maintenance_category = new_maintenance_category.save()
        valid_data = VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA.copy()
        valid_data['centerId'] = new_user.center_id
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA[
            "assetCategoryId"] = test_asset_category.id
        valid_data["workOrders"][0]['centerId'] = new_user.center_id
        valid_data["workOrders"][0]['workOrderId'] = work_order.id
        valid_data["workOrders"][0]['assigneeId'] = new_user.token_id
        valid_data["workOrders"][0]["assetCategoryId"] = test_asset_category.id
        valid_data["workOrders"][0]["title"] = 'Some unique tille'
        valid_data["workOrders"][0]["status"] = 'disabled'

        data = json.dumps(valid_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/maintenance-categories/{maintenance_category.id}',
            headers=auth_header_two,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        work_orders = response_json['data']['workOrders']
        updated_work_order = [
            item for item in work_orders if item['id'] == work_order.id
        ]
        assert updated_work_order[0]['title'] == valid_data["workOrders"][0][
            "title"]
        assert updated_work_order[0]['status'] == valid_data["workOrders"][0][
            "status"]
        assert response.status_code == 200
        assert response_json["status"] == "success"

    def test_update_maintenance_category_with_invalid_ends_field_in_work_orders_fails(
            self, client, init_db, auth_header_two, new_user, test_asset_category,
            new_maintenance_category):  # pylint: disable=R0201,W0613
        """Test to Update maintenance category with work orders and invalid ends field
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header_two(dict): fixture to get token
            new_user (dict): fixture to create a new user
            test_asset_category (dict): fixture to get an asset category
            new_maintenance_category(object): fixture with maintenance category
        """
        new_user.save()
        maintenance_category = new_maintenance_category.save()
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA_WITH_INVALID_ENDS_FIELD[
            'centerId'] = new_user.center_id
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA_WITH_INVALID_ENDS_FIELD[
            "assetCategoryId"] = test_asset_category.id
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA_WITH_INVALID_ENDS_FIELD[
            "workOrders"][0]['centerId'] = new_user.center_id
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA_WITH_INVALID_ENDS_FIELD[
            "workOrders"][0]['assigneeId'] = new_user.token_id
        VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA_WITH_INVALID_ENDS_FIELD[
            "workOrders"][0]["assetCategoryId"] = test_asset_category.id

        data = json.dumps(
            VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA_WITH_INVALID_ENDS_FIELD
        )
        response = client.patch(
            f'{API_BASE_URL_V1}/maintenance-categories/{maintenance_category.id}',
            headers=auth_header_two,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response.json['message'] == serialization_errors[
            'invalid_enum_value'].format(
                values='on, never or after in ends field')
