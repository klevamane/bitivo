"""Module to seed space table"""

# Model instances
from api.models import Space, SpaceType, Center

# Utilities
from api.utilities.helpers.seeders import clean_seed_data

# Seed data
from .seed_data import get_env_based_data


def save_space_data(name, parent_id, center_id, space_type_id):
    """Function that save an instance of space into the database

    Args:
        name(str): space name
        parent_id(NoneType or str): space parent id
        center_id(str): center id where space is located
        space_type_id(str): space type id

    Returns:
        Each space object saved into the database
    """

    space = Space(
        name=name,
        parent_id=parent_id,
        space_type_id=space_type_id,
        center_id=center_id)
    return space.save()


def seed_space(clean_data=False):
    """Seed space function

    Gets each space data and pass it as an argument for the save_space_data
    function

    Args:
        clean_data (bool): Determines if seed data is to be cleaned.
    """
    # create a variable with empty dict as value
    parent_ids = {}
    # query all space types
    all_space_types = SpaceType.query_().all()
    # map space types to space type id
    space_types = {
        space_type.type: space_type.id
        for space_type in all_space_types
    }
    center_id_mapper = {
        center.name: center.id
        for center in Center.query_().all()
    }

    space_data = get_env_based_data('space')['space']

    if not clean_data:
        # Get cleaned data and sort by 'id' key
        space_data = sorted(
            clean_seed_data('spaces', space_data), key=lambda s: s['id'])

    for space in space_data:
        center_id = center_id_mapper[space.get('center')]
        parent_id = None
        # saves spaces with parent and map its database id to the initial id
        if space.get("parentId"):
            parent_id = parent_ids[space["parentId"]]
            save_space = save_space_data(space["name"], parent_id, center_id,
                                         space_types[space["type"]])
        # saves space without parent and map its database id to the initial id
        else:
            save_space = save_space_data(space["name"], None, center_id,
                                         space_types[space["type"]])
        parent_ids[space["id"]] = save_space.id
