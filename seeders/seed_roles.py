"""Module to seed role table"""

# Models
from api.models import Role

# Utilities
from api.utilities.helpers.seeders import seed_data_helper

# Seed data
from .seed_data import get_env_based_data


def seed_roles(clean_data=False):
    """Seeds sample roles

    Args:
        clean_data (bool): Determines if seed data is to be cleaned
    """

    seed_data_helper(
        get_env_based_data, 'role', Role, clean_data=clean_data)
