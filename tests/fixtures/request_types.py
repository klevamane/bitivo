"""Module with request types fixtures """

# Third Party Modules
import pytest

# Models
from api.models import RequestType

# Constants
from tests.mocks.request_type import (RESPONSE_TIME, RESOLUTION_TIME,
                                      VALID_REQUEST_TYPE_DATA, CLOSURE_TIME)


@pytest.fixture(scope='module')
def new_request_type(app, init_db, new_user):
    """Fixture for creating a new request type

        Args:
            app (object): Instance of Flask test app
            init_db (fixture): Fixture to initialize the test database operations.
            new_user (User): Instance of a user
            new_center (Center): Instance of a center

        Returns:
            request_type (RequestType): Object of the created request type
    """
    new_user.save()

    request_type = RequestType(
        title='test title',
        center_id=new_user.center_id,
        assignee_id=new_user.token_id,
        response_time=RESPONSE_TIME,
        resolution_time=RESOLUTION_TIME,
        closure_time=CLOSURE_TIME,
        created_by=new_user.token_id,
    )

    return request_type


@pytest.fixture(scope='module')
def new_request_type_two(app, init_db, new_user):
    """Fixture for creating a new request type

        Args:
            app (object): Instance of Flask test app
            init_db (fixture): Fixture to initialize the test database operations.
            new_user (User): Instance of a user
            new_center (Center): Instance of a center

        Returns:
            request_type (RequestType): Object of the created request type
    """
    new_user.save()

    request_type = RequestType(
        title='MaintenanceTitle',
        center_id=new_user.center_id,
        assignee_id=new_user.token_id,
        response_time=RESPONSE_TIME,
        resolution_time=RESOLUTION_TIME,
        closure_time=CLOSURE_TIME,
        created_by=new_user.token_id)

    return request_type


@pytest.fixture(scope='module')
def new_request_types(app, init_db, new_user, new_center):
    """Fixture for creating multiple request types.

    Args:
        app (object): Instance of Flask test app
        init_db (fixture): Fixture to initialize the test database operations.
        new_user (User): Instance of a user
        new_center (Center): Instance of a center

    Returns:
        List (RequestType): List of created request types

    """
    new_user.save()
    new_center.save()

    records = [{
        'title': 'test_title',
        'center_id': new_center.id,
        'assignee_id': new_user.token_id,
        'response_time': RESPONSE_TIME,
        'resolution_time': RESOLUTION_TIME,
        'closure_time': CLOSURE_TIME,
    },
               {
                   'title': 'test_title1',
                   'center_id': new_center.id,
                   'assignee_id': new_user.token_id,
                   'response_time': RESPONSE_TIME,
                   'resolution_time': RESOLUTION_TIME,
                   'closure_time': CLOSURE_TIME,
               },
               {
                   'title': 'test_title2',
                   'center_id': new_center.id,
                   'assignee_id': new_user.token_id,
                   'response_time': RESPONSE_TIME,
                   'resolution_time': RESOLUTION_TIME,
                   'closure_time': CLOSURE_TIME,
               },
               {
                   'title': 'test_title3',
                   'center_id': new_center.id,
                   'assignee_id': new_user.token_id,
                   'response_time': RESPONSE_TIME,
                   'resolution_time': RESOLUTION_TIME,
                   'closure_time': CLOSURE_TIME,
               }]

    return [RequestType(**data).save() for data in records]


@pytest.fixture(scope='module')
def new_request_type_two(app, init_db, new_user, new_user_two, new_center):
    """Fixture for creating a new request type

        Args:
            app (object): Instance of Flask test app
            init_db (fixture): Fixture to initialize the test database operations.
            new_user (User): Instance of a user
            new_center (Center): Instance of a center

        Returns:
            request_type (RequestType): Object of the created request type
    """
    new_user.save()
    new_user_two.save()
    new_center.save()

    request_type = RequestType(
        title='test_title_two',
        center_id=new_user.center_id,
        assignee_id=new_user_two.token_id,
        response_time=RESPONSE_TIME,
        resolution_time=RESOLUTION_TIME,
        closure_time=CLOSURE_TIME,
        created_by=new_user.token_id)

    return request_type


@pytest.fixture(scope='module')
def new_request_type_three(app, init_db, new_user, new_user_two,
                           test_center_with_users):
    """Fixture for creating a new request type

        Args:
            app (object): Instance of Flask test app
            init_db (fixture): Fixture to initialize the test database operations.
            new_user (User): Instance of a user
            new_center (Center): Instance of a center

        Returns:
            request_type (RequestType): Object of the created request type
    """
    new_user.save()
    new_user_two.save()
    test_center_with_users.save()

    request_type = RequestType(
        title='test_title_two',
        center_id=test_center_with_users.id,
        assignee_id=new_user_two.token_id,
        response_time=RESPONSE_TIME,
        resolution_time=RESOLUTION_TIME,
        closure_time=CLOSURE_TIME)

    return request_type


@pytest.fixture(scope='function')
def duplicate_request_type(app, init_db, new_user, new_user_two,
                           test_center_with_users):
    """Fixture for creating a new request type

        Args:
            app (object): Instance of Flask test app
            init_db (fixture): Fixture to initialize the test database operations.
            new_user (User): Instance of a user
            new_center (Center): Instance of a center

        Returns:
            request_type (RequestType): Object of the created request type
    """
    new_user.save()
    new_user_two.save()
    test_center_with_users.save()

    request_type = RequestType(
        title='test_title_two',
        center_id=test_center_with_users.id,
        assignee_id=new_user_two.token_id,
        response_time=RESPONSE_TIME,
        resolution_time=RESOLUTION_TIME,
        closure_time=CLOSURE_TIME,
        created_by=new_user.token_id)
    return request_type
