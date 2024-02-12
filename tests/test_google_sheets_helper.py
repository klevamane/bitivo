"""Module to test the methods in the google sheet helper"""
import unittest
from unittest.mock import Mock, patch
from bot.utilities.google_sheets import google_sheets_helper

from tests.mocks.google_sheet import GoogleSheetHelper
from tests.mocks.hot_desk import REQUESTER_NAME, row


class TestGoogleSheetHelper(unittest.TestCase):
    """Test helper class for getting data from google sheet"""

    @patch('bot.utilities.google_sheets.google_sheets_helper.GoogleSheetHelper.open_sheet', Mock(return_value=GoogleSheetHelper().open_sheet()))
    def test_retrieve_all_hotdesk_eligible_users(self):
        """Test for retrieve_all_hotdesk_eligible_users"""

        hotdesk = GoogleSheetHelper().open_sheet()
        sheet_data = hotdesk[0]

        users = google_sheets_helper.GoogleSheetHelper().retrieve_all_hotdesk_eligible_users()

        self.assertNotEqual(users, sheet_data)

    @patch('bot.utilities.google_sheets.google_sheets_helper.GoogleSheetHelper.open_sheet', Mock(return_value=GoogleSheetHelper().open_sheet()))
    def test_get_requester_seat_location(self):
        """Test for get_requester_seat_location"""

        hotdesk = GoogleSheetHelper().open_sheet()
        sheet = hotdesk[1]
        sheet.find = Mock(return_value=row)
        a_mock = Mock(return_value=500)
        sheet.find(REQUESTER_NAME).row = a_mock()
        sheet.row_values = Mock(
            return_value=['530', '1N', '1st', '15', 'Firstname Lastname'])
        seat_location = google_sheets_helper.GoogleSheetHelper(
        ).get_requester_seat_location(REQUESTER_NAME)
        self.assertEqual(seat_location, '1N 15')
