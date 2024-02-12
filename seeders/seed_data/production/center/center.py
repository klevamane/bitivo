"""Production/staging environment center seed data module"""

# Helpers
from api.utilities.helpers.seeders import json_to_dictionary


def center_data():
    """Gets center data from json file

    Returns:
        dict: Production center seed data.
    """

    return json_to_dictionary(
        './seeders/seed_data/production/center/center.json')
