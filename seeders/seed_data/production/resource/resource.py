"""Production/staging environment resource seed data module"""

# Helpers
from api.utilities.helpers.seeders import json_to_dictionary


def resource_data():
    """Gets resource data from json file

    Returns:
        dict: Resource seed data
    """

    return json_to_dictionary(
        './seeders/seed_data/production/resource/resource.json')
