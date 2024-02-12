from api.utilities.helpers.asset_rows import generate_rows_from_tag, row_to_remove, rename_row_values
from main import celery_app

# utilities
from api.utilities.helpers.asset_transformer import (
    remove_empty_row, sheet_headers, remove_column, validate_lower_limit,
    has_data, change_cell_value, sheet_in_array, group_assets)
from api.utilities.constants import COLUMN_REPLACER, INDEX_DATA, AREA_DATA, CELL_DATA, CELL_REPLACER, HEADERS
from .transformer_interface import AssetTransformerInterface


class AssetRegisterTransformer(AssetTransformerInterface):
    @celery_app.task(name='transform_asset_document')
    def transform(book, email):
        """Initiates transformation by calling transform_all

            Args:
                book (dict): a dictionary of 2 dimensional arrays as sheets
                email (str): email of the user that initiated the transformation
            Returns:
                new_book_content
        """
        cls = AssetRegisterTransformer
        new_book_content = cls.transform_all(book, email)
        cls.send_email(new_book_content, 'Asset Register', email)
        return new_book_content

    @classmethod
    def transform_all(cls, book, email):
        """Transforms all the sheets in the document

            Args:
                book (dict): a dictionary of 2 dimensional arrays as sheets
                email (str): email of the user that initiated the transformation
            Returns:
                new_book_content (dict): a dict containing the transformed data
        """
        scripts_mapper = {
            'insured assets': cls.transform_insured_assets,
            'et airconditioners': cls.transform_et_airconditioners,
            'amity 2.0': cls.transform_amity_2_0,
            'it devices': cls.transform_it_devices,
            'et others': cls.transform_et_others,
            'et chairs': cls.transform_chairs_and_workstation_assets,
            'et workstations': cls.transform_chairs_and_workstation_assets,
            'jm 1': cls.transform_jm_1,
        }

        new_book_content = {}
        cls.run_scripts(scripts_mapper, book,
                        new_book_content)  # updates new_book_content

        return new_book_content

    @classmethod
    def transform_insured_assets(cls, sheet, new_book):
        """Transform insured assets sheet.Creates three sheets of this sheet
        namely office equipment, generator, and furniture

            Args:
                sheet (class): instance of pyexcel sheet
                new_book (dict): an empty dict that will be populated with
                2 dimensional arrays of the transformed document

            Returns:
                new_book (dict): a dict containing the transformed data
        """

        column_replacers = {'Code ID Ref.': 'Tag', 'Location': 'Assignee'}

        headers = sheet.row[0][1:-3] + ['Status']
        sheet_headers = list(
            map(cls.clean_sheet_headers(column_replacers), headers)
        )  # Adds status column to the new sheets that will be created off insured assets

        sheets_data = {
            'OFFICE EQUIPMENT': [sheet_headers],
            'FUNITURE': [sheet_headers],
            'GENERATOR': [sheet_headers]
        }

        for row in sheet:
            current_sheet = row[0]
            if current_sheet in sheets_data.keys():
                mult_dim_array = sheets_data.get(current_sheet)
                sheets_data[current_sheet] = cls.process_tags(
                    mult_dim_array, row, 2)
        new_book.update(sheets_data)
        return new_book

    @classmethod
    def process_tags(cls, mult_dim_array, row, tag_index):
        """Generates rows from tag if tags are grouped

            Args:
                mult_dim_array (dict): a dict of two dimensional array
                row (list): current row in the sheet
                tag_index (int): index of the tag value

            Returns:
                new_book (dict): a dict containing the transformed data
        """
        if '-' in row[tag_index]:
            rows = generate_rows_from_tag(row, tag_index)
            mult_dim_array = mult_dim_array + cls.format_insured_assets_rows(
                rows)
        else:
            mult_dim_array.append(cls.format_insured_assets_rows(row))

        return mult_dim_array

    @classmethod
    def format_insured_assets_rows(cls, rows):
        """Appends 'ok' to the end of each row

            Args:
                rows (list): a list of rows

            Returns:
                rows (list): updated rows with "ok" value
        """

        rows = list(map(lambda row: row[1:-3] + ['ok'], rows)) if isinstance(
            rows[0], list) else rows[1:-3] + ['ok']
        return rows

    @classmethod
    def transform_chairs_and_workstation_assets(cls, sheet, new_book,
                                                **kwargs):
        """Method to transform ET Chairs and any other data similar to ET Chairs
        Args:
            sheet (multidimentional list): excel sheet
            new_book (dict): the key is the sheet name while the value is an multidimentional list
            kwargs: a key word argument where the key can be any character but the value must be a new column to be added to sheet header

        Returns:
            dict: the key is the sheet name while the value is an multidimentional list
        """

        index = INDEX_DATA.get(sheet.name.lower())
        tag_index = index['tag']

        area_data = AREA_DATA
        cell_data = CELL_DATA
        header = sheet_headers(sheet.row[0], COLUMN_REPLACER,
                               index['remove_cell'], **kwargs)
        area_name = ''
        sheet_data = [header]
        for row in sheet.row[1:]:
            row, area_name, area, row_check = cls.formart_chairs_or_workstation_row(
                row, area_data, area_name, cell_data, index)
            row = row_to_remove(row, area_data, area)
            row_check = row and row_check
            if row_check and '-' in str(row[index['tag']]):
                rows = generate_rows_from_tag(row, tag_index)
                sheet_data = sheet_data + rows
            elif row_check and '-' not in str(row[tag_index]):
                uniform_tag = '/'.join(row[tag_index].split('/')[:-1])
                tag_limit = row[tag_index].split('/')[-1]
                row[tag_index] = validate_lower_limit(uniform_tag,
                                                      tag_limit)[2]
                sheet_data.append(row)
        new_book.update({sheet.name: sheet_data})
        return new_book

    @classmethod
    def formart_chairs_or_workstation_row(cls, *args):
        """Method to format ET CHAIRS excel data and any other similar to ET CHAIRS
        Args:
            args:
                row (list): current excell row
                area_data (list): list of asset area name
                area_name (str): current area name
                cell_data (list): list of cell data to replace
                index (dict): dictionary of all the sheet index to carry out operation like removing row or replacing row
        Returns:
            turple: turple containing row, current area name, area and row_check
        """

        row, area_data, area_name, cell_data, index = args
        area = row[index['area_name']]
        assignee_name = row[index['assignee']]

        area_name = area if area in area_data else area_name
        row_check = remove_empty_row(row)
        if str(assignee_name).startswith('BAY') or str(assignee_name).startswith('1') or\
           str(assignee_name).startswith('3') or assignee_name in cell_data:
            row[index['assignee']] = area_name

        row = sheet_headers(row, CELL_REPLACER, [])
        row = remove_column(row, index['remove_cell'])
        return row, area_name, area, row_check

    @classmethod
    def transform_et_airconditioners(cls, sheet, new_book):
        """Transforms air-conditioners google sheet

        Steps:
        - Loops through all the rows in the sheet
        - Checks if the row has data
        - Then return a clean row represented by a list
        - The clean row is appended to the sheet_data
        - The new_book is updated with the sheet_data
        Args:
            sheet (object): pyexcel sheet object
            new_book (dict): multidimensional dictionary to add the sheet to

        Returns:
            new_book (dict): multidimensional dictionary
        """
        sheet_data = []
        general_assignee = str()
        sheet_data.append(HEADERS)
        sheet.delete_columns([0, 11])
        sheet.delete_rows([0])
        values = {'Good': 'ok', 'N/A': ''}

        for row in sheet:
            rename_row_values(row, **values)  # clean rows with AC asset
            tag_column = 0
            if has_data(row):  # check if the row has data
                cls.process_sheet_rows(row, tag_column, sheet_data)
            else:
                general_assignee = row[
                    0]  # set the assignee value to the general location
                assignee_update = {
                    'OPEN WORKSPACE': general_assignee,
                    'P/C': general_assignee,
                    'BAY': general_assignee,
                    'CAFETERIA/': 'CAFETERIA'
                }
                values.update(assignee_update)

        new_book.update({sheet.name: sheet_data})

        return new_book

    @classmethod
    def process_sheet_rows(cls, row, tag_column, sheet_data):
        """ Processes rows in the sheet

        Args:
            row (list): List to be processed
            tag_column (int): index for tag column
            sheet_data (list): multidimensional list to add processed row to

        Returns:
            sheet_data (list): updated multidimensional list
        """

        if '-' in str(row[tag_column]):
            assets = generate_rows_from_tag(
                row, tag_column)  # generate assets from joined tags
            [sheet_data.append(item) for item in assets]
        else:
            sheet_data.append(row)

        return sheet_data

    @classmethod
    def transform_amity_2_0(cls, sheet, new_book):
        """Transforms amity 2.0 google sheet

        Creates different sheets for each item description in the sheet

        Args:
            sheet (object): pyexcel sheet object
            new_book (dict): multidimensional dictionary to add the sheet to

        Returns:
            new_book (dict): multidimensional dictionary
        """
        sheet.delete_columns([0, 11])
        sheet.delete_rows([0])
        values = {'Good': 'ok', 'N/A': ''}
        sheets_data = {
            '1HP Split Unit Air Conditioner': [HEADERS],
            'Swivel Chair': [HEADERS],
            'Gascooker': [HEADERS],
            'Fridge': [HEADERS],
            'Water dispenser': [HEADERS],
            'Microwave': [HEADERS],
            'Gas cylinder': [HEADERS],
            'FUEL TANK 1500litres': [HEADERS],
            'Fire Extinguisher': [HEADERS],
            '7.5kva Inverter': [HEADERS],
            '3.5Kva': [HEADERS],
            'Generators': [HEADERS],
        }
        for row in sheet:
            rename_row_values(row, **values)
            current_sheet = row[2]
            tag_column = 0
            if has_data(row) and current_sheet in sheets_data.keys():
                cls.process_sheet_rows(row, tag_column,
                                       sheets_data[current_sheet])
            elif has_data(row) and 'Generator' in current_sheet:
                cls.process_sheet_rows(row, tag_column,
                                       sheets_data['Generators'])
        new_book.update(sheets_data)
        return new_book

    @classmethod
    def transform_it_devices(cls, sheet, new_book):
        """Transforms it devices sheet

        Args:
            sheet (object): pyexcel sheet object
            new_book (dict): `multidimensional` dictionary to add the sheet to

        Returns:
            new_book (dict): `multidimensional` dictionary
        """
        column_replacers = {
            'Code ID Ref.': 'Tag',
            'Location/Areas served': 'Assignee',
            "Model/Series/Colour/Material and Manufacturer's Ref. no":
            "Manufacturer's Ref. no",
            'Maintenance period/History': 'Maintenance period',
            'Warranty/Guarantee data': 'Warranty',
            'Condition': 'Status'
        }
        row_change = {'Good': 'OK'}

        sheet_headers = list(
            map(cls.clean_sheet_headers(column_replacers), sheet.row[1][2:]))

        change_cell_value(sheet, row_change)
        del sheet.row[0:2]
        sheet_data = [row[2:] for row in sheet]
        sheet_data.insert(0, sheet_headers)
        new_book.update({'IT Devices': sheet_data})
        return new_book

    @classmethod
    def transform_et_others(cls, sheet, new_book):
        """Transforms et others sheet

        Args:
            sheet (object): pyexcel sheet object
            new_book (dict): `multidimensional` dictionary to add the sheet to

        Returns:
            new_book (dict): `multidimensional` dictionary
        """
        del sheet.column[0, 5]
        sheet[0, 0] = 'Tag'
        sheet[0, 5] = 'Assignee'
        sheet_data = sheet_in_array(sheet)
        headers = sheet_data[0] + ['Status']
        new_data = []
        for row in sheet_data[1:]:
            if '-' in str(row[0]):
                rows = generate_rows_from_tag(row, 0)
                new_data = new_data + rows
            elif '-' not in str(row[0]):
                uniform_tag = '/'.join(row[0].split('/')[:-1])
                tag_limit = row[0].split('/')[-1]
                tag = validate_lower_limit(uniform_tag, tag_limit)
                row[0] = tag[2]
                new_data.append(row)

        new_sheets = {}
        for row in new_data:
            row = row + ['ok']
            new_sheets = group_assets(row, new_sheets, headers)
        new_book.update(new_sheets)
        return new_book

    @classmethod
    def transform_jm_1(cls, sheet, new_book):
        """Transforms jm 1 sheet
        Args:
            sheet (object): pyexcel sheet object
            new_book (dict): multidimential dictionary to add the sheet to
        Returns:
            new_book (dict): multidimential dictionary
        """
        column_replacers = {
            'Code ID Ref.': 'Tag',
            'Areas served': 'Assignee',
            "Model/Series/Colour/Material and Manufacturer's Ref. no":
            "Manufacturer's Ref. no",
            'Maintenance period/History': 'Maintenance period',
            'Warranty/Guarantee data': 'Warranty',
            'Condition': 'Status'
        }
        area_data = ['EQUIPMENTS', 'FURNITURE & FITTINGS']
        row_change = {'Good': 'OK', 'Fair': 'OK'}

        sheet_headers = list(
            map(
                cls.clean_sheet_headers(column_replacers),
                sheet.row[1][2:5] + sheet.row[1][6:-3]))

        change_cell_value(sheet, row_change)
        # delete 2 blank row that are at the top of the sheet
        del sheet.row[0:2]
        sheet_data = []
        # insert a new header to the the sheet_data list
        sheet_data.insert(0, sheet_headers)

        for row in sheet:
            row = row_to_remove(row, area_data, row[4])
            if row and '-' in row[2]:
                # deletes the selected columns
                remove_column(row, [0, 1, 5, 14, 15, 16])
                # new tags that contain `-` in their Tag column
                rows = generate_rows_from_tag(row, 0)
                sheet_data = sheet_data + rows
            elif row and '-' not in row[2]:
                # deletes the selected columns
                remove_column(row, [0, 1, 5, 14, 15, 16])
                sheet_data.append(row)
        new_book.update({'JM 1': sheet_data})
        return new_book
