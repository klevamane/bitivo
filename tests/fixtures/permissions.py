"""Module with permissions fixtures """

# Third Party Modules
import pytest

# Models
from api.models import Permission, ResourceAccessLevel, Resource

# Utilities
from tests.helpers.generate_token import user_one


@pytest.fixture(scope='module')
def new_permissions(app):
    permissions = [
        Permission(type='Add'),
        Permission(type='Edit'),
        Permission(type='Delete'),
        Permission(type='Full Access'),
        Permission(type='No Access'),
    ]
    return permissions


@pytest.fixture(scope='module')
def new_permission(app):
    permission = Permission(type='Edit')
    return permission


@pytest.fixture(scope='function')
def grant_test_user_permissions(app, new_user, new_role):
    """
    Fixture to create a new role and with permission
    Args:
        new_user (object): a new user fixture
        new_role (object): a new role fixture
    """

    def func():
        resource = Resource(name='Permissions')
        resource.save()
        role = new_role.save()
        permission = Permission(type='View')
        permission.save()
        access_level = ResourceAccessLevel(
            role_id=role.id, resource_id=resource.id)
        access_level.permissions = [permission]
        access_level = access_level.save()
        new_user.token_id = user_one.id
        new_user.role = role
        new_user.save()

    return func
