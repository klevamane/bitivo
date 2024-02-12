def remove_empty_row(row):
    """Method to check if empty rows is in a sheet
    Args:
        row (list): list of data in a excel sheet
    Returns:
        list: if not empty
        bool: if empty
    """
    for item in row:
        if item != '':
            return row
    return False


def generate_rows_from_tag(row, tag_index):
    """Method to generate excel rows from tag range
    Args:
        row (list): list of data in a excel sheet

    Returns:
        list: multidimentional list
    """
    from api.utilities.helpers.asset_transformer import validate_lower_limit, generate_tags
    new_rows = []
    tag = row[tag_index]  # tag eg AND/FE/SC/0009-18
    del row[tag_index]
    tag_fractions = tag.split('/')  # tag that will be same in the rows eg AND/FE/SC  ==>> AND/LA/ET/AC/001-008, 025-039
    uniform_tag = '/'.join(tag_fractions[:-1])
    tag_ranges = tag_fractions[-1]  # list of lower and upper tag limit eg [0009, 18]
    if ',' in tag_ranges:
        tag_ranges = tag_ranges.replace(' ', '').split(',')  # ['0009-18', '025-039']
    else:
        tag_ranges = [tag_ranges]
    for tag_range in tag_ranges:
        tag_limit = tag_range.split('-')
        uniform_tag, tag_limit[0], full_tag = validate_lower_limit(uniform_tag, tag_limit[0])
        generate_tags(tag_limit, row, new_rows, uniform_tag, tag_index)
    return new_rows


def rename_row_values(row, **kwargs):
    """Rename given strings in a list

    Args:
        row (list): the list with asset data

    Returns:
        list: list with occurences of the keys changes to values in the kwargs
    """
    from api.utilities.helpers.asset_transformer import change_string_value
    for index, string in enumerate(row):
        change_string_value(row, string, index, **kwargs)
    return row


def update_column_row(*args):
    """Methods loops through the cell value to replace cell data key with a value"""
    sheet, cell_data, row, column = args

    for key, value in cell_data.items():
        if sheet.cell_value(row, column) == key:
            sheet[row, column] = value


def row_to_remove(row, row_data, area_name):
    """Method to check if a particular data exist in the row.
    Args:
        row (list): list of column data in a excel sheet
        row_data (list): a list of data to compare
        area_name (str): area name or wing name
    Returns:
        list: a list of sheet columns if the data is not in row_data
        bool: if the a particular data is present in a cell
    """
    if area_name in row_data:
        return False
    return row
