from datetime import datetime


def greeting():
    """ Checks part of the day and returns a greeting message accordingly
    Returns:
        string: greeting message
    """

    hour = datetime.now().hour

    if hour < 12:
        greeting_msg = "Good morning"
    elif hour < 18:
        greeting_msg = "Good afternoon :sunny:"
    else:
        greeting_msg = "Good evening"

    return greeting_msg
