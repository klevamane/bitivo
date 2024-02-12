"""Module with users fixtures """

# Third Party Modules
import pytest
from faker import Faker

# Models
from api.models import User, Role, Permission, Resource, Center, ResourceAccessLevel

# Utilities
from tests.helpers.generate_token import generate_token, user_one, user_two, user_three

# Constants
from tests.mocks.user import USER_LIST, USER_DATA_NEW

# Push ID
from api.models.push_id import PushID

fake = Faker()


@pytest.fixture(scope='module')
def new_user_and_asset_category(app, new_role, test_center_without_users,
                                new_asset_category, new_user):
    """Fixture for new user with valid request token.
       Args:
           app (Flask): Instance of Flask test app.
           new_role (Model): Fixture for role model object.
           test_center_without_users (Model): Fixture for Center model object.
       Returns:
           dict: New user data
       """
    new_role.save()
    new_user.role_id = new_role.id,
    new_user.center_id = test_center_without_users.id

    return new_user, new_asset_category


@pytest.fixture(scope='module')
def new_test_user(app, new_roles, test_center_without_users):
    role = new_roles[-2].save()

    return User(
        **{
            'name': 'Ayo',
            'email': 'test@email.com',
            'image_url': 'http://some_url',
            'role_id': role.id,
            'center_id': test_center_without_users.id,
            'token_id': PushID().next_id()
        })


@pytest.fixture(scope='module')
def user_details(app, new_center, new_custom_role):
    new_custom_role.save()
    new_center.save()
    for user in USER_LIST:
        user['role_id'] = new_custom_role.id
        user['center_id'] = new_center.id
    User.bulk_create(USER_LIST)
    return {'role_id': new_custom_role.id, 'center_id': new_center.id}


@pytest.fixture(scope='module')
def second_user(app, init_db, new_role, test_center_without_users):
    """Fixture for second user

    Args:
        app (object): Instance of Flask test app
        init_db (fixture): Fixture to initialize the test database operations.
        new_role (Model): Fixture for role model object.
        test_center_without_users (Model): Fixture for Center model object.

    Returns:
        User (object): User object
    """
    new_role.save()
    params = {
        'name': 'Sunday',
        'email': 'monday@andela.com',
        'image_url': 'http://some_url',
        'role_id': new_role.id,
        'center_id': test_center_without_users.id,
        'token_id': USER_DATA_NEW['tokenId']
    }
    return User(**params)


@pytest.fixture(scope='module')
def new_mock_user(app, new_role, new_center):
    new_role.save()
    new_center.save()
    params = {
        'name': 'CommentAlien',
        'email': 'testemailnotrequester@andela.com',
        'image_url': 'http://some_url',
        'role_id': new_role.id,
        'center_id': new_center.id,
        'token_id': 'neither-requester-nor-responder'
    }
    return User(**params)


@pytest.fixture(scope='module')
def new_requester(app, new_role, new_center):
    new_role.save()
    new_center.save()
    params = {
        'name': 'CommentRequester',
        'email': 'testemailrequester@andela.com',
        'image_url': 'http://some_url',
        'role_id': new_role.id,
        'center_id': new_center.id,
        'token_id': 'mock-comment-requester-id'
    }
    return User(**params)


@pytest.fixture(scope='module')
def new_responder(app, new_role, new_center):
    new_role.save()
    new_center.save()
    params = {
        'name': 'CommentResponder',
        'email': 'testemailcommentresponder@andela.com',
        'image_url': 'http://some_url',
        'role_id': new_role.id,
        'center_id': new_center.id,
        'token_id': 'mock-comment-responder-id'
    }
    return User(**params)


@pytest.fixture(scope='module')
def new_user(app, new_role, test_center_without_users):
    new_role.save()
    params = {
        'name': 'Ayo',
        'email': 'testemail@andela.com',
        'image_url': 'http://some_url',
        'role_id': new_role.id,
        'center_id': test_center_without_users.id,
        'token_id': user_one.id
    }
    return User(**params)


@pytest.fixture(scope='module')
def test_user(app, new_role_two, test_center_without_users):
    new_role_two.save()
    params = {
        'name': 'Dave',
        'email': 'dave@andela.com',
        'image_url': 'http://some_url',
        'role_id': new_role_two.id,
        'center_id': test_center_without_users.id,
        'token_id': user_three.id
    }
    return User(**params)

@pytest.fixture(scope='module')
def get_first_user(app, new_role):
    new_role.save()
    params = {
        'name': 'Ayo',
        'email': fake.email(),
        'image_url': 'http://some_url',
        'role_id': new_role.id,
        'token_id': user_one.id
    }
    return User(**params).save()


@pytest.fixture(scope='module')
def new_user_two(app, default_role, test_center_without_users):
    default_role.save()
    params = {
        'name': 'Mary',
        'email': 'testemailer@andela.com',
        'image_url': 'http://some_url',
        'role_id': default_role.id,
        'center_id': test_center_without_users.id,
        'token_id': user_two.id
    }
    return User(**params)


@pytest.fixture(scope='module')
def new_user_three(app, new_role, test_center_without_users):
    new_role.save()
    params = {
        'name': 'Joe',
        'email': 'newtestemail@andela.com',
        'image_url': 'http://some_url',
        'role_id': new_role.id,
        'center_id': test_center_without_users.id,
        'token_id': user_three.id
    }
    return User(**params)


@pytest.fixture(scope='module')
def new_work_order_user(app, new_role, new_center):
    new_role.save()
    new_center.save()
    params = {
        'name': 'Mary',
        'email': 'testemailer@andela.com',
        'image_url': 'http://some_url',
        'role_id': new_role.id,
        'center_id': new_center.id,
        'token_id': user_two.id
    }
    return User(**params)


@pytest.fixture(scope='module')
def new_request_user(app, new_role, test_center_without_users):
    new_role.save()
    params = {
        'name': 'Richie',
        'email': 'testmail@andela.com',
        'image_url': 'http://some_url',
        'role_id': new_role.id,
        'center_id': test_center_without_users.id,
        'token_id': PushID().next_id()
    }
    return User(**params)


@pytest.fixture(scope='function')
def revoke_test_user_permissions(app):
    """
    Fixture to change role of a new user
    """

    def func():
        role = Role(
            title='Assets Lead',
            description='reports to the operations coordinator')
        role.save()
        user = User.query_().filter_by(token_id=user_one.id).first()
        user.role = role
        user.save()

    return func


@pytest.fixture(scope='function')
def assignee_details(new_user, new_space):
    def func(assignee_type='user', **kwargs):
        assignee_types = {
            'user': {
                'assigneeId': new_user.token_id,
                'assigneeType': 'user'
            },
            'space': {
                'assigneeId': new_space.id,
                'assigneeType': 'space'
            }
        }
        result = assignee_types.get(assignee_type)
        result.update(**kwargs)
        return result

    return func


@pytest.fixture(scope='module')
def user_with_role(app):
    new_role = Role(title=fake.first_name(), description=fake.sentence())
    center_data = {
        'name': fake.name(),
        'image': {
            'url': fake.image_url(width=None, height=None)
        }
    }
    new_center = Center(**center_data)
    new_permission = Permission(type="Add")
    new_resource = Resource(name=fake.name())

    new_center.save()  # create new center
    new_role.save()  # create new role
    new_permission.save()  # create new permission
    new_resource.save()  # create new resource

    center_id = new_center.id
    role_id = new_role.id
    resource_id = new_resource.id

    new_resource_access_level = ResourceAccessLevel(
        role_id=role_id,
        resource_id=resource_id,
        resource=new_resource,
        permissions=[new_permission])
    new_role.resource_access_levels = [new_resource_access_level]
    new_role.save()

    user_data = {  # new user-data having new center id and new role id
        'name': fake.first_name(),
        'email': 'tester@andela.com',
        'token_id': PushID().next_id(),
        'email': f'{fake.first_name()}@andela.com'.lower(),
        'image_url': fake.image_url(),
        'role_id': role_id,
        'center_id': center_id,
        'created_by': '-Lsdi97y6uyeABD5S'
    }
    new_user_with_role = User(**user_data)  # create new user
    return new_user_with_role, role_id


@pytest.fixture(scope='function')
def save_assignees(new_user, new_space):
    new_space.save()
    new_user.save()
    yield
