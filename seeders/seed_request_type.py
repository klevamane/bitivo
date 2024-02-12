# Models
from api.models import RequestType

# Helpers
from api.utilities.helpers.generate_time import generate_time

# Utilities
from api.utilities.helpers.seeders import clean_seed_data

# Seed data
from .seed_data import get_env_based_data

def seed_request_type(clean_data=False):
    """ Seeds multiple request types into the database.
    This function checks seeding is of particulary on request types in the given environment,
    seeds new data if provided or none if the given data exists in the database.
    Args:
        clean_data (bool): Determines if seed data is to be cleaned.
    """
    users, request_types = get_env_based_data('request_type')

    if not clean_data:
        request_types = clean_seed_data('request_type', request_types, True)

    if request_types:
        request_types = [create_request_type_data(x[0], x[1], users[index])
                         for index, x in enumerate(request_types)]

    RequestType.bulk_create(request_types)


def create_request_type_data(title, center_id, assignee_id):
    """ Creates a dict for a request type.
        Args:
            title (String): Title for the request type.
            center_id (String): Center id to which that request type belongs to.
            assignee_id (String): User token_id who is responsible for the request type.
        Returns:
            dict: A dictionary of a request type
    """
    return {
        "title" : title,
        "center_id" : center_id,
        "assignee_id" : assignee_id,
        "response_time" : generate_time(),
        "resolution_time" : generate_time(),
        "closure_time" : generate_time()
    }
