"""Module with requests fixtures """

# System libraries
import json
from datetime import datetime, timedelta

# Third Party Modules
import pytest

# Models
from api.models import Request

# Constants
from tests.mocks.requests import VALID_ATTACHMENTS


@pytest.fixture(scope='module')
def new_request(app, init_db, new_user, new_center, new_request_type):
    """Fixture for creating a new request

        Args:
            app (object): Instance of Flask test app
            init_db (fixture): Fixture to initialize the test database operations.
            new_user (User): Instance of a user
            new_center (Center): Instance of a center
            new_request_type (RequestType): Instance of a Request Type

        Returns:
            request (Request): Object of the request created
    """
    new_user.save()
    new_center.save()
    new_request_type.save()

    request_one = Request(
        subject='my iphone screen cracked',
        request_type_id=new_request_type.id,
        center_id=new_user.center_id,
        description='''Some randomly long description about the imaginary
        iphone that got broken''',
        requester_id=new_user.token_id,
        responder_id=new_user.token_id,
        status='open',
        closed_by_system=False,
        attachments=VALID_ATTACHMENTS,
        created_by=new_user.token_id)

    return request_one


def create_expired_request(new_user, new_center, new_request_type):
    """Returns an expired Request object

    Args:
        new_user (User): Instance of a user
        new_center (Center): Instance of a center
        new_request_type (RequestType): Instance of a Request Type


    Returns:
        request (Request): Object of the created request
    """
    closure_time = new_request_type.closure_time
    delta = timedelta(**closure_time) + timedelta(seconds=1)

    return Request(
        subject='expired request',
        request_type_id=new_request_type.id,
        center_id=new_center.id,
        description='''This request is expired
            This means that it is completed and its closure time has been exceeded
            The system should automatically closed these kinds of requests''',
        requester_id=new_user.token_id,
        responder_id=new_user.token_id,
        status='completed',
        completed_at=datetime.now() - delta,
        closed_by_system=False,
        attachments=VALID_ATTACHMENTS)


@pytest.fixture(scope='module')
def new_expired_request(app, init_db, new_user, new_center, new_request_type):
    """Fixture for creating a new request

        Args:
            app (object): Instance of Flask test app
            init_db (fixture): Fixture to initialize the test database operations.
            new_user (User): Instance of a user
            new_center (Center): Instance of a center
            new_request_type (RequestType): Instance of a Request Type

        Returns:
            request (Request): Object of the created request
    """
    new_user.save()
    new_center.save()
    new_request_type.save()

    return create_expired_request(new_user, new_center, new_request_type)


@pytest.fixture(scope='module')
def new_expired_requests(app, init_db, new_user, new_center, new_request_type):
    """Fixture for creating a new request

        Args:
            app (object): Instance of Flask test app
            init_db (fixture): Fixture to initialize the test database operations.
            new_user (User): Instance of a user
            new_center (Center): Instance of a center
            new_request_type (RequestType): Instance of a Request Type

        Returns:
            request (Request): Object of the created request
    """
    new_user.save()
    new_center.save()
    new_request_type.save()
    expired_requests = []

    for i in range(6):
        expired_requests.append(
            create_expired_request(new_user, new_center, new_request_type))

    return expired_requests


@pytest.fixture(scope='module')
def open_request(app, init_db, new_user, new_request_user, new_center,
                 new_request_type):
    """Fixture for creating a user request which has an open status

        Args:
            app (object): Instance of Flask test app
            init_db (fixture): Fixture to initialize the test database operations.
            new_user (User): Instance of a user
            new_center (Center): Instance of a center
            new_request_type (RequestType): Instance of a Request Type

        Returns:
            request (Request): Object of the created request
    """
    new_user.save()
    new_request_user.save()
    new_center.save()
    new_request_type.save()

    request_one = Request(
        subject='my iphone screen cracked',
        request_type_id=new_request_type.id,
        center_id=new_center.id,
        description='''Some very randomly long description about the imaginary
        iphone that got spoilt''',
        responder_id=new_user.token_id,
        requester_id=new_request_user.token_id,
        status='open',
        closed_by_system=False,
        attachments=VALID_ATTACHMENTS)
    return request_one


@pytest.fixture(scope='module')
def new_request_by_requester(app, init_db, new_requester, new_responder,
                             new_center, new_request_type):
    """Fixture for creating a new request

        Args:
            app (object): Instance of Flask test app
            init_db (fixture): Fixture to initialize the test database operations.
            new_user (User): Instance of a user
            new_center (Center): Instance of a center
            new_request_type (RequestType): Instance of a Request Type

        Returns:
            request (Request): Object of the created request
    
    """

    new_requester.save()
    new_responder.save()
    new_center.save()
    new_request_type.save()

    request_one = Request(
        subject='My Request Is for testing',
        request_type_id=new_request_type.id,
        center_id=new_center.id,
        description='''Some very randomly long description about the imaginary
        request that is used for testing''',
        requester_id=new_requester.token_id,
        responder_id=new_responder.token_id,
        status='open',
        closed_by_system=False,
        attachments=VALID_ATTACHMENTS)

    return request_one


@pytest.fixture(scope='module')
def in_progress_request(app, init_db, new_user, new_request_user, new_center,
                        new_request_type):
    """Fixture for a user request with status in_progress

        Args:
            app (object): Instance of Flask test app
            init_db (fixture): Fixture to initialize the test database operations.
            new_user (User): Instance of a user
            new_center (Center): Instance of a center
            new_request_type (RequestType): Instance of a Request Type

        Returns:
            request (Request): Object of the created request
    """
    new_user.save()
    new_request_user.save()
    new_center.save()
    new_request_type.save()

    request_one = Request(
        subject='my iphone screen cracked',
        request_type_id=new_request_type.id,
        center_id=new_center.id,
        description='''Some very randomly long description about the imaginary
        iphone that got spoilt''',
        responder_id=new_user.token_id,
        requester_id=new_request_user.token_id,
        status='in_progress',
        closed_by_system=False,
        attachments=VALID_ATTACHMENTS)

    return request_one


@pytest.fixture(scope='module')
def closed_request(app, init_db, new_user, new_request_user, new_center,
                   new_request_type):
    """Fixture for a user request with status closed

        Args:
            app (object): Instance of Flask test app
            init_db (fixture): Fixture to initialize the test database operations.
            new_user (User): Instance of a user
            new_center (Center): Instance of a center
            new_request_type (RequestType): Instance of a Request Type

        Returns:
            request (Request): Object of the created request
    """
    new_user.save()
    new_request_user.save()
    new_center.save()
    new_request_type.save()

    request_one = Request(
        subject='my iphone screen cracked',
        request_type_id=new_request_type.id,
        center_id=new_center.id,
        description='''Some very randomly long description about the imaginary
        iphone that got spoilt''',
        responder_id=new_user.token_id,
        requester_id=new_request_user.token_id,
        status='closed',
        closed_by_system=False,
        attachments=VALID_ATTACHMENTS)

    return request_one


@pytest.fixture(scope='module')
def completed_request(app, init_db, new_user, new_request_user, new_center,
                      new_request_type):
    """Fixture for a user request with status completed

        Args:
            app (object): Instance of Flask test app
            init_db (fixture): Fixture to initialize the test database operations.
            new_user (User): Instance of a user
            new_center (Center): Instance of a center
            new_request_type (RequestType): Instance of a Request Type

        Returns:
            request (Request): Object of the created request
    """
    new_user.save()
    new_request_user.save()
    new_center.save()
    new_request_type.save()

    request_one = Request(
        subject='my iphone screen cracked',
        request_type_id=new_request_type.id,
        center_id=new_center.id,
        description='''Some very randomly long description about the imaginary
        iphone that got spoilt''',
        responder_id=new_user.token_id,
        requester_id=new_request_user.token_id,
        status='completed',
        closed_by_system=False,
        attachments=VALID_ATTACHMENTS)

    return request_one


@pytest.fixture(scope='module')
def request_list(app, init_db, new_user, new_center, new_request_type):
    """Fixture for creating a new request

        Args:
            app (object): Instance of Flask test app
            init_db (fixture): Fixture to initialize the test database operations.
            new_user (User): Instance of a user
            new_center (Center): Instance of a center
            new_request_type (RequestType): Instance of a Request Type

        Returns:
            requests(List): List of created requests
    """

    new_user.save()
    new_center.save()
    new_request_type.save()
    request_attachments = [
        json.dumps({"image_url": f"https://somerandomimage.com/image{x}.jpg"})
        for x in range(3)
    ]
    requests = [{
        'subject': f'Laptop{x} not starting up',
        'request_type_id': new_request_type.id,
        'center_id': new_center.id,
        'description':
        f'My laptop{x} is not starting up. I really do not know why',
        'attachments': request_attachments,
        'requester_id': new_user.token_id,
        'responder_id': new_user.token_id
    } for x in range(5)]
    return Request.bulk_create(requests)


@pytest.fixture(scope='function')
def create_new_request(app, init_db, new_user, new_center,
                       new_request_type_two):
    """Fixture for creating a new request

        Args:
            app (object): Instance of Flask test app
            init_db (fixture): Fixture to initialize the test database operations.
            new_user (User): Instance of a user
            new_center (Center): Instance of a center
            new_request_type (RequestType): Instance of a Request Type

        Returns:
            request (Request): Object of the created request
    """
    user = new_user.save()
    center = new_center.save()
    request_type = new_request_type_two.save()

    request_two = Request(
        subject='my iphone screen cracked',
        request_type_id=request_type.id,
        center_id=center.id,
        description='''Some very randomly long description about the imaginary
        iphone that got spoilt''',
        requester_id=new_user.token_id,
        responder_id=new_user.token_id,
        status='open',
        closed_by_system=False,
        attachments=VALID_ATTACHMENTS,
        created_by=new_user.token_id)

    return request_two


@pytest.fixture(scope='module')
def new_request_responder_update(app, init_db, new_user, new_center,
                                 new_request_type, new_request_user):
    """Fixture for creating a new request for a responder

    Args:
        app (object): Instance of Flask test app
        init_db (fixture): Fixture to initialize the test database operations.
        new_user (User): Instance of a user
        new_center (Center): Instance of a center
        new_request_type (RequestType): Instance of a Request Type

    Returns:
        request (dict): Dictionary of the created request
    """
    new_user.save()
    new_request_user.save()
    new_center.save()
    new_request_type.assignee_id = new_user.token_id
    new_request_type.save()

    request_one = Request(
        subject='my iphone screen cracked',
        request_type_id=new_request_type.id,
        center_id=new_request_type.center_id,
        description='''Some very randomly long description about the imaginary
        iphone that got spoilt''',
        requester_id=new_request_user.token_id,
        attachments=VALID_ATTACHMENTS,
        responder_id=new_user.token_id,
        assignee_id=None,
        status='open',
        closed_by_system=False)
    return request_one


@pytest.fixture(scope='module')
def new_request_requester_update(app, init_db, new_user, new_center,
                                 new_request_type, new_request_user,
                                 new_test_user, new_user_two):
    """Fixture for creating a new request for a requester

    Args:
        app (object): Instance of Flask test app
        init_db (fixture): Fixture to initialize the test database operations.
        new_user (User): Instance of a user
        new_center (Center): Instance of a center
        new_request_type (RequestType): Instance of a Request Type
        new_request_user (User): Instance of a user

    Returns:
        request (dic): Dictionary of the created request
    """
    new_user.save()
    new_test_user.save()
    new_center.save()
    new_request_type.assignee_id = new_test_user.token_id
    new_request_type.save()

    request_one = Request(
        subject='my iphone screen cracked',
        request_type_id=new_request_type.id,
        center_id=new_request_type.center_id,
        description='''Some very randomly long description about the imaginary
        iphone that got spoilt''',
        requester_id=new_user.token_id,
        responder_id=None,
        status='open',
        assignee_id=None,
        closed_by_system=False)

    return request_one


@pytest.fixture(scope='module')
def overdue_requests(app, init_db, new_user, new_center, new_request_type):
    """Fixture for creating a new request

        Args:
            app (object): Instance of Flask test app
            init_db (fixture): Fixture to initialize the test database operations.
            new_user (User): Instance of a user
            new_center (Center): Instance of a center
            new_request_type (RequestType): Instance of a Request Type

        Returns:
            requests(List): List of created requests
    """

    new_user.save()
    new_center.save()
    new_request_type.save()
    request_attachments = [
        json.dumps({"image_url": f"https://somerandomimage.com/image{x}.jpg"})
        for x in range(2)
    ]
    overdue_requests = [{
        'subject': f'Laptop-{x} is slow',
        'request_type_id': new_request_type.id,
        'center_id': new_center.id,
        'due_by': '2018-12-18 00:00:00',
        'description': f'My laptop-{x} is super slow. I don\'t know why',
        'attachments': request_attachments,
        'requester_id': new_user.token_id,
        'responder_id': new_user.token_id
    } for x in range(4)]
    return Request.bulk_create(overdue_requests)
