"""Module with center database seed data."""

# Database instance
from api.models.database import db

# Models
from api.models import Center

# Utilities
from api.utilities.helpers.seeders import clean_seed_data

# Seed data
from .seed_data import get_env_based_data


def seed_center(clean_data=False):
    """Function that seeds data into the center table.

     Args:
        clean_data (bool): Determines if seed data is to be cleaned

    Returns:
        None
    """

    args = get_env_based_data('center')['center']

    if not clean_data:
        args = clean_seed_data('center', args)

    for arg in args:
        center = Center(name=arg['name'], image=arg['image'])
        db.session.add(center)
    db.session.commit()
