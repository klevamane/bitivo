"""Module with asset insurance fixtures """
import datetime

# Third Party Modules
import pytest

# Models
from api.models import AssetInsurance

# Constants
# from tests.mocks.requests import VALID_ATTACHMENTS


@pytest.fixture(scope='module')
def new_asset_insurance(app, init_db, new_asset_for_asset_note, new_user):
    """Fixture for creating a new asset insurance

        Args:
            app (object): Instance of Flask test app
            init_db (fixture): Fixture to initialize the test database operations.
            new_asset_for_asset_note (Asset): Instance of an asset

        Returns:
            asset insurance (AssetInsurance): Object of the asset insurance created
    """
    new_asset_for_asset_note.save()
    return AssetInsurance(
        company="Some Company",
        start_date='2019-01-01',
        end_date=datetime.date.today() + datetime.timedelta(days=10),
        asset_id=new_asset_for_asset_note.id,
        created_by=new_user.token_id)
