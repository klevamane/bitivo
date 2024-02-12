"""Module to seed stock counts table"""

# Standard library
import datetime as dt
from calendar import monthrange
import random
import math

# Models
from api.models import StockCount, AssetCategory, Center, User

# App config
from config import AppConfig


def generate_dates(start, end, delta):
    """Generate a range of dates with a given delta

    Args:
        start (Datetime): The start date
        end (Datetime): The end date
        delta (Datetime): The delta between the dates

    Yields:
        Datetime: a datetime object
    """
    current = start
    while current < end:
        yield current
        current += delta


def get_week_number(date):
    """Generate a week number given the date

    Args:
        date (Datetime): The date to calculate the week from

    Returns:
        int: The week number of the given date. Can be between 1 and 5
    """
    return int(math.ceil(date.day / 7.0))


def seed_stock_count(clean_data=False):
    """Seeder for the stock count table

    Seeds the stock count table with stock count data for each week in a one
    year period ending with the current month. The data is generated for each
    asset category present in the database

    Args:
        clean_data (bool): Determines if seed data is to be cleaned.

    Returns:
        None
    """

    if AppConfig.FLASK_ENV in ('production', 'staging') and not clean_data:
        return []

    now = dt.datetime.utcnow()
    categories = AssetCategory.query_().all()
    center = Center.query_().first()
    users = User.query_().all()
    start_date = dt.datetime(now.year - 1, 1, 1)
    last_day = monthrange(now.year, now.month)[1]
    end_date = dt.datetime(now.year, now.month, last_day)
    delta = dt.timedelta(days=7)

    for date in generate_dates(start_date, end_date, delta):
        week_num = get_week_number(date)
        sc = [{
            'asset_category_id': category.id,
            'center_id': center.id,
            'token_id': random.choice(users).token_id,
            'created_at': date,
            'week': week_num,
            'count': random.randint(10, 200)
        } for category in categories if week_num >= 2 and week_num != 5]
        StockCount.bulk_create(sc)
