"""Module to seed permission table"""

# Models
from api.models import Permission
from api.models.database import db

# Utilities
from api.utilities.helpers.seeders import clean_seed_data

# Seed data
from .seed_data.production.permission.permission import TYPES


def seed_permissions(clean_data=False):
    """Seeds sample permissions

     Args:
        clean_data (bool): Determines if seed data is to be cleaned.
    """

    types = clean_seed_data('permission', TYPES, True) if not clean_data else TYPES

    for i in types:
        db.session.add(Permission(type=i))
    db.session.commit()
