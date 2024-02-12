def get_last_month(year, month):
    """ Returns the correct previous month.

    Args:
        year (integer): the current year
        month(integer): the current month

    Returns:
        year & month (tuple): data holding the previous month and year
    """
    if month == 1:
        return year - 1, 12
    else:
        return year, month - 1
