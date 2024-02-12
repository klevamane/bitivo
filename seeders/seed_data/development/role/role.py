"""Development/Testing environment role type seed data module"""

# Development data
from seeders.seed_data.development import get_production_development_data


def role_data():
    """Gets role data from json file.

    Returns:
        dict: Development role seed data.
    """

    return get_production_development_data('role')
