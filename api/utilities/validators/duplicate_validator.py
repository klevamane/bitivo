"""Module for validating duplicate data"""

# Standard library
import re

# Third party
from humps.camel import case

# Error
from ..error import raise_error, raises


def validate_duplicate(model, message="", **kwargs):
    """
    Checks if model instance already exists in database

    Parameters:
         model(object): model to run validation on
         kwargs(dict): keyword arguments containing fields to filter query by
    """

    record_id = kwargs.get('id')
    kwargs.pop('id', None)  # remove id from kwargs if found or return None

    query = dict(deleted=False, **kwargs)
    if record_id:
        result = model.query.filter_by(**query).filter(
            model.id == record_id).first(
        )  # selects the first query object for model records

        if result:
            return None  # return None if query object is found

    if not message:
        message = f'{re.sub(r"(?<=[a-z])[A-Z]+",lambda x: f" {x.group(0).lower()}" , model.__name__)}'

    # check name column for duplications
    validate_name_duplicate(model, message, kwargs)

    result = model.query.filter_by(**query).first()
    if result:
        raises('exists', 409, message)


def validate_input_duplicate(data, resource_ids_set, resource_id_type):
    """Validate that an id is not duplicated within a request body.

    It is used to validate that a particular Id has not been wrongfully
    repeated in the body of a post request. Eg. repeating the value of
    assetCategoryId when recording stock count

    Args:
        data (dict): Contains individual element of a collection
            passed in the request body.
        resource_ids_set (set): Resource_ids set.
        resource_id_type (str): Type of id to be checked for duplication,
            eg "asset_category_id".

    Raises:
        ValidationError: If an id is duplicated.
    """

    # Get resource id from data
    resource_id = data.get(resource_id_type)
    # Check if resource_id in set
    if resource_id in resource_ids_set:
        raise_error('duplicate_found', resource_id_type.replace('_', ' '),
                    **{'fields': case(resource_id_type)})
    # Add resource_id to set if not already present.
    if resource_id:
        resource_ids_set.add(resource_id)


def title_case_and_validate(model, data_arg, data):
    """Convert a center name or role title to title case and
    validate it.

        Args:
            model (object): The model to be validated for duplicate.
            data_arg (str): The key to be converted to title case, should
            be either one of ['name', 'title'].
            data (dict): keyword arguments to filter validation query by

        Raises:
            ValidationError: If an id is duplicated.
        """
    if data_arg in data.keys():
        data[data_arg] = data[data_arg].title()
        args = {data_arg: data[data_arg], 'id': data.get('id')}
        validate_duplicate(model, **args)


def validate_name_duplicate(model, message, data):
    """Checks for any duplications in the name column

    Args:
        model (object): The model to be validated for duplicate.
        message (str): response message
        data (dict): keyword arguments to filter validation query by

    Returns:
        ValidationError: If the name is duplicated.

    """

    name = data.get('name')

    if name:
        result = model.query.with_entities(model.name)\
            .filter(model.name.ilike(name), model.deleted == False).first()

        if result and result[0].lower() == name.lower():
            raises('exists', 409, name)
