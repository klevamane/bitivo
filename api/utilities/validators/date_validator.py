from datetime import datetime, date
import dateutil.parser
from ..error import raises


def date_validator(date_value):
    """Validates date format

     Arguments:
        date_value (string): date string

     Raises:
        ValidationError: Used to raise exception if date format is not valid

    Returns:
        date: the validated date
    """

    try:
        dateutil.parser.parse(date_value).date()
        try:
            date = datetime.strptime(date_value, '%Y-%m-%d')
        except ValueError:
            raises('invalid_date', 400, date_value)
    except ValueError as error:
        # raise error if the date values are out of range
        raises('invalid_provided_date', 400, str(error))
    return date


def validate_asset_log_return_date(date_value):
    """Validates asset log return date
     Args:
        date_value (string): date string
     Raises:
        ValidationError: Used to raise exception if expected return date is invalid
    """
    if date_value:
        valid_date = date_validator(date_value)
        today = datetime.strptime(
            date.today().strftime('%Y-%m-%d'), '%Y-%m-%d')
        if valid_date and valid_date < today:
            raises('invalid_return_date', 400)


def validate_date_range(start_date, end_date):
    """Validates date range of two dates
     Args:
        start_date (string): the supplied start date
        end_date (string): the supplied end date
     Raises:
        ValidationError: raise exception if date or range is invalid
    """
    if start_date is not None and end_date is not None:
        start_date = date_validator(start_date)
        end_date = date_validator(end_date)
        if start_date > end_date:
            raises('invalid_date_range', 400)
