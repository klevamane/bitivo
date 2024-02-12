from ..bugsnag import post_bugsnag_exception
from ..google_sheets.google_sheets_helper import GoogleSheetHelper
from ..ref_no_info import get_floor_and_seat_no


def update_spread_sheet_data(*args):
    """Method to update google sheet data
    Args:
        *args
            index(int): index of list
            record(dict): sheet record
            sheet(obj): sheet object
            hot_desk_ref_no(string): hot desk ref number
            updated_to(str): What we want to update to
    """

    index, record, sheet, hot_desk_ref_no, updated_to = args
    floor, seat_no = get_floor_and_seat_no(hot_desk_ref_no)

    if record.get('# of seats') == seat_no and record.get('Floor')[0] == str(floor):
        try:
            sheet.update_cell(index + 2, 5, updated_to)
        except Exception as error:
            post_bugsnag_exception(
                error, f'Could not update spreadsheet seat no - {seat_no}')


def update_(*args):
    """ Function to update hot desk
    Args:
        hot_desk_ref(string): hot desk ref number
        update_to(str): What we want to update to
    """
    sheet_data, sheet, bay_column, hot_desk_ref, update_to = args
    for index, record in enumerate(zip(sheet_data, bay_column[:])):
        update_spread_sheet_data(index, record[0], sheet, hot_desk_ref, update_to)
