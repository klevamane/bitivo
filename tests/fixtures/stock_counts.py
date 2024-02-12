"""Module with stock counts fixtures """

# System libraries
import datetime as dt

# Third Party Modules
import pytest

# Models
from api.models import StockCount, AssetCategory

# Utilities
from api.utilities.helpers.get_last_month import get_last_month


@pytest.fixture(scope='module')
def new_stock_count(app, new_asset_category, new_center, new_user):
    """Fixture for a stock count.
    Args:
        app (object): application
        new_asset_category (object): fixture for a new asset category
        new_center (object): fixture for a new center
        new_user (object): fixture for a new user
    """

    user = new_user.save()
    category = new_asset_category.save()
    center = new_center.save()
    stock_count = StockCount(
        count=10,
        asset_category_id=category.id,
        center_id=center.id,
        token_id=user.token_id,
        week=1)
    return stock_count


@pytest.fixture(scope='module')
def stock_count_data(app, new_stock_count):
    """Fixture for a data to create a stock count.
    Args:
        app (object): application
        new_stock_count (object): fixture for a new stock count
    """
    data = {
        'assetCategoryId': new_stock_count.asset_category_id,
        'tokenId': new_stock_count.token_id,
        'centerId': new_stock_count.center_id,
        'week': 1,
        'count': 50
    }
    return data


@pytest.fixture(scope='module')
def save_stock_count(new_spaces, new_user):
    category_one = AssetCategory(name='Owls').save()
    category_two = AssetCategory(name='Broomsticks').save()
    now = dt.datetime.now()
    year, month = get_last_month(now.year, now.month)
    stock_count_data = [{
        'asset_category_id': category_one.id,
        'center_id': new_spaces['centers'][0].id,
        'created_at': dt.datetime(year, month, 16),
        'token_id': new_user.save().token_id,
        'week': 3,
        'count': 30
    },
                        {
                            'asset_category_id': category_one.id,
                            'center_id': new_spaces['centers'][1].id,
                            'created_at': dt.datetime(year, month, 28),
                            'token_id': new_user.save().token_id,
                            'week': 4,
                            'count': 40
                        },
                        {
                            'asset_category_id': category_two.id,
                            'center_id': new_spaces['centers'][0].id,
                            'created_at': dt.datetime(now.year, now.month, 1),
                            'token_id': new_user.save().token_id,
                            'week': 1,
                            'count': 10
                        },
                        {
                            'asset_category_id': category_two.id,
                            'center_id': new_spaces['centers'][1].id,
                            'created_at': dt.datetime(now.year, now.month, 1),
                            'token_id': new_user.save().token_id,
                            'week': 2,
                            'count': 20
                        }]
    return [StockCount(**sc).save() for sc in stock_count_data]
