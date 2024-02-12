def check_creator(created_by, requester):
    """Checks if the person making the request is the creator
    of the resource

    Args:
        requester (str): the id of the person making the request
        created_by (str): the instance creator to verify with

    Returns:
        Boolean: True or False depending on if the person making the
        request is the creator of the resource
    """
    if created_by == requester:
        return True
    return False
