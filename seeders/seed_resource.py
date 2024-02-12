"""Module to seed resources table"""

# Models
from api.models import Resource
from api.models.database import db

# Seed data
from .seed_data import get_env_based_data

# Utilities
from api.utilities.helpers.seeders import clean_seed_data


def seed_resources(clean_data=False):
    """Seeds sample resources

    Args:
        clean_data (bool): Determines if seed  data is to be cleaned
    """

    resources = get_env_based_data('resource')['resource']
    if not clean_data:
        resources = clean_seed_data('resource', resources, True)

    resource_list = [Resource(name=name) for name in resources]
    db.session.add_all(resource_list)
    db.session.commit()
