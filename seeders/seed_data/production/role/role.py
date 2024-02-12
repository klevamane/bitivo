"""Production/staging environment role seed data module"""

# Helpers
from api.utilities.helpers.seeders import json_to_dictionary


def role_data():
    """Gets role data from json file

    Returns:
        dict: Role seed data.
    """

    return json_to_dictionary('./seeders/seed_data/production/role/role.json')
