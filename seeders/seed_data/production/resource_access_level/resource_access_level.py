"""Module to seed resource access level table"""
# Resource access level mapper
from seeders.get_resource_data import get_resource_data



def resource_access_level_data():
    """Gets resource_access_level data to be seeded.

    Returns:
        (list): resource_access_level data to be seeded into the db.
    """
    return get_resource_data()
