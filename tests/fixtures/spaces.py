"""Module with spaces fixtures """

# Third Party Modules
import pytest

# Models
from api.models import Space, Center


@pytest.fixture(scope='module')
def new_space_two(app, new_space_type_store1, new_center, new_user):
    new_user.save()
    new_space_type_store1.save()
    new_center.save()
    space = Space(
        name='Epic',
        parent_id=None,
        space_type_id=new_space_type_store1.id,
        center_id=new_center.id,
        created_by='-Lsdi97y6uyeABD5S')
    return space


@pytest.fixture(scope='module')
def new_space(app, new_space_type, new_center, new_user):
    new_space_type.save()
    new_center.save()
    space = Space(
        name='Epic Tower',
        parent_id=None,
        space_type_id=new_space_type.id,
        center_id=new_center.id,
        created_by=new_user.token_id)
    return space


@pytest.fixture(scope='function')
def custom_space():
    def func(params):
        space = Space(**params)
        space.save()
        return space

    return func


@pytest.fixture(scope='module')
def new_space2(app, new_space_type2, new_center, new_space):
    new_space_type2.save()
    new_center.save()
    new_space.save()
    space2 = Space(
        name='First Floor',
        parent_id=new_space.id,
        space_type_id=new_space_type2.id,
        center_id=new_center.id)
    return space2


@pytest.fixture(scope='function')
def update_space(app, new_spaces, new_space_types, new_user):
    centers = new_spaces['centers']
    spaces = new_spaces['spaces']
    space_types = new_space_types

    space = Space(
        name="First Floor",
        center_id=centers[0].id,
        space_type_id=space_types[1].id,
        parent_id=spaces[0].id)

    Space(
        name="Ground Floor",
        center_id=centers[0].id,
        space_type_id=space_types[1].id,
        parent_id=spaces[0].id,
        created_by=new_user.token_id).save()

    return space


@pytest.fixture(scope='module')
def new_space_store(app, new_space_type_store, new_center, new_space):
    new_space_type_store.save()
    lagos_center = Center(name="Lagos", image={'url': 'image.com/url'}) \
        .save()
    new_space.save()
    space_store = Space(
        name='ET Store',
        parent_id=new_space.id,
        space_type_id=new_space_type_store.id,
        center_id=lagos_center.id)
    return space_store


@pytest.fixture(scope='module')
def new_spaces(app, new_space_types, new_user):
    new_user.save()
    lagos_center = Center(name="Lagos", image={'url': 'image.com/url'}).save()

    nairobi_center = Center(
        name="Nairobi", image={
            'url': 'image.com/url'
        }).save()

    for space_type in new_space_types:
        space_type.save()

    epic_tower = Space(
        name='Epic Tower',
        space_type_id=new_space_types[0].id,
        center_id=lagos_center.id).save()

    fourth_floor = Space(
        name='Fourth Floor',
        parent_id=epic_tower.id,
        space_type_id=new_space_types[1].id,
        center_id=lagos_center.id).save()

    left_wing = Space(
        name='Left Wing',
        parent_id=fourth_floor.id,
        space_type_id=new_space_types[2].id,
        center_id=lagos_center.id).save()

    wall_street = Space(
        name='Wall Street',
        parent_id=left_wing.id,
        space_type_id=new_space_types[3].id,
        center_id=lagos_center.id).save()

    fun_tower = Space(
        name='Fun Tower',
        space_type_id=new_space_types[0].id,
        center_id=nairobi_center.id).save()

    Naija = Space(
        name='Ops Store',
        space_type_id=new_space_types[0].id,
        center_id=lagos_center.id).save()

    return {
        "centers": [lagos_center, nairobi_center],
        "spaces":
        [epic_tower, fourth_floor, left_wing, wall_street, fun_tower, Naija]
    }
