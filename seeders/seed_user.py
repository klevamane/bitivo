"""Module to seed users table"""

# Models
from api.models import User, Role, Center

# Utilities
from api.utilities.helpers.seeders import clean_seed_data

# Seed data
from .seed_data import get_env_based_data


def seed_user(clean_data=False):
    """Seeds user data to User table.

    Args:
        clean_data (bool): Determines if seed data is to be cleaned
    """

    user_data = get_env_based_data('user')

    if not clean_data:
        # Clean user_data by omitting already existing records
        user_data = clean_seed_data('user', user_data)

    User.bulk_create(user_data)
