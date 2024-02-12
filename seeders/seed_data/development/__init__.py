"""Main development data module"""

# Helpers
from api.utilities.helpers.seeders import json_to_dictionary


def get_production_development_data(resource):
    """Gets both production and development data from json files.

    Args:
        resource (str): data type/model to be seeded

    Returns:
        dict: Seed data to be seeded.
    """

    production_data = json_to_dictionary(
        f'./seeders/seed_data/production/{resource}/{resource}.json')
    development_data = json_to_dictionary(
        f'./seeders/seed_data/development/{resource}/{resource}.json')

    production_data[resource].extend(development_data[resource])
    return production_data
