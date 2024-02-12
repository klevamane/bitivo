def title_case(value, data):
    """Return Capitalized value in data.

    Args:
        value (str): key to check for in data supplied
        data (dict): data supplied to the schema

    """
    if value in data:
        data[value] = data[value].title()
