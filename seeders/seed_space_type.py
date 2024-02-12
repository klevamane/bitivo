"""Module to seed space type table"""

# Models
from api.models import SpaceType

# Helpers
from api.utilities.helpers.seeders import seed_data_helper

# Seed data
from .seed_data import get_env_based_data


def seed_space_type(clean_data=False):
    """Seeds sample space type

    Args:
        clean_data (bool): Determines if seed data is to be cleaned
    """

    seed_data_helper(
        get_env_based_data, 'space_type', SpaceType, clean_data=clean_data)
