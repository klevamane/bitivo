"""Checks if resource should be paginated or not"""
from api.utilities.helpers.resource_manipulation import get_all_resources
from api.utilities.paginator import pagination_helper
from api.utilities.constants import EXCLUDED_FIELDS


def should_resource_paginate(*args, **kwargs):
    """
    Args:
        request: flask request object
        model: model to run queries on
        model_schema: schema to use for serialization
    Returns:
        tuple: data and the meta object
    """
    only = kwargs.get('only', None)
    excluded_fields = kwargs.get('exclude', EXCLUDED_FIELDS)
    extra_query = kwargs.get('extra_query', None)

    request, model, model_schema = args
    query_dict = request.args.to_dict()

    include = query_dict.get('include')

    if ('pagination' in query_dict \
        and query_dict['pagination'].lower() == 'false'):
        data_ = get_all_resources(
            model,
            model_schema,
            only=only,
            exclude=excluded_fields,
            extra_query=extra_query)

        # include deleted feild in returned data if include=deleted
        exclude = excluded_fields.copy()
        exclude.remove('deleted')

        data = get_all_resources(
            model,
            model_schema,
            only=only,
            exclude=exclude,
            extra_query=extra_query,
            include_deleted=True) if include == 'deleted' else \
                data_
        pagination_object = None
    else:
        data, pagination_object = return_data(
            model,
            model_schema,
            only,
            excluded_fields,
            extra_query,
            include=include)

    return data, pagination_object


def return_data(*args, **kwargs):
    """
    Args:
        include(str): parameter to determine whether deleted objects are to be included
                      in response or not
        model(obj): model to run queries on
        model_schema(obj): schema to use for serialization
    Returns:
        tuple: data and the meta object
    """

    include = kwargs.get('include')
    model, model_schema, only, excluded_fields, extra_query = args

    if include == 'deleted':
        # include deleted feild in returned data if include=deleted
        exclude = excluded_fields.copy()
        exclude.remove('deleted')

        data, pagination_object = pagination_helper(
            model,
            model_schema,
            only=only,
            exclude=exclude,
            extra_query=extra_query,
            include_deleted=True)
        return data, pagination_object

    return pagination_helper(
        model,
        model_schema,
        only=only,
        exclude=excluded_fields,
        extra_query=extra_query)
