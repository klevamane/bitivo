"""Development/Testing environment seed data module"""

# Development data
from seeders.seed_data.development import get_production_development_data


def center_data():
    """Gets center data from json file.

    Returns:
        dict: Center data to be seeded.
    """

    return get_production_development_data('center')
