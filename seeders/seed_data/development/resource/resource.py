"""Development/Testing environment resource seed data module"""

# Development data
from seeders.seed_data.development import get_production_development_data


def resource_data():
    """Gets resource data from json file

    Returns:
        dict: Development resource seed data
    """

    return get_production_development_data('resource')
