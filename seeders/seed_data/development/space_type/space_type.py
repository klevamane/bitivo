"""Development/Testing environment space type seed data module"""

# Development data
from seeders.seed_data.development import get_production_development_data


def space_type_data():
    """Gets space_type data from json file

    Returns:
        dict: Development space_type seed data
    """

    return get_production_development_data('space_type')
