import pyexcel as pe
from ..validators.asset_migration_validators import validate_sheet_file_upload
from ..constants import XLSX
from ...middlewares.base_validator import ValidationError
from ..messages.error_messages import serialization_errors 


def get_book(request_obj):
    """
    """
    # get and read the file upload
    file = validate_sheet_file_upload(request_obj.files.get('file'))
    filename = file.filename
    extension = filename.split(".")[-1]
    if extension != XLSX:
        raise ValidationError({'message': serialization_errors['invalid_file_type'].format(extension)})
    data = file.read()
    book = pe.get_book_dict(file_type=extension, file_content=data)
    return book
