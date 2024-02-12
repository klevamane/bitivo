"""Test model calendar module"""
import math
from datetime import datetime as dt, timedelta
from calendar import monthrange

# Local Modules
from api.utilities.helpers.calendar import (
    get_start_or_end_of_day, get_start_of_week, get_end_of_week,
    get_start_of_month, get_end_of_month, get_start_of_quarter,
    get_end_of_quarter, get_start_of_year, get_end_of_year,
    convert_string_to_date)

date = dt.today()
str_date = '2018-4-24'
date_format = '%Y-%m-%d'
start_of_week = get_start_of_week(date)
current_quarter = math.floor((date.month - 1) / 3 + 1)
year = convert_string_to_date(date).year


class TestCalendar:
    """Tests for the calender helper"""

    def test_convert_string_to_date_succeeds(self):
        """ tests that the method returns date in datetime format"""
        converted_date = convert_string_to_date(str_date)
        assert converted_date == dt.strptime(str_date, date_format)

    def test_get_start_of_the_day(self):
        """ tests that the method returns start of the day's date"""

        start_date_time = get_start_or_end_of_day(date, end=False)
        assert start_date_time == dt(date.year, date.month, date.day, 0, 0, 0)

    def test_get_end_of_the_day(self):
        """ tests that the method returns end of the day's date"""

        end_date_time = get_start_or_end_of_day(date, end=True)
        assert end_date_time == dt(date.year, date.month, date.day, 23, 59, 59)

    def test_get_start_of_week_succeeds(self):
        """ tests that the method returns start of the week's date"""
        assert start_of_week == date - timedelta(days=date.weekday())

    def test_get_end_of_week_succeeds(self):
        """ tests that the method returns end of the week's date"""
        end_of_week = get_end_of_week(date)
        assert end_of_week == start_of_week + timedelta(days=6)

    def test_get_start_of_month_succeeds(self):
        """ tests that the method returns start of the month's date"""
        start_of_month = get_start_of_month(date)
        assert start_of_month == dt(date.year, date.month, 1)

    def test_get_end_of_month_succeeds(self):
        """ tests that the method returns end of the month's date"""
        end_of_month = get_end_of_month(date)
        last_day_of_month = monthrange(date.year, date.month)[-1]
        assert end_of_month == dt(date.year, date.month, last_day_of_month)

    def test_get_start_of_quarter_succeeds(self):
        """ tests that the method returns start of the quarter's date"""
        start_of_quarter = get_start_of_quarter(date)
        assert start_of_quarter == dt(date.year, 3 * current_quarter - 2, 1)

    def test_get_end_of_quarter_succeeds(self):
        """ tests that the method returns end of the quarter's date"""
        end_of_quarter = get_end_of_quarter(date)
        assert end_of_quarter == dt(date.year, 3 * current_quarter,
                                    1) + timedelta(days=-1)

    def test_get_start_of_year_succeeds(self):
        """ tests that the method returns start of the year's date"""
        start_of_year = get_start_of_year(date)
        assert start_of_year == dt(year, 1, 1)

    def test_get_end_of_year_succeeds(self):
        """ tests that the method returns end of the year's date"""
        end_of_year = get_end_of_year(date)
        assert end_of_year == dt(year, 12, 31)
