"""Module with resource access levels fixtures """

# Third Party Modules
import pytest

# Models
from api.models import ResourceAccessLevel


@pytest.fixture(scope='module')
def new_resource_access_level(app, new_custom_role, new_permission,
                              new_resource):
    """
    Fixture for a resource access level.
    """
    role = new_custom_role.save()
    permission = new_permission.save()
    resource = new_resource.save()

    access_level = ResourceAccessLevel(
        role_id=role.id, resource_id=resource.id)
    access_level.permissions = [permission]
    return access_level
