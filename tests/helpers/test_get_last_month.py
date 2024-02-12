# System Libraries
import datetime as dt

# Utilities
from api.utilities.helpers.get_last_month import get_last_month


class TestGetLastMonth:
    def test_for_month_before_january_succeed(self):
        """ Test to validate that the function returns
        the month December of the previous year if the current
        month is January.
        """
        current_month = 1  # The integer representing January
        current_year = dt.datetime.now().date().year

        year, month = get_last_month(current_year, current_month)

        assert month == 12  # The integer representing December
        assert year == current_year - 1  # The previous year

    def test_for_month_before_february_succeed(self):
        """ Test to validate that the function returns
        the month January of the current year if the current
        month is February.
        """
        current_month = 2  # The integer representing February
        current_year = dt.datetime.now().date().year

        year, month = get_last_month(current_year, current_month)

        assert month == 1  # The integer representing January
        assert year == current_year  # The current year
