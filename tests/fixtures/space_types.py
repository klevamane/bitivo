"""Module with space types fixtures """

# Third Party Modules
import pytest

# Models
from api.models import SpaceType


@pytest.fixture(scope='module')
def new_space_types(app, new_user):
    new_user.save()
    space_types = [
        SpaceType(type='Building', color='Blue'),
        SpaceType(type='Floor', color='Orange'),
        SpaceType(type='Wing', color='Green'),
        SpaceType(type='Space', color='Yellow')
    ]
    return space_types


@pytest.fixture(scope='function')
def custom_space_type():
    def func(params):
        space_type = SpaceType(**params)
        space_type.save()
        return space_type

    return func


@pytest.fixture(scope='module')
def new_space_type(app):
    space_type = SpaceType(type='Building', color='Red')
    return space_type


@pytest.fixture(scope='module')
def new_space_type_store1(app, new_user):
    new_user.save()
    space_type = SpaceType(type='Store', color='Brown')
    return space_type


@pytest.fixture(scope='module')
def new_space_type2(app):
    space_type2 = SpaceType(type='Floor', color='Green')
    return space_type2


@pytest.fixture(scope='module')
def new_space_type_store(app):
    space_type_store = SpaceType(type='Store', color='Gray')
    return space_type_store


@pytest.fixture(scope='module')
def new_space_type2(app):
    space_type2 = SpaceType(type='Floor', color='Green')
    return space_type2
