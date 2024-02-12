""" Module for validating support documents"""
from marshmallow import ValidationError
from ..messages.error_messages import serialization_errors

from ..enums import AssetSupportingDocumentTypeEnum, get_enum_fields


def validate_supporting_document_type(document_type):
    """
    Used to validate support document types

    Arguments:
        document_type (object): field to be validated

    Raises:
        ValidationError: Used to raise exception if status field is
        not in ["Purchase reciepts", "Repair reciepts"]
    """ 

    types = get_enum_fields(AssetSupportingDocumentTypeEnum)
    if document_type.value.lower() not in types:
        choices = str(types).strip('[]')
        raise ValidationError(
            serialization_errors[
                'invalid_document_type'].format(choices=choices))
