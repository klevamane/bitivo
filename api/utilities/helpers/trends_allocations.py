""" helper functions for trend allocations"""
import calendar
from flask import request
from sqlalchemy import text

from api.models.database import db
from api.utilities.sql_queries import sql_queries
from .calendar import get_start_of_week, get_end_of_week, get_start_of_month, \
    get_end_of_month, get_start_of_year, get_end_of_year, get_start_of_quarter, get_end_of_quarter
from ...utilities.validators.hot_desk_report_query_validator \
    import validate_frequency_value


def get_descriptor(frequency, period):
    """
    Get description of the time passed based on the frequency and period
    Args:
        frequency (string): The interval of repetition
        period (integer): A positive integer gotten from the query result

    Returns:
        (string) abbrievated time unit depending on the value of the frquency argument
    """
    prefix_mapper = {
        'week': 'Week ',
        'quarter': 'Q',
    }
    prefix = prefix_mapper.get(frequency, '')
    if prefix:
        return f'{prefix}{int(period)}'
    if frequency == 'year':
        return int(period)
    elif frequency == 'month':
        return calendar.month_abbr[int(period)]
    # since calendar date starts at 0 and date_part starts at 1, we deduct 1 from date
    return calendar.day_abbr[int(period) - 1]


def get_trends_query(*args, **kwargs):
    """
    get the trends_query_data depending on the arguments passed
    Args:
        *args:
            frequency (str): The value of the query param frequency
            floor (dict): A dictionary containing the available floors
            start_date (str): The value of the start_date from the startDate query param
            end_date (str): The value of the end_date from the endDate query param
        *kwargs:
            query_key (str): string that determines which trend_allocation query to execute
            user_id (str): The token_id of the user

    Returns:
        (tuple): A tuple of the periods and the values
    """
    query_key, user_id = kwargs.get('query_key',
                                    'trends_allocation'), kwargs.get('user_id')
    frequency, floor, start_date, end_date = args
    frequency_mapper = {
        'week': 'weekly',
        'month': 'monthly',
        'year': 'yearly',
        'quarter': 'quarterly',
        'day': 'daily',
    }
    if query_key == 'trends_allocation':
        trends_allocation = sql_queries[query_key].format(
            frequency, frequency_mapper.get(frequency), floor, start_date,
            end_date)
    else:
        trends_allocation = sql_queries[query_key].format(
            frequency, frequency_mapper.get(frequency), user_id, floor,
            start_date, end_date)
    query = db.engine.execute(text(trends_allocation)).fetchall()
    periods, values = [], []
    for period in query:
        periods.append(get_descriptor(frequency, period[0]))
        values.append(period[1])
    return periods, values


def weekly_trends(*args, **kwargs):
    """
    get the weekly trends
    Args:
        *args:
            floor (dict): A dictionary containing the available floors
            start_date (str): The value of the start_date from the startDate query param
            end_date (str): The value of the end_date from the endDate query param
        **kwargs:
            query_key (str): string that determines which trend_allocation query to execute
            user_id (str): The token_id of the user

    Returns:
        get_trends_query(function): Returns the trends_query
    """
    floor, start_date, end_date = args
    query_key, user_id = kwargs.get('query_key',
                                    'trends_allocation'), kwargs.get(
                                        'user_id', '')
    start_date = get_start_of_week(start_date)
    end_date = get_end_of_week(end_date)
    return get_trends_query(
        'week',
        floor,
        start_date,
        end_date,
        query_key=query_key,
        user_id=user_id)


def monthly_trends(*args, **kwargs):
    """
    get the monthly trends
    Args:
        *args:
            floor (dict): A dictionary containing the available floors
            start_date (str): The value of the start_date from the startDate query param
            end_date (str): The value of the end_date from the endDate query param
        **kwargs:
            query_key (str): string that determines which trend_allocation query to execute
            user_id (str): The token_id of the user

    Returns:
        get_trends_query(function): Returns the trends_query
    """
    query_key, user_id = kwargs.get('query_key',
                                    'trends_allocation'), kwargs.get(
                                        'user_id', '')
    floor, start_date, end_date = args
    start_date = get_start_of_month(start_date)
    end_date = get_end_of_month(end_date)
    return get_trends_query(
        'month',
        floor,
        start_date,
        end_date,
        query_key=query_key,
        user_id=user_id)


def yearly_trends(*args, **kwargs):
    """
    get the yearly trends
    Args:
        *args:
            floor (dict): A dictionary containing the available floors
            start_date (str): The value of the start_date from the startDate query param
            end_date (str): The value of the end_date from the endDate query param
        **kwargs:
            query_key (str): string that determines which trend_allocation query to execute
            user_id (str): The token_id of the user

    Returns:
        get_trends_query(function): Returns the trends_query
    """
    query_key, user_id = kwargs.get('query_key',
                                    'trends_allocation'), kwargs.get(
                                        'user_id', '')
    floor, start_date, end_date = args
    start_date = get_start_of_year(start_date)
    end_date = get_end_of_year(end_date)
    return get_trends_query(
        'year',
        floor,
        start_date,
        end_date,
        query_key=query_key,
        user_id=user_id)


def quarterly_trends(*args, **kwargs):
    """
    get the quartely trends
    Args:
        *args:
            floor (dict): A dictionary containing the available floors
            start_date (str): The value of the start_date from the startDate query param
            end_date (str): The value of the end_date from the endDate query param
        **kwargs:
            query_key (str): string that determines which trend_allocation query to execute
            user_id (str): The token_id of the user

    Returns:
        get_trends_query(function): Returns the trends_query
    """
    query_key, user_id = kwargs.get('query_key',
                                    'trends_allocation'), kwargs.get(
                                        'user_id', '')
    floor, start_date, end_date = args
    start_date = get_start_of_quarter(start_date)
    end_date = get_end_of_quarter(end_date)
    return get_trends_query(
        'quarter',
        floor,
        start_date,
        end_date,
        query_key=query_key,
        user_id=user_id)


def daily_trends(*args, **kwargs):
    """
    get the daily trends
    Args:
        *args:
            floor (dict): A dictionary containing the available floors
            start_date (str): The value of the start_date from the startDate query param
            end_date (str): The value of the end_date from the endDate query param
        **kwargs:
            query_key (str): string that determines which trend_allocation query to execute
            user_id (str): The token_id of the user

    Returns:
        get_trends_query(function): Returns the trends_query
    """
    # the 'date_part() function expects 'dow' to return an integer
    # representing the day of week
    query_key, user_id = kwargs.get('query_key',
                                    'trends_allocation'), kwargs.get(
                                        'user_id', '')
    floor, start_date, end_date = args
    day_of_week = 'dow'
    return get_trends_query(
        day_of_week,
        floor,
        start_date,
        end_date,
        query_key=query_key,
        user_id=user_id)


def trends_allocations_helper(*args, **kwargs):
    """
    This method returns all trends_allocations
    Args:
        start_date(string): Value of start_date query param
        end_date(string): Value of end_date query param
    returns:
        data (dictionary): data of trend allocation
    """
    query_key, user_id = kwargs.get('query_key',
                                    'trends_allocation'), kwargs.get('user_id')
    start_date, end_date = args
    frequency = request.args.get('frequency', 'month').lower()
    validate_frequency_value(frequency)
    frequency_mapper = {
        'week': weekly_trends,
        'month': monthly_trends,
        'year': yearly_trends,
        'quarter': quarterly_trends,
        'day': daily_trends,
    }
    get_trends = frequency_mapper.get(frequency)
    floors = [{'no': '1', 'description': 'First floor'}]
    data = []
    for floor in floors:
        period, values = get_trends(floor['no'], start_date, end_date) \
            if query_key == 'trends_allocation' \
                else get_trends(
                    floor['no'],
                    start_date,
                    end_date,
                    user_id=user_id,
                    query_key=query_key
                )
        data.append(
            dict(floor=floor['description'], period=period, values=values))
    return dict(data=data)
