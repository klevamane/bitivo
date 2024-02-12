"""Module to validates categories """
# Third party imports
from flask import g
from marshmallow import ValidationError

# Helpers
from ..messages.error_messages import serialization_errors
from .validate_id import is_valid_id


def validate_category_exists(model, category_id):
    """Marshmallow function to verify a category exists in the db.
    
    Args:
        model (obj): model to check in 
        category_id (str): id of the category to check
    
    Raises:
        ValidationError: Marshmallow Validation error if the asset category doesn't exist.
    """
    if not is_valid_id(category_id):
        raise ValidationError(serialization_errors['invalid_id'])

    category = model.get(category_id)

    if not category:
        raise ValidationError(serialization_errors['category_not_found'])
    else:
        # add category to g object so it stays in request context to avoid
        # another query to db on category.
        g.category = category
