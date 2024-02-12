"""Module to validate form data request"""

# Functools
from functools import wraps

# Flask
from flask import request

# Utilities
from ..messages.error_messages import serialization_errors
from ...middlewares.base_validator import ValidationError
from ..enums import AssetSupportingDocumentTypeEnum, get_enum_fields

def validate_form_data_request(func):
    """Decorator function to check for form-data content type in request"""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not request.form:
            raise ValidationError(
                {
                    'status': 'error',
                    'message': serialization_errors['form_data_type_required']
                }, 400)
        return func(*args, **kwargs)

    return decorated_function


def validate_document_type(func):
    """Decorator function to check that document type in
    request is not empty and is in AssetSupportingDocumentEnum

    Args:
        func(function) Function

    Returns:
          function: Returns function if no errors

    Raises:
        ValidationError: If the document type is incorrect
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        document_type = request.form.get('documentType')
        if not document_type:
            raise ValidationError(
                {
                    'status': 'error',
                    'message': 'An error occured',
                    'errors':{
                            'documentType': [
                                serialization_errors['not_empty']
                            ]
                        }
                    
                }, 400)
        document_types = get_enum_fields(AssetSupportingDocumentTypeEnum)
        choices = str(document_types).strip('[]')
        if document_type.lower() not in document_types:
            raise ValidationError(
                {
                    'status': 'error',
                    'message': 'An error occured',
                    'errors':{
                            'documentType': [
                                serialization_errors['invalid_document_type'].format(choices=choices)
                            ]
                        }
                }, 400)
        
        return func(*args, **kwargs)

    return decorated_function
