from api.utilities.error import raises


def validate_sort_column(sort_column, valid_sort_columns):
    """Validates if the sort column.

    Arguments:
        sort_column (string): the column to be validated
        valid_sort_columns (List): a list of valid columns


    Raises:
        raises: Use to raise exception if any error occur

    Returns:
        (string) -- Returns the sort column if valid
    """

    if sort_column not in valid_sort_columns:
        raises('invalid_query_strings', 400, 'sort query', sort_column)

    return sort_column
