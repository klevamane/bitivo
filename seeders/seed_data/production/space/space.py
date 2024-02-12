"""Production/staging environment space seed data module"""

# Helpers
from api.utilities.helpers.seeders import json_to_dictionary


def space_data():
    """Gets space data from json file

    Returns:
        dict: Space seed data
    """

    return json_to_dictionary(
        './seeders/seed_data/production/space/space.json')
