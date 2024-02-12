"""Module with work orders fixtures """
from datetime import datetime

# Third Party Modules
import pytest

# Database
from api.models.database import db

# Models
from api.models import AssetWarranty


@pytest.fixture(scope='module')
def new_asset_warranty(init_db, new_asset_for_asset_warranty, new_user):
    """ Fixture for a new asset warranty """
    new_asset_for_asset_warranty.save()
    return AssetWarranty(
        start_date='2011-08-12',
        end_date='2019-08-12',
        asset_id=new_asset_for_asset_warranty.id,
        created_by=new_user.token_id)


@pytest.fixture(scope='module')
def asset_warranty_for_delete(init_db, new_asset_for_asset_warranty):
    """ Fixture for a new asset warranty """
    new_asset_for_asset_warranty.save()
    return AssetWarranty(asset_id=new_asset_for_asset_warranty.id)
