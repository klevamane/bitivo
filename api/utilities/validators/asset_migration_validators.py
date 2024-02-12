"""
Module for validating the asset migration inputs
"""

# Validators
from api.middlewares.base_validator import ValidationError

# messages
from api.utilities.messages.error_messages import MIGRATION_ERRORS, database_errors


def validate_sheet_name_input(sheet_name, book):
    """ validates the input data from the user
    
    Handles the validation of the user input and checks if is
    valid name.
    Args:
        sheet_name (str): The input data sent from the user
        book (dict): a dictonary object of the excel data
    Returns:
        sheet_name (str): A valid string is returned back
    """
    all_sheet_names = [key.lower() for key in book.keys()]

    if sheet_name not in all_sheet_names:
        raise ValidationError(
            {
                'message': MIGRATION_ERRORS['not_found'].format(sheet_name)
            }, 400)

    return sheet_name


def migration_get_or_404(name, model, resource_name):
    """ Get asset category
    Get the asset category object by querying the asset category table
    Args:
        name (str): the asset category name
    Returns:
        category (object): returns the object of the the asset category
    """

    result = model.query_().filter(model.name.ilike(name)).first()
    if not result:
        raise ValidationError({
            'message':
            database_errors['non_existing'].format(f'{name} {resource_name}')
        }, 404)
    return result


def validate_sheet_file_upload(file):
    """ Validates the sheet upload
    validates the file upload to ensure that it doesnt crash
    when user doesnt upload a sheet data
    Args:
        file (obj): excel sheet file uploaded by user
    Returns:
        file (obj): returns the file object if its not empty else raises validation error 
    """
    empty_file_names = ['3e9', '527']
    if not file or file and file.filename in empty_file_names:
        raise ValidationError({'message': MIGRATION_ERRORS['no_file']}, 400)
    return file