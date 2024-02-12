"""Module to test the hot desk spreadsheet reset"""
from unittest.mock import Mock, patch

# Services
from datetime import timedelta, datetime

from api.services.schedule_notification import reset_hot_desk_spreadsheet
from bot.utilities.helpers.spreadsheet_helper import update_
from ...mocks.hot_desk import HOTDESK_GOOGLE

# GoogleSheetHelper
from ...mocks.google_sheet import GoogleSheetHelper


class TestHotDeskReset:
    """Test schedule due date email notifications."""

    def test_reset_hot_desk_spreadsheet(self, init_db, new_today_hot_desk):

        """
        Test for reset_hot_desk_spreadsheet succeeds
        Args:
            self (instance): instance of this class
            init_db (fixture): fixture to initialize the test database
            new_today_hot_desk (fixture): fixture that creates a new hot desk request
        """
        yesterday = datetime.today() - timedelta(days=1)
        new_today_hot_desk.created_at = yesterday
        new_today_hot_desk.save()
        reset_res = reset_hot_desk_spreadsheet()

        assert reset_res is None

    @patch(
        "bot.utilities.helpers.spreadsheet_helper.GoogleSheetHelper",
        **{'return_value.raiseError.side_effect': Exception()},
    )
    def test_reset_hot_desk_spreadsheet_fails(self, init_db, new_today_hot_desk):
        """
        Test for reset_hot_desk_spreadsheet fails
        Args:
            self (instance): instance of this class
            init_db (fixture): fixture to initialize the test database
            new_today_hot_desk (fixture): fixture that creates a new hot desk request
        """
        yesterday = datetime.today() - timedelta(days=1)
        new_today_hot_desk.created_at = yesterday
        new_today_hot_desk.save()

        _sheet_data, _sheet = GoogleSheetHelper().open_sheet()

        reset_res = reset_hot_desk_spreadsheet()

        assert reset_res is None
        assert _sheet == {}
        assert isinstance(_sheet_data, list)
        assert _sheet_data in HOTDESK_GOOGLE
