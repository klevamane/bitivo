"""Module with maintenance categories fixtures """

# Third Party Modules
import pytest

# Models
from api.models import MaintenanceCategory


@pytest.fixture(scope='module')
def new_maintenance_category(app, init_db, test_center_without_users, new_user,
                             new_asset_category):
    """Fixture for creating a maintenance category

    Args:
        app (obj): Instance of Flask test app
        init_db (func): Function to initialize the test database operations.
        new_center (obj): Instance of a center
        new_request_type (obj): Instance of a Request Type

    Returns:
        maintenance_category(obj): Object for maintenance category
    """
    # new_center.save()
    new_user.save()
    new_asset_category.save()

    maintenance_category = MaintenanceCategory(
        title="Servicing",
        asset_category_id=new_asset_category.id,
        center_id=test_center_without_users.id,
        created_by=new_user.token_id)

    return maintenance_category


@pytest.fixture(scope='function')
def duplicate_maintenance_category(app, init_db, new_center,
                                   new_asset_category):
    """Fixture for creating a duplicate maintenance category

    Args:
        app (obj): Instance of Flask test app
        init_db (func): Function to initialize the test database operations.
        new_center (obj): Instance of a center
        new_request_type (obj): Instance of a Request Type

    Returns:
        maintenance_category(obj): Object for maintenance category
    """
    new_center.save()
    new_asset_category.save()

    maintenance_category = MaintenanceCategory(
        title="Maintenance Category",
        asset_category_id=new_asset_category.id,
        center_id=new_center.id)

    return maintenance_category
