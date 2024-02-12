"""Module for resource manipulation"""

from ..constants import EXCLUDED_FIELDS
from ..messages.error_messages import serialization_errors
from flask import request
from api.middlewares.base_validator import ValidationError

# Utilities
from api.models.database import db
from api.utilities.validators.validate_id import bulk_ids_validate
from ...utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import serialization_errors
from ...utilities.paginator import pagination_helper


def none_existing_id_checker(id_list, valid_instance_ids):
    """Checks for ids not found in the db, maps invalid ids to appropriate error messages
    Args:
        valid_instance_ids (list): list of ids from the db
        id_list (list): list of ids provided during bulk delete request
        Returns:
            (list): a list with no objects in db
    """
    id_not_found = []
    for id in id_list:
        if id not in valid_instance_ids:
            id_not_found.append(id)

    invalid_ids = invalid_id_mapper(id_not_found)

    return id_not_found, invalid_ids


def invalid_id_mapper(invalid_ids_list):
    """
    Args:
        invalid_ids_list (list): list of ids which are invalid
        Returns:
            (list): a list of dictionaries mapping object id to its error
    """

    if invalid_ids_list:
        map_invalid_id_to_error_list = [{
            id:
            serialization_errors['invalid_id_field']
        } for id in invalid_ids_list]
        return map_invalid_id_to_error_list


def map_not_found_to_id(id_not_found):
    """
    Args:
        id_not_found (list): list of ids not found in the db
        Returns:
            (list): a list of dictionaries mapping object id to its error
    """
    if id_not_found:
        map_not_found_to_id_list = [{
            id:
            serialization_errors['not_found'].format('Work order')
        } for id in id_not_found]

        return map_not_found_to_id_list


def join_error_all_errors(all_errors, id_not_found):
    """
    Args:
        all_errors (list): list of ids of object(s) to be deleted
        id_not_found(list):list of ids not found in the db
    """
    if id_not_found:  # tuple of a list of all invalid ids and ids not found in db
        invalid_ids_list, not_found_list = bulk_ids_validate(id_not_found[0])

        map_not_found_to_id_list = map_not_found_to_id(not_found_list)

        if map_not_found_to_id_list:
            all_errors.extend(map_not_found_to_id_list)
        if invalid_ids_list:
            map_invalid_to_id_list = invalid_id_mapper(invalid_ids_list)
            all_errors.extend(map_invalid_to_id_list)


def get_paginated_resource(model,
                           model_schema,
                           *success_message_args,
                           include_deleted=False):
    """Retrieves paginated resource
        Uses the model and model_schema to send a resource to the
        client
        Args:
            model (class): a subclass of BaseModel class
            model_schema (Marshmallow.Schema): the model schema
            *success_message_args:  the success message message argument
        Returns:
            (dict): returns the response back to the user
    """

    data, meta = pagination_helper(
        model, model_schema, include_deleted=include_deleted)
    return {
        "status": 'success',
        "message": SUCCESS_MESSAGES['fetched'].format(*success_message_args),
        "data": data,
        "meta": meta
    }


def get_all_resources(*args, **kwargs):
    """Retrieves all resources without pagination
    Args:
        model (class): Model to be paginated
        model_schema (class): Schema to be used for serialization
        extra_query (dict): Extra queries to be performed on the model
        exclude (list): Fields to be excluded by the schema provided
        only (list): Fields to be included by the schema provided
    Returns:
        (dict): returns the response back to the user
    """
    model, model_schema = args
    query = model.query_(None)

    extra_query, exclude, only, include_deleted = (kwargs.get(
        'extra_query', None), kwargs.get('exclude', EXCLUDED_FIELDS),
                                                   kwargs.get('only', None),
                                                   kwargs.get(
                                                       'include_deleted',
                                                       False))

    query_rows = query.include_deleted().filter_by(
    ) if include_deleted else query.filter_by()
    if extra_query and isinstance(extra_query, dict):
        try:
            query_rows = query_rows.filter_by(**extra_query)
        except:
            raise ValidationError(
                {'message': serialization_errors['invalid_field']})
    all_rows = query_rows.all()

    data = return_resource_data(model_schema, exclude, only, all_rows,
                                include_deleted)
    return data


def return_resource_data(*args):
    """Returns data depending on whether deleted is True or False
    Args:
        model (class): Model to be paginated
        model_schema (class): Schema to be used for serialization
        extra_query (dict): Extra queries to be performed on the model
        exclude (list): Fields to be excluded by the schema provided
        only (list): Fields to be included by the schema provided
    Returns:
        (dict): returns the response back to the user
    """
    model_schema, exclude, only, all_rows, include_deleted = args
    data = model_schema(
        many=True, exclude=exclude, only=only).dump(all_rows).data if not include_deleted else \
            model_schema(
            many=True, exclude=exclude, only=only).dump(all_rows, request_args={'include': 'deleted'}).data
    return data
