# Standard library
from datetime import date
import random
import string

import pytest

from api.models import AssetRepairLog
from api.utilities.enums import RepairLogStatusEnum


def generate_tag():
    """Function to generate a random tag string
    Args:
        None
    Returns:
        tag(str): a random string as tag
    """
    tag = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(10))
    return tag


@pytest.fixture(scope='function')
def new_asset_repair_log(app, init_db, new_user, new_asset, request_ctx,
                         mock_request_two_obj_decoded_token):
    """Fixture for a new asset repair log
    Args:
        app (Flask): Instance of Flask test app
        new_user(object): new user object
        new_asset(object): new asset
        init_db (object): Initialize the test database
    Returns:
        new_asset_repair_log(obj): asset repair log fixture
    """
    new_user.save()
    new_asset.tag = generate_tag()
    new_asset.save()
    params = {
        'created_at': '2019-03-12 00:00:00',
        'asset_id': new_asset.id,
        'repairer': "Repairer",
        'defect_type': "Cracked screen",
        'date_reported': '2019-03-12 00:00:00',
        'issue_description': "Need Screen fixed",
        'status': RepairLogStatusEnum.open,
        'expected_return_date': '2019-09-12 00:00:00',
        'created_by': new_user.token_id
    }
    return AssetRepairLog(**params)

@pytest.fixture(scope='function')
def new_asset_repair_log_three(app, init_db, new_user, new_asset_for_asset_note, request_ctx,
                         mock_request_two_obj_decoded_token):
    """Fixture for a new asset repair log
    Args:
        app (Flask): Instance of Flask test app
        new_user(object): new user object
        new_asset_for_asset_note(object): new asset
        init_db (object): Initialize the test database
    Returns:
        new_asset_repair_log(obj): asset repair log fixture
    """
    new_user.save()
    new_asset_for_asset_note.tag = generate_tag()
    new_asset_for_asset_note.save()
    params = {
        'created_at': '2019-03-12 00:00:00',
        'asset_id': new_asset_for_asset_note.id,
        'repairer': "Repairer",
        'defect_type': "Cracked screen",
        'date_reported': '2019-03-12 00:00:00',
        'issue_description': "Need Screen fixed",
        'status': RepairLogStatusEnum.open,
        'expected_return_date': '2019-09-12 00:00:00',
        'created_by': new_user.token_id
    }
    return AssetRepairLog(**params)


@pytest.fixture(scope='function')
def asset_repair_log_two(app, init_db, client, new_asset, new_user_two,
                         mock_request_two_obj_decoded_token, request_ctx):
    """Fixture for asset repair log object
    Args:
        app (Flask): Instance of Flask test app
        new_user(object): new user object
        new_user_two(object): new user two object
        new_asset(object): new asset
        init_db (object): Initialize the test database
    Returns:
        repair_log(obj): asset repair log fixture
    """
    new_user_two.save()
    new_asset.tag = generate_tag()
    new_asset.save()
    repair_log = {
        'created_by': '-sjhES374n6-87nb7h',
        'repairer': "Repairer",
        "asset_id": new_asset.id,
        "issue_description": "Requires repainting",
        'defect_type': "Cracked screen",
        'date_reported': '2019-03-12 00:00:00',
        "expected_return_date": date.today().strftime('%Y-%m-%d')
    }
    return repair_log


@pytest.fixture(scope='function')
def asset_repair_log(app, init_db, client, new_asset, new_user_two,
                     mock_request_two_obj_decoded_token, request_ctx):
    """Fixture for asset repair log object
    Args:
        app (Flask): Instance of Flask test app
        new_user(object): new user object
        new_user_two(object): new user two object
        new_asset(object): new asset
        init_db (object): Initialize the test database
    Returns:
        repair_log(obj): asset repair log fixture
    """
    new_user_two.save()
    new_asset.tag = generate_tag()
    new_asset.save()
    repair_log = {
        'repairer': "Repairer",
        "assetId": new_asset.id,
        "issueDescription": "Requires repainting",
        'defect_type': "Cracked screen",
        'date_reported': '2019-03-12 00:00:00',
        "expectedReturnDate": date.today().strftime('%Y-%m-%d')
    }
    return repair_log
