"""Development/Testing environment space seed data module"""

# Development data
from seeders.seed_data.development import get_production_development_data


def space_data():
    """Gets space data from json file

    Returns:
        dict: Development seed space data.
    """

    return get_production_development_data('space')
