"""Module with hot desk request fixtures """

# Third Party Modules
import pytest

from datetime import datetime

# Mock
from unittest.mock import Mock

# models
from api.models import HotDeskResponse

# Database
from ..conftest import db

# Enum
from api.utilities.enums import HotDeskResponseStatusEnum


@pytest.fixture(scope='module')
def new_hot_desk_response(app, init_db, new_user, new_hot_desk_request):
    """Fixture for hot desk request
    Args:
        app (Flask): Instance of Flask test app
        new_user(object): new user object
        new_hot_desk_request(object): new hot desk request object
        init_db (object): Initialize the test database
    Returns:
        new_hot_desk_response(obj): hot desk fixture
    """
    new_user.save()
    new_hot_desk_request.save()
    params = {
        'created_at': datetime.today(),
        'status': HotDeskResponseStatusEnum.pending,
        'assignee_id': new_hot_desk_request.assignee_id,
        'hot_desk_request_id': new_hot_desk_request.id,
    }
    return HotDeskResponse(**params)
