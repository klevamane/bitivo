""" module for accessories transformation"""
from main import celery_app

from .transformer_interface import AssetTransformerInterface

# Utilities
from api.utilities.helpers.asset_transformer import (
    sheet_in_array,
    split_column,
    add_status_header,
    swap_column_value_in_usb_dongle_sheet,
    replace_unwanted_string)


class AccessoriesTransformer(AssetTransformerInterface):
    """Class for transforming accessories sheet"""

    @celery_app.task(name='transform_accessories_document')
    def transform(book, email):
        """Initiates transformation by calling transform_all

            Args:
                book (dict): a dictionary of 2 dimensional arrays as sheets
                email (str): email of the user that initiated the transformation
            Returns:
                new_book_content
        """
        cls = AccessoriesTransformer
        scripts_mapper = {
            'andela laptops': cls.transform_andela_laptops,
            'usb-c dongle': cls.transform_usb_dongle_assets,
            'test devices': cls.transform_test_devices,
        }
        new_book_content = cls.transform_all(book, scripts_mapper, email, 'Accessories')
        return new_book_content


    @classmethod
    def transform_andela_laptops(cls, sheet, new_book):
        """Transforms andela laptop sheet

        Args:
            sheet (object): pyexcel sheet object
            new_book (dict): multidimensional dictionary to add the sheet to

        Returns:
            new_book (dict): multidimensional dictionary
        """

        column_replacers = {
            'Asset Tag': 'Tag',
            'Adeniyi Kayode': 'Assignee'
        }

        sheet_headers = list(map(
            cls.clean_sheet_headers(column_replacers), sheet.row[0][1:13]))

        sheet_data = [sheet_headers]

        for row in sheet.row[1:]:
            sheet_data.append(row[1:13])
            new_book.update({'Andela Laptops': sheet_data})
        return new_book


    @classmethod
    def transform_test_devices(cls, sheet, new_book):
        """Transforms test devices sheet

        Args:
            sheet (object): pyexcel sheet object
            new_book (dict): multidimensional dictionary to add the sheet to

        Returns:
            new_book (dict): multidimensional dictionary
        """

        sheet_data = sheet_in_array(sheet)

        test_device_last_index = [sheet_data.index(
            item) for item in sheet_data if item[0] == 'PARTNER DEVICES']

        test_device_data = split_column(
            sheet_data[0:test_device_last_index[0]], 2)

        partner_device_data = split_column(
            sheet_data[test_device_last_index[0]+1:], 2)

        headers = test_device_data[0]+['Status']

        for header in headers:
            if header == 'Custodians':
                i = headers.index(header)
                headers[i] = 'Assignee'

        status_mapper = {
            'ops': 'Availabe',
            'reserve - ops': 'Inventory',
            'damaged': 'faulty-in store'
        }

        test_device = add_status_header(
            test_device_data, status_mapper, headers)

        partner_device = add_status_header(
            partner_device_data, status_mapper, headers)

        new_book.update({'Test Devices': test_device,
                         'Partner Devices': partner_device})
        return new_book


    @classmethod
    def transform_usb_dongle_assets(cls, sheet, new_book):
        """Transforms usb-c-dongle sheet

                Args:
                    sheet (object): pyexcel sheet object
                    new_book (dict): multidimensional dictionary to add the sheet to

                Returns:
                    new_book (dict): multidimensional dictionary
        """
        # set column headers
        sheet[0, 2] = 'Assignee'
        sheet[0, 4] = 'Prev User'
        sheet[0, 5] = 'Status'

        sheet.filter(column_indices=[0, 6, 7, 8])

        prev_user_values = list(sheet.column[3])
        status_list = list(sheet.column[4])

        # replace unwanted string in column
        prev_user_values = replace_unwanted_string(prev_user_values)

        #swap value in column
        swap_column_value_in_usb_dongle_sheet(prev_user_values, status_list)

        sheet.column[3] = prev_user_values
        sheet.column[4] = status_list
        new_book.update({'USB-C Dongle': sheet})
        return new_book
