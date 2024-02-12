# Models
from api.models import WorkOrder

# Utilities
from api.utilities.helpers.seeders import clean_seed_data

# Seed data
from .seed_data import get_env_based_data

def seed_work_order(clean_data=False):
    """Seeds multiple work order into the database.
    This function checks seeding is of particulary on work order in the given environment,
    seeds new data if provided or none if the given data exists in the database.
    
    Args:
        clean_data (bool): Determines if seed data is to be cleaned.
    """
    work_order = get_env_based_data('work_order')
    work_order = clean_seed_data('work_order', work_order) if not clean_data else work_order

    WorkOrder.bulk_create(work_order)
