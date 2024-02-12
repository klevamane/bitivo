# Models
from api.models import HotDeskRequest

# Utilities
from api.utilities.helpers.seeders import clean_seed_data

# Seed data
from .seed_data import get_env_based_data

def seed_hot_desk_request(clean_data=False):
    """Seeds multiple hot desk request data into the
        hot_desk_requests table
    Args:
        clean_data (bool): Determines if seed data is to be cleaned.
    """
    hot_desk_request = get_env_based_data('hot_desk')
    hot_desk_request = hot_desk_request if clean_data else clean_seed_data('hot_desk_request', hot_desk_request)

    HotDeskRequest.bulk_create(hot_desk_request)
