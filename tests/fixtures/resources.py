"""Module with resources fixtures """

# Third Party Modules
import pytest

# Models
from api.models import Resource


@pytest.fixture(scope='module')
def new_resource(app):
    """
    Fixture for a resource.
    """
    resource = Resource(name='Assets')
    return resource


@pytest.fixture(scope='module')
def new_resources(app):
    """
    Fixture for resources
    """
    resources = [
        Resource(name='Assets'),
        Resource(name='Centers'),
        Resource(name='Permissions'),
        Resource(name="Requests"),
        Resource(name="Request Types"),
        Resource(name="People"),
        Resource(name="Spaces"),
        Resource(name="History"),
        Resource(name="Asset Categories"),
        Resource(name="Roles"),
        Resource(name="Stock Count")
    ]
    return resources
