"""Production/staging environment space type seed data module"""

# Helpers
from api.utilities.helpers.seeders import json_to_dictionary


def space_type_data():
    """Gets center data from json file

    Returns:
        dict: Space type seed data.
    """

    return json_to_dictionary(
        './seeders/seed_data/production/space_type/space_type.json')
