"""Module with roles fixtures """

# Third Party Modules
import pytest
from faker import Faker

# Models
from api.models import Role

fake = Faker()


@pytest.fixture(scope='module')
def new_roles(app, new_user):
    new_user.save()
    roles = [
        Role(
            title='Operations Intern',
            description='reports to the operations coordinator'),
        Role(
            title='Operations Coordinator',
            description='reports to the operations assistant'),
        Role(
            title='Operations Assistant',
            description='reports to the operations manager'),
        Role(
            title='Operations Associate',
            description='reports to the operations assistant'),
        Role(
            title='Operations Manager',
            description='reports to the operations director'),
    ]
    return roles


@pytest.fixture(scope='module')
def new_custom_role(app, new_user):
    return Role(
        title=fake.first_name(),
        description=fake.sentence(),
        created_by=new_user.token_id)


@pytest.fixture(scope='module')
def new_role(app, new_permissions):
    new_permissions[4].save()
    role = Role(
        title='Operations Intern',
        description='reports to the operations coordinator',
        super_user=True)
    return role


@pytest.fixture(scope='module')
def new_role_two(app, new_permissions):
    new_permissions[4].save()
    role = Role(
        title='Office Intern',
        description='reports to the operations coordinator')
    return role


@pytest.fixture(scope='module')
def duplicate_role(app):
    role = Role(
        title='Operations Assistant Manager',
        description='reports to the operations manager')
    return role


@pytest.fixture(scope='module')
def duplicate_role2(app, new_user):
    role = Role(
        title='Operations Intern',
        description='reports to the operations coordinator',
        created_by=new_user.token_id)
    return role


@pytest.fixture(scope='module')
def default_role(app):
    """Fixture for creating default role for users
    Args:
        app (Flask): Instance of Flask test app
    Returns:
        Role: Object of the default role to be created
    """

    params = {'title': 'Regular User', 'description': 'default user'}
    return Role(**params).save()
