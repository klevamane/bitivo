'''Helper for spaces endpoint'''
from ...models.space_type import SpaceType


def space_query(spaces, include):
    """
    Queries the SpaceType model and returns the data
    Args:
        spaces (list): list containing all available spaces
        include (str): query param that determines if deleted should be included in the query

    Returns:
        space_type_query (list): list of all space_types
    """
    space_type_query = SpaceType.query_(include_deleted=True).all() \
        if include and include == 'deleted' else spaces
    return space_type_query


def update_space_type(space_types, spaces):
    """
    Updates the space_category of the space_types
    Args:
        space_types (list): list of all space_types
        spaces (list): list containing dictonaries of spaces

    Returns:
        grouped_spaces (dict): spaces with updated space_category
    """
    grouped_spaces = {}
    for space_type in space_types:
        type_name = space_type['type']
        space_category = type_name.lower() + 's'
        space_list = [space for space in spaces if space['type'] == type_name]
        grouped_spaces.update({space_category: space_list})
    return grouped_spaces
