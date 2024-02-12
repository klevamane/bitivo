from datetime import datetime as dt, timedelta
from calendar import monthrange
import math


def convert_string_to_date(date, date_format='%Y-%m-%d'):
    """ converts string formatted date to datetime format or returns the date
    if in datetime format

    Args:
        date (datetime / string): date of today
        date_format (string): true or false value with default set to false

    Returns:
        date in datetime format
    """
    if isinstance(date, str):
        return dt.strptime(date, date_format)
    return date


def get_start_or_end_of_day(date, end=False):
    """ gets the start or end date-time of a day

    Args:
        date (datetime): date of today
        end (bool): true or false value with default set to false

    Returns:
        end or start date-time of the day
    """
    date = convert_string_to_date(date)
    time = [00, 00, 00] if not end else [23, 59, 59]
    return dt(date.year, date.month, date.day, time[0], time[1], time[2])


def get_start_of_week(date):
    date = convert_string_to_date(date)
    return date - timedelta(days=date.weekday())


def get_end_of_week(date):
    start_of_week = get_start_of_week(date)
    return start_of_week + timedelta(days=6)


def get_start_of_month(date):
    date = convert_string_to_date(date)
    return dt(date.year, date.month, 1)


def get_end_of_month(date):
    date = convert_string_to_date(date)
    last_day_of_month = monthrange(date.year, date.month)[-1]
    return dt(date.year, date.month, last_day_of_month)


def get_start_of_quarter(date):
    date = convert_string_to_date(date)
    current_quarter = math.floor((date.month - 1) / 3 + 1)
    return dt(date.year, 3 * current_quarter - 2, 1)


def get_end_of_quarter(date):
    date = convert_string_to_date(date)
    current_quarter = math.floor((date.month - 1) / 3 + 1)
    return dt(date.year, 3 * current_quarter, 1) + timedelta(days=-1)


def get_end_of_year(date):
    year = convert_string_to_date(date).year
    return dt(year, 12, 31)


def get_start_of_year(date):
    year = convert_string_to_date(date).year
    return dt(year, 1, 1)
