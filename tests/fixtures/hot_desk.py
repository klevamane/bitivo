"""Module with hot desk request fixtures """

# Standard library
from datetime import datetime

# Third Party Modules
import pytest
import datetime
# Mock
from unittest.mock import Mock

# models
from api.models import HotDeskRequest

# Database
from ..conftest import db

# GoogleSheetHelper
from bot.utilities.google_sheets.google_sheets_helper import GoogleSheetHelper

# Enum
from api.utilities.enums import HotDeskRequestStatusEnum


@pytest.fixture(scope='function')
def mock_google_sheets_api_call(monkeypatch):
    """Fixture for monkey patching google sheets api call
    Args:
        monkeypatch

    Return:
        None
    """
    sheet = Mock(return_value=[{'cell': 'value'}])
    response = ({}, sheet)

    def return_sheet():
        return [{"value": "etc"}]

    sheet.range = Mock(return_value=[{"value": "etc"}] or return_sheet)
    sheet.update_cells = Mock(return_value=None)
    monkeypatch.setattr(GoogleSheetHelper, 'open_sheet', lambda self: response)


@pytest.fixture(scope='function')
def mock_sheet_update(monkeypatch, mock_google_sheets_api_call):
    """Fixture for monkey patching sheet object update api call
    Args:
        monkeypatch

    Return:
        None
    """

    def return_sheet_update():
        return None

    sheet_data, sheet = GoogleSheetHelper().open_sheet()
    monkeypatch.setattr(sheet, 'update', return_sheet_update)


@pytest.fixture(scope='module')
def new_hot_desk_request(app, init_db, new_user, new_user_two):
    """Fixture for hot desk request
    Args:
        app (Flask): Instance of Flask test app
        new_user(object): new user object
        init_db (object): Initialize the test database
    Returns:
        new_hot_desk_request(obj): hot desk fixture
    """
    new_user.save()
    new_user_two.save()
    params = {
        'requester_id': new_user.token_id,
        'status': HotDeskRequestStatusEnum.pending,
        'created_at':
        datetime.datetime.now(),
        'hot_desk_ref_no': '1G 65',
        'assignee_id': new_user_two.token_id,
        'reason': ''
    }
    return HotDeskRequest(**params)


@pytest.fixture(scope='module')
def new_today_hot_desk(app, init_db, new_user, new_user_two):
    """Fixture for hot desk request
    Args:
        app (Flask): Instance of Flask test app
        new_user(object): new user object
        init_db (object): Initialize the test database
    Returns:
        new_hot_desk_request(obj): hot desk fixture
    """
    new_user.save()
    new_user_two.save()
    params = {
        'created_at': datetime.datetime.now(),
        'requester_id': new_user.token_id,
        'status': HotDeskRequestStatusEnum.approved,
        'hot_desk_ref_no': '1G 66',
        'assignee_id': new_user_two.token_id,
        'reason': ''
    }
    return HotDeskRequest(**params)


@pytest.fixture(scope='module')
def new_hot_desk_request_with_complaint(app, init_db, new_user, new_user_two):
    """Fixture for hot desk request
    Args:
        app (Flask): Instance of Flask test app
        new_user(object): new user object
        new_user_two(object): another user object
        init_db (object): Initialize the test database
    Returns:
        new_hot_desk_request(obj): hot desk fixture
    """
    new_user.save()
    new_user_two.save()

    params = {
        'created_at': '2019-03-12 00:00:00',
        'requester_id': new_user.token_id,
        'status': HotDeskRequestStatusEnum.cancelled,
        'hot_desk_ref_no': '1G 65',
        'assignee_id': new_user_two.token_id,
        'reason': 'not feeling too well',
        'complaint': 'not feeling too well',
        'complaint_created_at': '2019-05-21 00:00:00'
    }
    return HotDeskRequest(**params)

@pytest.fixture(scope='module')
def new_hot_desk_cancelled(app, init_db, new_user, new_user_two):
    """Fixture for hot desk request
    Args:
        app (Flask): Instance of Flask test app
        new_user(object): new user object
        new_user_two(object): another user object
        init_db (object): Initialize the test database
    Returns:
        new_hot_desk_request(obj): hot desk fixture
    """
    new_user.save()
    new_user_two.save()

    params = {
        'created_at': '2019-03-12 00:00:00',
        'requester_id': new_user.token_id,
        'status': HotDeskRequestStatusEnum.cancelled,
        'hot_desk_ref_no': '1G 80',
        'assignee_id': new_user_two.token_id,
        'reason': 'changed my mind'
    }
    return HotDeskRequest(**params)

@pytest.fixture(scope='module')
def new_hot_desk_request_two(app, init_db, new_user, new_user_two):
    """Fixture for hot desk request
    Args:
        app (Flask): Instance of Flask test app
        new_user(object): new user object
        init_db (object): Initialize the test database
    Returns:
        new_hot_desk_request(obj): hot desk fixture
    """
    new_user.save()
    new_user_two.save()
    params = {
        'created_at': '2019-04-12 00:00:00',
        'requester_id': new_user.token_id,
        'status': HotDeskRequestStatusEnum.pending,
        'hot_desk_ref_no': '1G 66',
        'assignee_id': new_user_two.token_id,
        'reason': ''
    }
    return HotDeskRequest(**params)

@pytest.fixture(scope='module')
def new_hot_desk_request_three(app, init_db, new_user, new_user_two):
    """Fixture for hot desk request
    Args:
        app (Flask): Instance of Flask test app
        new_user(object): new user object
        init_db (object): Initialize the test database
    Returns:
        new_hot_desk_request(obj): hot desk fixture
    """
    new_user.save()
    new_user_two.save()
    params = {
        'created_at': datetime.datetime.utcnow(),
        'requester_id': new_user.token_id,
        'status': HotDeskRequestStatusEnum.pending,
        'hot_desk_ref_no': '1k 69',
        'assignee_id': new_user_two.token_id,
        'reason': ''
    }
    return HotDeskRequest(**params)

@pytest.fixture(scope='module')
def test_hot_desk_request(app, init_db, new_user_two, new_user_three):
    """Fixture for hot desk request
    Args:
        app (Flask): Instance of Flask test app
        new_user(object): new user object
        init_db (object): Initialize the test database
    Returns:
        new_hot_desk_request(obj): hot desk fixture
    """
    new_user_three.save()
    new_user_two.save()

    params = {
        'created_at': datetime.datetime.now(),
        'requester_id': new_user_three.token_id,
        'status': HotDeskRequestStatusEnum.pending,
        'hot_desk_ref_no': '1G 65',
        'assignee_id': new_user_two.token_id,
        'reason': ''
    }
    return HotDeskRequest(**params)


@pytest.fixture(scope='module')
def approved_hot_desk_request(app, init_db, new_user, new_user_two):
    """Fixture for hot desk request
    Args:
        app (Flask): Instance of Flask test app
        new_user(object): new user object
        init_db (object): Initialize the test database
    Returns:
        new_hot_desk_request(obj): hot desk fixture
    """
    new_user.save()
    new_user_two.save()
    params = {
        'requester_id': new_user.token_id,
        'status': HotDeskRequestStatusEnum.approved,
        'hot_desk_ref_no': '1G 65',
        'assignee_id': new_user_two.token_id,
        'hot_desk_ref_no':
        '1G 65',
        'created_at':
        datetime.datetime.now()
    }
    return HotDeskRequest(**params)


@pytest.fixture(scope='module')
def hot_desk_with_invalid_assignee_id(app, init_db, new_user):
    """Fixture for hot desk with invalid assignee_id
    Args:
        app (Flask): Instance of Flask test app
        new_user(object): new user object
        init_db (object): Initialize the test database
    Returns:
        hot_desk_with_invalid_assignee_id(obj): hot desk fixture with
                                          invalid assignee id
    """
    new_user.save()

    params = {
        'requester_id': new_user.token_id,
        'status': 'pending',
        'hot_desk_ref_no': '1G 65',
        'assignee_id': "XXXXX"
    }
    return HotDeskRequest(**params)


@pytest.fixture(scope='module')
def hot_desk_with_invalid_requster_id(app, init_db, new_user):
    """Fixture for hot desk with invalid email
    Args:
        app (Flask): Instance of Flask test app
        new_user(object): new user object
        init_db (object): Initialize the test database
    Returns:
        hot_desk_with_invalid_email(obj): hot desk fixture with
                                          invalid email
    """

    db.session.rollback()
    new_user.save()

    params = {
        "requester_id": "invalid",
        'status': 'pending',
        'hot_desk_ref_no': '1G 65',
        'assignee_id': new_user.token_id
    }
    return HotDeskRequest(**params)


@pytest.fixture(scope='module')
def hot_desk_with_missing_fields(app, init_db, new_user):
    """Fixture for hot desk with missing fields
    Args:
        app (Flask): Instance of Flask test app
        init_db (object): Initialize the test database
    Returns:
        hot_desk_with_missing_fields(obj): hot desk fixture with
                                          missing fields
    """

    db.session.rollback()
    new_user.save()

    params = {
        'requester_id': new_user.token_id,
        'status': 'pending',
        'hot_desk_ref_no': '1G 65'
    }
    return HotDeskRequest(**params)


@pytest.fixture(scope='module')
def multiple_approved_hot_desk_request(app, init_db,
                                       approved_hot_desk_request):
    """Fixture for multiple approved hot desk request
    Args:
        app (Flask): Instance of Flask test app
        init_db(object): Initialize the db
        approved_hot_desk_request (object): Fixture for hot desk request
    Returns:
        new_hot_desk_request(obj): hot desk fixture
    """

    return [approved_hot_desk_request.save() for i in range(0, 5)]
