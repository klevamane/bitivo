"""Module contains function to remove whitespaces in schema"""


def remove_whitespace(data, field, field_exists):
    """Function to remove white space in data fields

    Args:
      data(dict): a dictionary containing fields
      field(str): a field in the data
      field_exists(bool): boolean value to indicate if the
      field exists


      Example:

      data = {
        "title": " an activo       application "
      }
      cleanup_data_field(data, 'title', data.get('title'))
    """
    if field_exists:
        data[field] = " ".join(data[field].split())
