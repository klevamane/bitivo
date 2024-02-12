import re
import difflib

from api.utilities.helpers.asset_rows import remove_empty_row, update_column_row


def generate_tags(*args):
    """Generates tags from tag limit
    Args:
        args (list):
            0 (list): a list of tag limit.
            1 (list): unique key for validation. e.g Tag
            2 (list): True for invalid status and False for valid status
            3 (str): True for exists and False if it does not exist
    Returns:
        None
    """
    tag_limit, row, new_rows, uniform_tag, tag_index = args
    difference = 0  # range of tag number
    lower_tag_limit = tag_limit[0]
    if len(tag_limit) > 1:  # [069, 080]
        difference = int(tag_limit[1]) - int(tag_limit[0])
        if difference < 0:
            difference = int(tag_limit[0]) - int(tag_limit[1])
            lower_tag_limit = tag_limit[1]
    for number in range(difference + 1):
        new_row = row[:]  # extract zero numbers before tag number
        zero_before_number = get_zero_before_number(tag_limit[0])
        tag_number = int(lower_tag_limit) + number
        tag_number = ''.join(zero_before_number) + str(tag_number)
        new_tag = f'{uniform_tag}/{tag_number}'
        new_row.insert(tag_index, new_tag)
        new_rows.append(new_row)
    return new_rows


def get_zero_before_number(data):
    """Method to extract zero numbers present before tag number
    Args:
        data (str): string of a number

    Returns:
        list: list of zero string
    """
    zeros = []
    for number in data:
        if number == '0':
            zeros.append(number)
        else:
            return zeros
    return zeros


def validate_lower_limit(uniform_tag, lower_limit):
    """Method to catch value error if tag number contains a  string and format the number
    Args:
        uniform_tag (str): a uniform tag eg AND/TC/HG
        lower_limit (str): tag number lower range which may or may not contain a letter string egT009 or 009
     Returns:
        list: multidimentional list of rows
    """
    number = []
    string_value = []
    for i in lower_limit:
        try:
            int(i)
            number.append(i)
        except ValueError:
            string_value.append(i)
    number_tag = ''.join(number)
    string_tag = ''.join(string_value)
    uniform_tag = f'{uniform_tag}/{string_tag}' if string_tag else uniform_tag
    full_tag = f'{uniform_tag}/{number_tag}' if uniform_tag else ''
    return uniform_tag, number_tag, full_tag


def has_data(data):
    """Checks if there values in the list
    Args:
        data (list): list to be checked

    Returns:
        boolean: true or false
    """
    res = [x for x in data if x]
    return True if len(set(res)) > 1 else False


def change_string_value(row, string, index, **kwargs):
    """ Changes items in a list

    Args:
        row (list): list to be editted
        string (str): item in list be checked
        index (int): index of the string

    Returns:
        list: editted list
    """
    for key, value in kwargs.items():
        if key in str(string):
            row[index] = value
    return row


def split_column(data, start):
    """Method to extract wanted columns
    Args:
        data (list): list of columns
        start (num): starting index of needed columns
    Returns:
        list: list of zero string
    """
    new_data = []
    for row in data:
        new_data = new_data + [row[start:10]]
    return new_data


def add_status_header(data, status_mapper, header):
    """Method to add corressponding status to a column based on the  assigneee

    Args:
        data (dict): dict mapping status with corressponding assignee
        status_mapper (dict): status mapper
        header (dict): sheet headers

    Returns:
        list: list of zero string
    """
    for row in data:
        status = status_mapper.get(row[3].lower()) or 'Assigned'
        row += [status]
    data[0] = header
    return data


def sheet_in_array(sheet):
    """Method to add corresponding status to a column based on the assignee

    Args:
        sheet (excel): the sheet

    Returns:
        list: list of zero string
    """
    sheet_data = []
    for row in sheet:
        row = remove_empty_row(row)
        if row:
            sheet_data += [row]
    return sheet_data


def change_cell_value(sheet, cell_data):
    """Method to change the cell value in a cell
    Args:
        sheet (obj): pyexcel sheet object
        cell_data (dict): Dict for cell data with old cell data
          as key and new cell data as value
     Returns:
        update_column_row (func): Function that will update the new column cell
    """
    for row in sheet.row_range():
        for column in sheet.column_range():
            update_column_row(sheet, cell_data, row, column)


def swap_column_value_in_usb_dongle_sheet(first_list, second_list):
    """swap values in column in transforming usb-c dongle

        Args:
            first_list (List): list to iterate over
            second_list (List): list to update


        Returns:
            column (List): an updated list
    """
    word_find = ['Faulty', 'Replaced', 'Changed']
    for x in first_list:
        if x in word_find:
            index_of_x = first_list.index(x)
            first_list[index_of_x] = ''
            second_list[index_of_x] = x


def replace_unwanted_string(data):
    """Replace unwanted string from column

            Args:
                data (List): List to iterate over

            Returns:
                column (List): an updated list of wanted values
            """
    case_ignore = re.compile('prev user:', re.IGNORECASE)

    data = [re.sub(case_ignore, '', x) for x in data]

    return data


def group_assets(row, new_sheets, headers):
    new_row = row[2].replace("/", "-")
    match = [
        key for key, value in new_sheets.items()
        if difflib.SequenceMatcher(None, key, new_row).ratio() > 0.80
    ]
    if match:
        new_sheets[match[0]].append(row)
    elif row[2]:
        new_sheets.update({new_row: [headers]})
        new_sheets[new_row].append(row)
    return new_sheets


def sheet_headers(sheet_header, column_replacers, index_list, **kwargs):
    """Method to replace an excel colomn, add new coloumn or remove a column.
    Args:
        sheet_header (list): list of column data in a excel sheet
        column_replacers (dict): the key is the column to be replaced while the value is the new column
        index_list (list): an int list of column index to be removed
        kwargs: a key word argument where the key can be any character but the value must be a new column name to be added
 
    Returns:
        list: a list of sheet columns
    """

    sheet_header = remove_column(sheet_header, index_list)

    for item, values in kwargs.items():
        sheet_header.append(values)

    return list(
        map(
            lambda x: column_replacers.get(x.strip())
            if str(x).strip() in column_replacers else x, sheet_header))


def remove_column(row, index_list):
    """Method to remove a column.
    Args:
        row (list): list of column data in a excel sheet
        index_list (tuple or list): a list of column index to be removed
    Returns:
        list: a list of sheet columns
    """
    i = 0
    for index in index_list:
        del row[index - i]
        i += 1
    return row
