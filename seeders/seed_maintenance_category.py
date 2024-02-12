# Models
from api.models import MaintenanceCategory

# Utilities
from api.utilities.helpers.seeders import seed_data_helper

# Seed data
from .seed_data import get_env_based_data


def seed_maintenance_category(clean_data=False):
    """Populate the maintenance category table with data

    Args:
        clean_data (bool, optional): Defaults to False. checks is seed data is clean
    """
    seed_data_helper(
        get_env_based_data,
        'maintenance_category',
        MaintenanceCategory,
        clean_data=clean_data)
