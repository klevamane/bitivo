# Standard imports
from functools import wraps
from datetime import datetime, timedelta, date

# Library Imports
from flask import request

# Local Imports
from .validators.date_validator import date_validator
from .error import raises
from .constants import START_DATE

def verify_date_range(start, end):
    """Verify that date values are valid and in range

        Args:
            start (date): the start date
            end (date): the end date

        Returns:
            tuple of start_date and end_date

        """
    # set default date values
    today = datetime.strptime(date.today().strftime('%Y-%m-%d'), '%Y-%m-%d')

    start_date = date_validator(start) if start else today

    end_date = date_validator(end) if end else today

    check_date_order(start, end, start_date, end_date, today)

    # ensure end_date captures the last second of the day
    end_date = end_date + timedelta(seconds=60 * 60 * 24 - 1)

    return start_date, end_date

def check_date_order(*args):
    """Verify that date values are valid and in range

        Args:
            start (str): the provided start date
            end (str): the provided end date
            start_date (datetime): the validated start date
            end_date (datetime): the validated end date
            today (datetime): the current date

    """

    start, end, start_date, end_date, today = args

    # raise error if start date is not provided and end date not today
    only_end_date = end and not start
    if only_end_date and datetime.strptime(end, '%Y-%m-%d') != today:
        raises('invalid_end_date', 400)

    # raise error if end date is not provided and start date
    # is greater than today
    only_start_date = start and not end
    if only_start_date and start_date > end_date:
        raises('invalid_start_date', 400)

    # raise error if start date and end date are provided and
    # start date is greater than end date
    if start_date > end_date:
        raises('invalid_date_range', 400)

def default_date_range(start, end, url):
    """Returns default start and end dates if both are not provided

    Sets default date range to allow exporting endpoints to return all items
    or sets default date range to a week interval for other endpoints

        Args:
            start (str): the start date
            end (str): the end date

        Returns:
            tuple of start_date and end_date string

        """

    start_date, end_date = start, end

    if start or end:
        return start_date, end_date

    end_date = datetime.strftime(datetime.now(), '%Y-%m-%d')

    if 'export' in url:
        start_date = START_DATE
    else:
        a_week_ago = datetime.strptime(end_date,
                                       '%Y-%m-%d') - timedelta(days=7)
        start_date = datetime.strftime(a_week_ago, '%Y-%m-%d')
    return start_date, end_date


def report_query_date_validator(func):
    """Validates report query date range

    Set start/end date if not provided
    Raises error if date not in the format '%Y-%m-%d'

    Args:
        func(function): Decorated function

    Returns:
        function

    Raises:
        Throws error if date not in the format '%YYYY-%mm-%dd'
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        query = request.args.to_dict()

        # normalize the query keys
        norm_query = {
            key.lower().strip(): value
            for key, value in query.items()
        }

        start_date = norm_query.get('startdate', '')
        end_date = norm_query.get('enddate', '')

        # set default date range if not provided
        start_date, end_date = default_date_range(start_date, end_date,
                                                  request.path)
        # verify that date range is valid
        start_date, end_date = verify_date_range(start_date, end_date)

        return func(*args, start_date, end_date, **kwargs)

    return decorated_function
