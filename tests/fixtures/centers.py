"""Module with canters fixtures """

# Third Party Modules
import pytest
from faker import Faker

# Database
from api.models.database import db

# Models
from api.models import Center, User

# Push ID
from api.models.push_id import PushID

# Utilities
from api.utilities.helpers.random_string_gen import gen_string

# Mocks
from tests.mocks.center import VALID_CENTER_FOR_DELETE

fake = Faker()


@pytest.fixture(scope='module')
def test_center_without_users():
    """A center without users for testing."""
    center = Center(name=gen_string(), image=dict(metadata=gen_string()))
    center = center.save()
    return center


@pytest.fixture(scope='module')
def test_deleted_center():
    """A deleted center without users for testing."""
    center = Center(
        name=gen_string(), image=dict(metadata=gen_string()), deleted=True)
    center = center.save()
    return center


@pytest.fixture(scope='module')
def new_center(app, init_db):
    params = {
        'name': fake.name(),
        'image': {
            'url': fake.image_url(width=None, height=None),
            'public_id': 'fr4mxeqx5zb8rlakpfku'
        },
    }
    return Center(**params)


@pytest.fixture(scope='module')
def new_custom_center(app, new_user):
    def func(params):
        new_user.save()
        center = Center(**params)
        return center

    return func


@pytest.fixture(scope='function')
def test_center(app, new_user):
    """
    Create a center instance for testing
    """
    VALID_CENTER_FOR_DELETE['created_by'] = new_user.token_id
    center = Center(**VALID_CENTER_FOR_DELETE)

    center = center.save()
    yield center

    db.session.delete(center)
    db.session.commit()


@pytest.fixture(scope='module')
def test_center_with_users(new_role, new_user):
    """A center with users for testing."""
    new_user.save()
    new_role.save()
    center = Center(name=gen_string(), image=dict(metadata=gen_string()))
    center = center.save()
    for i in range(5):
        db.session.add(
            User(
                id=gen_string(),
                name=gen_string(),
                email=gen_string() + '@andela.com',
                token_id=PushID().next_id(),
                image_url=gen_string(10),
                role_id=new_role.id,
                center_id=center.id))
    db.session.commit()
    return center


@pytest.fixture(scope='module')
def test_center_with_deleted_users(new_role):
    """A center with users for testing."""
    new_role.save()
    center = Center(name=gen_string(), image=dict(metadata=gen_string()))
    center = center.save()
    for i in range(5):
        db.session.add(
            User(
                id=gen_string(),
                name=gen_string(),
                email=gen_string() + '@andela.com',
                token_id=PushID().next_id(),
                image_url=gen_string(10),
                role_id=new_role.id,
                center_id=center.id),
            deleted=True)
    db.session.commit()
    return center


@pytest.fixture(scope='module')
def test_center_with_deleted_users(new_role):
    """A center with deleted users for testing."""
    new_role.save()
    center = Center(name=gen_string(), image=dict(metadata=gen_string()))
    center = center.save()
    for i in range(3):
        db.session.add(
            User(
                id=gen_string(),
                deleted=True,
                name=gen_string(),
                email=gen_string() + '@andela.com',
                image_url=gen_string(10),
                token_id=PushID().next_id(),
                role_id=new_role.id,
                center_id=center.id))
    db.session.commit()
    return center
