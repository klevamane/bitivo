"""Validate query to get single space with children"""
from api.middlewares.base_validator import ValidationError
from ..messages.error_messages import serialization_errors


def validate_query(query, included_fields):
    """
    Validates query in request

    Parameters:
        query (str): The query passed by the user
        included_fields (array): Space fields to filter within the schema

    Raises:
        (ValidationError): Used to raise exception if validation
        of query fails
    """
    # convert to lower case and compare to 'children'
    if query.get('include', '').lower() == 'children':
        included_fields.append('children')
    elif query:
        raise ValidationError({
            'status': 'error',
            'message': serialization_errors['invalid_query']
        }, 400)
