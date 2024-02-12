"""
Module of tests for  stock count activity tracker
"""
# system imports
import json

#App config
from config import AppConfig

# models
from api.models import History

# Constant
from api.utilities.constants import CHARSET

# mock data
from tests.mocks.stock_count import CREATE_STOCK_COUNT_DATA


BASE_URL = AppConfig.API_BASE_URL_V1


class TestStockCountActivityTracker:
    """Tests for stock count activity tracker
    """
    def test_create_stock_count_activity_tracker_succeed(
            self, client, init_db, auth_header, new_user, test_asset_category):
        """Test history is generated when new stock count is created

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_user (dict): fixture to create a new user
            test_asset_category (dict): fixture to get an asset category
        """
        new_user.save()

        CREATE_STOCK_COUNT_DATA["tokenId"] = new_user.token_id
        CREATE_STOCK_COUNT_DATA["stockCount"][0]['assetCategoryId'] = test_asset_category.id

        data = json.dumps(CREATE_STOCK_COUNT_DATA)

        stock_count_response = client.post(
            f'{BASE_URL}/stock-count', headers=auth_header, data=data)
        response = json.loads(
            stock_count_response.data.decode(CHARSET))

        stock_count_id = response['data'][0]['weeks']['1']['id']
        history = History.query_().filter_by(resource_id=stock_count_id).first()

        assert history.resource_id == stock_count_id
        assert history.action == 'Add'
        assert history.activity == 'Added to Activo'

    def test_delete_stock_count_activity_tracker_succeed(
        self, client, init_db, auth_header, new_stock_count):
        """Test history is generated when stock count is deleted

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_stock_count (dict): fixture for creating a stock count
        """
        stock_count= new_stock_count.save()
        stock_count_id = stock_count.id
        client.delete(
            f'{BASE_URL}/stock-count/{stock_count_id}', headers=auth_header)

        history = History.query_().filter_by(resource_id=stock_count_id).first()

        assert history.resource_id == stock_count_id
        assert history.action == 'Delete'
        assert history.activity == 'Removed from Activo'
