"""Production/staging environment asset category seed data module"""

# Helpers
from api.utilities.helpers.seeders import json_to_dictionary


def asset_category_data():
    """Gets asset category data from json file

    Returns:
        dict: Production asset category seed data
    """

    return json_to_dictionary(
        './seeders/seed_data/production/asset_category/asset_category.json')
