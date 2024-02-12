import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# app config
from config import AppConfig
from ..constants import HOT_DESK
from ..bugsnag import post_bugsnag_exception
from .hot_desks_helper import add_hot_desk_to_list

GOOGLE_SHEET_NAME = AppConfig.GOOGLE_SHEET_NAME


class GoogleSheetHelper():
    """Helper class for getting data from google sheet"""

    def __init__(self):
        """Instance method to initialize Google Drive API
        Args:
            self
        Return
            None
        """

        # setup for google sheet - Google Drive API instance
        self.scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]

        google_credentials = json.loads(
            AppConfig.GOOGLE_CREDENTIALS, strict=False)
        self.credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            google_credentials, scopes=self.scope)
        self.client = gspread.authorize(self.credentials)

    def is_alive(self):
        """Check if the google spreadsheet api service is up
        Returns:
            (bool): True if the service works as expected else false
        """
        sheet = self.client.open(GOOGLE_SHEET_NAME)
        return True if sheet else False

    def open_sheet(self):
        """Instance method to open a wookbook and get the data
        in Space Allocation sheet

        Args:
            self(instance): Instance of GoogleSheetHelper
        Return
            None

        """
        # Find a workbook by name and open the a specific sheet
        try:
            sheet = self.client.open(GOOGLE_SHEET_NAME).worksheet(
                'Space Allocation')

            get_sheet_records = sheet.get_all_records()
            return get_sheet_records, sheet

        except gspread.exceptions.SpreadsheetNotFound as e:
            post_bugsnag_exception(e, 'Google sheet not found')
            return None, None

    def get_grouped_data(self, list_of_hot_desk):
        """Groups rooms which belong to the same floor
            Args:
        list_of_hot_desk (list): List of available hot_desks
        eg >>>>['5th Floor 1G61', '1st Floor 1G62', '5th Floor 1G63', '1st Floor 1G64']
            Returns:
        hot_desks (list): List of dictionaries
        eg >>>>[{'5th Floor': ['1G61', '1G63']}, {'1st Floor': ['1G62', '1G64']}]
        """
        floor_dict = {}
        hot_desk = []
        for string_hot_desk in list_of_hot_desk:
            split_data = string_hot_desk.split(",")
            floor = " ".join(split_data[0])
            room = split_data[-1]
            floor_dict.setdefault(floor, []).append(room)

        hot_desks = [{key: value} for key, value in floor_dict.items()]
        return hot_desks

    def retrieve_all_hot_desk(self):
        """ function to get all hot desk available on google sheet
        arg:
           workbook name
           work sheet position in the book
        returns:
               a list of hot desk
        """
        list_of_hot_desk = []
        sheet_data, sheet = self.open_sheet()
        if sheet:
            bay_column = sheet.col_values(2)[1:]

            room_bay = ''
            for index, (record, column) in enumerate(
                    zip(sheet_data, bay_column[:])):
                column = column.strip().upper()

                room_bay, hot_desk = self.get_next_hot_desk(
                    index, record, column, bay_column, room_bay)

                add_hot_desk_to_list(hot_desk, list_of_hot_desk)
            return self.get_grouped_data(list_of_hot_desk)

    def retrieve_all_hotdesk_eligible_users(self):
        """Get all hot desk eligible users from google sheet

        Args:
           sheet(instance): an instance of the SpreadSheet
           sheet_data(list): List of dictionaries containing        the contents of the spreadsheet.

        Returns:
               list: all hot desk eligible users
        """
        sheet_data, sheet = self.open_sheet()
        if sheet:
            bay_column = sheet.col_values(4)[651:]
            users = []
            for index, (record, column) in enumerate(
                    zip(sheet_data, bay_column[:])):
                column = column.strip()
                users.append(column)
            return users

    def get_requester_seat_location(self, requester_name):
        """Get the seat location of a requester

        Get the seat location of a requester allocated
        a permanent seat from google sheet

        Args:
            sheet(instance): an instance of the spreadsheet
            requester_name(str): name of the user making the
                request e.g (Firstname Lastname)

        Returns:
            string: the seat location of the requester
        """
        try:
            _, sheet = self.open_sheet()
            requester_serial_number = sheet.find(requester_name).row
            seat_detail = sheet.row_values(requester_serial_number)
            room_bay = ''
            while not room_bay:
                requester_serial_number -= 1
                if sheet.row_values(requester_serial_number)[1]:
                    room_bay = sheet.row_values(requester_serial_number)[1]
            seat_location = f'{room_bay} {seat_detail[3]}'

            return seat_location
        except Exception as e:
            post_bugsnag_exception(e, f'Name not found in spreadsheet')

    def get_next_hot_desk(self, *args):
        """ helper method which gets the next hot desk from spreadsheet.
            Args:
            index: current index of the for loop
            record: current record of the iteration
            column: current column of the iteration
            bay_column:
            roombay:
            Returns: (tuple) roombay and hot_desk
        """
        index, record, column, bay_column, roombay = args
        hot_desk = ''
        other_bays = ['BLACK OPS', 'GLOBAL POD', 'MAUNA KEA']

        if column and len(column) == 2 or column in other_bays:
            roombay = column
        bay_column[index] = roombay

        if record.get("Name").upper() == HOT_DESK:
            roombay = bay_column[index]
            hot_desk = f'{record.get("Floor")} Floor, {roombay} {str(record.get("# of seats"))}'

        return roombay, hot_desk
