"""Development/Testing environment asset category seed data module"""

# Development data
from seeders.seed_data.development import get_production_development_data


def asset_category_data():
    """Gets asset category data from json file

    Returns:
        dict: development asset category seed data.
    """

    return get_production_development_data('asset_category')
