"""Module that tests the functionalities of verify_date_range and date_validator"""

# Standard Library
from datetime import date, datetime, timedelta

# Third Party Library
from pytest import raises
from flask import request

# Local Modules
from api.utilities.messages.error_messages import serialization_errors
from api.middlewares.base_validator import ValidationError
from api.utilities.verify_date_range import verify_date_range, default_date_range
from api.utilities.validators.date_validator import date_validator
from api.utilities.constants import START_DATE

# App config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1
analytics_url = BASE_URL + '/assets/analytics/'
export_url = BASE_URL + '/assets/analytics/export?report=assetinflow'

start_date = '2018-01-11'
end_date = '2019-09-29'


class TestVerifyDateRangeAndDateValidator:
    """
    Tests the functionality of verify_date_range / date validator
    """

    def test_verify_date_range_succeeds(self):
        """
        Should return equivalent python datetime range
        if provided with valid string date range

        The end date should capture all the 
        hours and seconds of the day
        """

        new_start_date, new_end_date = verify_date_range(start_date, end_date)

        assert new_start_date == datetime.strptime(start_date, '%Y-%m-%d')
        assert new_end_date == datetime \
            .strptime(end_date, '%Y-%m-%d') + timedelta(seconds=60*60*24-1)

    def test_verify_date_range_no_end_date_succeeds(self):
        """
        Should return todays datetime as end date 
        if not provided

        """

        new_start_date, new_end_date = verify_date_range(start_date, None)

        assert new_start_date == datetime.strptime(start_date, '%Y-%m-%d')
        assert new_end_date.date() == datetime.now().date()

    def test_verify_date_range_no_start_date_succeeds(self):
        """
        Should return todays datetime as start date 
        if not provided

        """

        today = datetime.strftime(date.today(), '%Y-%m-%d')

        new_start_date, new_end_date = verify_date_range(None, today)

        assert new_start_date.date() == datetime.now().date()
        assert new_end_date == datetime \
            .strptime(today, '%Y-%m-%d') + timedelta(seconds=60*60*24-1)

    def test_verify_date_range_no_start_and_end_date_succeeds(self):
        """
        Should return the start and end  of the current date
        if both start and end date are not provided
        """

        new_start_date, new_end_date = verify_date_range(None, None)

        assert new_start_date.date() == datetime.now().date()
        assert new_end_date.date() == datetime.now().date() \
                                     + timedelta(seconds=60*60*24-1)

    def test_verify_date_range_invalid_start_date_format_fails(self):
        """
        Should throw an error with error message and status code
        400 if start date is not a valid date format
        """

        with raises(ValidationError) as error:
            verify_date_range('208-11-3', end_date)

        assert error.value.status_code == 400
        assert error.value.error['status'] == 'error'
        assert error.value.error['message'] == serialization_errors[
            'invalid_date'].format('208-11-3')

    def test_verify_date_range_if_end_date_not_equal_today_fails(self):
        """Test verify date range

        Should throw an error with error message and status code
        400 if start date is not provided and end date is not today
        """

        not_today = datetime.now() + timedelta(days=2)
        after_today = datetime.strftime(not_today, '%Y-%m-%d')

        with raises(ValidationError) as error:
            verify_date_range(None, after_today)

        assert error.value.status_code == 400
        assert error.value.error['status'] == 'error'
        assert error.value.error['message'] == serialization_errors[
            'invalid_end_date']

    def test_verify_date_range_if_start_date_greater_than_today_fails(self):
        """Test verify date range

        Should throw an error with error message and status code
        400 if end date is not provided and start date is greater 
        than today
        """

        tomorrow = datetime.now() + timedelta(1)
        tomorrow = datetime.strftime(tomorrow, '%Y-%m-%d')

        with raises(ValidationError) as error:
            verify_date_range(tomorrow, None)

        assert error.value.status_code == 400
        assert error.value.error['status'] == 'error'
        assert error.value.error['message'] == serialization_errors[
            'invalid_start_date']

    def test_verify_date_range_invalid_end_date_format_fails(self):
        """
        Should throw an error with error message and status code
        400 if end date is not a valid date format
        """

        with raises(ValidationError) as error:
            verify_date_range(start_date, '2018-01')

        assert error.value.status_code == 400
        assert error.value.error['status'] == 'error'
        assert error.value.error['message'] == serialization_errors[
            'invalid_date'].format('2018-01')

    def test_verify_date_range_start_date_greater_than_end_date_fails(self):
        """
        Should throw an error with error message and status code
        400 if start date is greater than end date
        """

        with raises(ValidationError) as error:
            verify_date_range('2019-10-10', '2018-01-10')

        assert error.value.status_code == 400
        assert error.value.error['status'] == 'error'
        assert error.value.error['message'] == serialization_errors[
            'invalid_date_range']

    def test_date_validator_succeeds(self):
        """
        Should return a valid datetime if
        passed valid date string
        """

        valid_date = date_validator('2019-10-10')

        assert valid_date == datetime.strptime('2019-10-10', '%Y-%m-%d')

    def test_date_validator_fails(self):
        """
        Should throw an error with error message and status code
        400 if end date is not a valid date format
        """

        with raises(ValidationError) as error:
            date_validator('209-10')

        assert error.value.status_code == 400
        assert error.value.error['status'] == 'error'
        assert error.value.error['message'] == serialization_errors[
            'invalid_date'].format('209-10')

    def test_default_date_range_succeeds(self):
        """
        Should not set default date range if
        either start or end date is provided
        """

        start_date_res, end_date_res = default_date_range(
            start_date, end_date, analytics_url)

        assert start_date_res == start_date
        assert end_date_res == end_date

    def test_default_date_range_with_no_date_succeeds(self):
        """
        Should return start and end date range with
        a week interval if no date is specified
        and endpoint is not an export endpoint
        """
        start_date_res, end_date_res = default_date_range(
            None, None, analytics_url)

        end_date_value = datetime.strftime(datetime.now(), '%Y-%m-%d')
        a_week_ago = datetime.strptime(end_date_value,
                                       '%Y-%m-%d') - timedelta(days=7)
        start_date_value = datetime.strftime(a_week_ago, '%Y-%m-%d')

        assert start_date_res == start_date_value
        assert end_date_res == end_date_value

    def test_default_date_range_with_no_date_in_export_succeeds(self):
        """
        Should return start and end date range that
        captures all data from the database if it is 
        an export endpoint
        """
        start_date_res, end_date_res = default_date_range(
            None, None, export_url)

        end_date_value = datetime.strftime(datetime.now(), '%Y-%m-%d')
        start_date_value = START_DATE

        assert start_date_res == start_date_value
        assert end_date_res == end_date_value
