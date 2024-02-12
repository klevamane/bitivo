import random

def get_number(upper_limit):
    """ Generates a random integer from 0 to the limit provided.

    Args:
        upper_limit (Integer): Maximum number the result should fall in.
    Returns:
        interger : generated integer
    """

    return random.randint(0, upper_limit)

def generate_time():
    """ Creates a dict for time to be used in a request_type.
    Returns:
        dict: A dictionary with time options
    """
    return {
        "days" : get_number(31),
        "hours" : get_number(24),
        "minutes" : get_number(60)
    }
