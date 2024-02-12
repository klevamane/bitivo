"""Module of tests for stock count endpoints"""
# Third party
from flask import json

# Models
from api.models.asset_category import AssetCategory

# Constants
from api.utilities.constants import CHARSET

# Error messages
from api.utilities.messages.error_messages import (
    serialization_errors, jwt_errors, INVALID_INPUT_MSG_EXTRAS)

# Mocks
from tests.mocks.stock_count import STOCK_COUNT_DATA, STOCK_COUNT_LIST

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1


class TestStockCountEndpoints:
    """
    Stock count endpoints test
    """

    @staticmethod
    def get_stock_count_data(*args):
        """Create the stock count data

        Args:
            args (tuple): Contains new_user and new_asset_category objects.

        Returns:
            list: stock count data
        """

        new_user, asset_category = args
        new_user.save()
        stock_count_data = STOCK_COUNT_DATA.copy()
        stock_count_data['assetCategoryId'] = asset_category.save().id

        return {
            'stockCount': [
                stock_count_data,
            ]
        }

    def test_record_stock_count_no_token(self, client, init_db):
        """Tests recording stock count with invalid week value fails.

        Args:
            client (FlaskClient): Fixture to get flask test client.
            init_db (SQLAlchemy): Fixture to initialize the test database.

        Returns:
            None

        """

        response = client.post(f'{BASE_URL}/stock-count')
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_record_stock_count_success(self, client, init_db, auth_header,
                                        new_user_and_asset_category):
        """Tests successfully recording stock count.

        Args:
            client (FlaskClient): Fixture to get flask test client.
            init_db (SQLAlchemy): Fixture to initialize the test database.
            auth_header (dict): Fixture to get token.
            new_user_and_asset_category (object): Fixture to load new user obj.

        Returns:
            None

        """

        stock_count_data = self.get_stock_count_data(
            *new_user_and_asset_category)

        response = client.post(
            f'{BASE_URL}/stock-count',
            data=json.dumps(stock_count_data),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 201
        assert response_json['status'] == 'success'
        assert len(response_json['data'][0]) > 0
        assert response_json['data'][0]['weeks']
        assert response_json['data'][0]['lastStockCount']
        assert response_json['data'][0]['category']

    def test_record_stock_count_invalid_week_fail(
            self, client, init_db, auth_header, new_user_and_asset_category):
        """Tests recording stock count with invalid week value fails.

        Args:
            client (FlaskClient): Fixture to get flask test client.
            init_db (SQLAlchemy): Fixture to initialize the test database.
            auth_header (dict): Fixture to get token.
            new_user_and_asset_category (object): Fixture to load new user obj.

        Returns:
            None

        """

        stock_count_data = self.get_stock_count_data(
            *new_user_and_asset_category)

        stock_count_data['stockCount'][0]['week'] = 0

        response = client.post(
            f'{BASE_URL}/stock-count',
            data=json.dumps(stock_count_data),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['0']['week'][0] == \
            serialization_errors['invalid_value'] \
            .format(stock_count_data['stockCount'][0]['week'],
                    'week. It must be 1, 2, 3 or 4')

    def test_record_stock_count_same_period_mulitple_times_fails(
            self, client, init_db, auth_header, new_user_and_asset_category):
        """Tests recording stock count for the same period more than once fails.

        Args:
            client (FlaskClient): Fixture to get flask test client.
            init_db (SQLAlchemy): Fixture to initialize the test database.
            auth_header (dict): Fixture to get token.
            new_user_and_asset_category (object): Fixture to load new user obj.

        Returns:
            None

        """

        new_user, asset_category = new_user_and_asset_category
        new_user.save()
        asset_category = AssetCategory(**{'name': 'Test Device'})

        stock_count_data = STOCK_COUNT_DATA.copy()
        stock_count_data['assetCategoryId'] = asset_category.save().id

        data = {
            'stockCount': [
                stock_count_data,
            ]
        }

        # Create initial stock count record
        response_initial = client.post(
            f'{BASE_URL}/stock-count',
            data=json.dumps(data),
            headers=auth_header)

        assert response_initial.status_code == 201

        response = client.post(
            f'{BASE_URL}/stock-count',
            data=json.dumps(data),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['0']['stockCount'][0] == \
            serialization_errors['stock_count_exists']

    def test_record_stock_count_invalid_asset_category_id_fails(
            self, client, init_db, auth_header, new_user_and_asset_category):
        """Tests recording stock count with an invalid asset_category_id.

        Args:
            client (FlaskClient): Fixture to get flask test client.
            init_db (SQLAlchemy): Fixture to initialize the test database.
            auth_header (dict): Fixture to get token.
            new_user_and_asset_category (object): Fixture to load new user obj.

        Returns:
            None

        """

        stock_count_data = self.get_stock_count_data(
            *new_user_and_asset_category)

        stock_count_data['stockCount'][0]['assetCategoryId'] = '***'

        response = client.post(
            f'{BASE_URL}/stock-count',
            data=json.dumps(stock_count_data),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['0']['assetCategoryId'][0] == \
            serialization_errors['invalid_id_field']

    def test_record_stock_count_non_existing_asset_category_id_fails(
            self, client, init_db, auth_header, new_user_and_asset_category):
        """Tests recording stock count with a non-existing asset_category_id.

        Args:
            client (FlaskClient): Fixture to get flask test client.
            init_db (SQLAlchemy): Fixture to initialize the test database.
            auth_header (dict): Fixture to get token.
            new_user_and_asset_category (object): Fixture to load new user obj.

        Returns:
            None

        """

        stock_count_data = self.get_stock_count_data(
            *new_user_and_asset_category)
        stock_count_data['stockCount'][0]['assetCategoryId'] += 'invalid'

        response = client.post(
            f'{BASE_URL}/stock-count',
            data=json.dumps(stock_count_data),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response_json['status'] == 'error'
        assert response_json['errors']['0']['assetCategoryId'][0] == \
            serialization_errors['category_not_found']

    def test_record_stock_count_invalid_stock_count_field_fails(
            self, client, init_db, auth_header, new_user_and_asset_category):
        """Tests recording stock count for the same period more than once.

        Args:
            client (FlaskClient): Fixture to get flask test client.
            init_db (SQLAlchemy): Fixture to initialize the test database.
            auth_header (dict): Fixture to get token.
            new_user_and_asset_category (object): Fixture to load new user obj.

        Returns:
            None

        """

        response = client.post(
            f'{BASE_URL}/stock-count',
            data=json.dumps({'stockCount': []}),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == \
            serialization_errors['invalid_input_value'].format('stockCount')

    def test_record_stock_count_no_stock_count_field_fails(
            self, client, init_db, auth_header, new_user_and_asset_category):
        """Tests recording stock count with missing 'stockCount` field fails.

        Args:
            client (FlaskClient): Fixture to get flask test client.
            init_db (SQLAlchemy): Fixture to initialize the test database.
            auth_header (dict): Fixture to get token.
            new_user_and_asset_category (object): Fixture to load new user obj.

        Returns:
            None

        """

        response = client.post(
            f'{BASE_URL}/stock-count',
            data=json.dumps({}),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == \
            serialization_errors['missing_input_field'].format('stockCount')

    def test_record_stock_count_with_duplicate_asset_category_id_fails(
            self, client, init_db, auth_header, new_user_and_asset_category):
        """Tests recording stock count with duplicate asset categories fails.

        Args:
            client (FlaskClient): Fixture to get flask test client.
            init_db (SQLAlchemy): Fixture to initialize the test database.
            auth_header (dict): Fixture to get token.
            new_user_and_asset_category (object): Fixture to load new user obj.


        Returns:
            None

        """

        new_user, asset_category = new_user_and_asset_category
        new_user.save()
        stock_count_list = STOCK_COUNT_LIST[:]
        for stock_count in stock_count_list:
            stock_count['assetCategoryId'] = asset_category.save().id
            stock_count['week'] = 2

        response = client.post(
            f'{BASE_URL}/stock-count',
            data=json.dumps({'stockCount': stock_count_list}),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']
        assert response_json['errors']['1']['assetCategoryId'][0] == \
            serialization_errors['duplicate_found'].format('asset category id')

    def test_record_stock_count_different_week_values_fails(
            self, client, init_db, auth_header, new_user_and_asset_category):
        """Tests  recording stock count with differing week values fails.

        Args:
            client (FlaskClient): Fixture to get flask test client.
            init_db (SQLAlchemy): Fixture to initialize the test database.
            auth_header (dict): Fixture to get token.
            new_user_and_asset_category (object): Fixture to load new user obj.

        Returns:
            None

        """

        stock_count_data = self.get_stock_count_data(
            *new_user_and_asset_category)
        stock_count_data['stockCount'][0]['week'] = 3

        asset_category = AssetCategory(**{'name': 'Test Device'})
        stock_count_two = STOCK_COUNT_DATA.copy()
        stock_count_two['assetCategoryId'] = asset_category.save().id
        stock_count_two['week'] = 4
        stock_count_data['stockCount'].append(stock_count_two)

        response = client.post(
            f'{BASE_URL}/stock-count',
            data=json.dumps(stock_count_data),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'different_week']

    def test_record_stock_count_invalid_count_fail(
            self, client, init_db, auth_header, new_user_and_asset_category):
        """Tests recording stock count with invalid count value fails.

        Args:
            client (FlaskClient): Fixture to get flask test client.
            init_db (SQLAlchemy): Fixture to initialize the test database.
            auth_header (dict): Fixture to get token.
            new_user_and_asset_category (object): Fixture to load new user obj.

        Returns:
            None

        """

        stock_count_data = self.get_stock_count_data(
            *new_user_and_asset_category)
        stock_count_data['stockCount'][0]['count'] = -1

        response = client.post(
            f'{BASE_URL}/stock-count',
            data=json.dumps(stock_count_data),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['0']['count'][0] == \
            serialization_errors['invalid_value'] \
            .format(stock_count_data['stockCount'][0]['count'],
                    INVALID_INPUT_MSG_EXTRAS['count'])
