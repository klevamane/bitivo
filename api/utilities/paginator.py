"""Module for pagination helpers"""

# Standard
import re
from math import ceil

# Third Party Libraries
from flask import request

# Utilities
from api.utilities.query_parser import QueryParser

# Messages
from .messages.error_messages import serialization_errors

# Middlewares
from ..middlewares.base_validator import ValidationError

# Constants
from .constants import EXCLUDED_FIELDS


def validate_pagination_args(arg_value, arg_name):
    """
    Validates if the query strings are valid.

    Arguments:
        arg_value (string): Query string value
        arg_name (string): Query string name

    Raises:
        ValidationError: Use to raise exception if any error occur

    Returns:
        (int) -- Returns True or False
    """

    if arg_name == 'limit' and arg_value == 'None':
        return 10  # Defaults limit to 10 if not provided
    if arg_name == 'page' and arg_value == 'None':
        return 1  # Defaults page to 1 if not provided

    # Checks if the arg is >= 1
    if arg_value.isdigit() and int(arg_value) > 0:
        return int(arg_value)
    else:
        raise ValidationError({
            'message':
            serialization_errors['invalid_query_strings'].format(
                arg_name, arg_value)
        })


def generate_metadata(records_count):
    """Generates the pagination metadata object

    Args:
        records_count (int): The total record count

    Returns:
        tuple: A tuple with the limit, offset and pagination meta dict
    """
    limit = validate_pagination_args(
        request.args.get('limit', 'None'), 'limit')
    root_url = request.url_root.strip('/')
    base_url = f'{root_url}{request.path}'
    new_base_url = get_param_based_url(base_url)
    current_page_url = request.url
    current_page_count = validate_pagination_args(
        request.args.get('page', 'None'), 'page')
    first_page = get_first_page(base_url, new_base_url, limit)
    pages_count = ceil(records_count / limit)

    # when there are no records the default page_count should still be 1
    if pages_count == 0:
        pages_count = 1

    meta_message = None
    if current_page_count > pages_count:
        # If current_page_count > pages_count set current_page_count to pages_count
        current_page_count = pages_count
        first_page = get_first_page(base_url, new_base_url, limit)
        current_page_url = get_current_page(base_url, new_base_url,
                                            pages_count, limit)
        meta_message = serialization_errors['last_page_returned']

    offset = (current_page_count - 1) * limit

    # pagination meta object
    pagination_object = {
        "firstPage": first_page,
        "currentPage": current_page_url,
        "nextPage": "",
        "previousPage": "",
        "page": current_page_count,
        "pagesCount": pages_count,
        "totalCount": records_count
    }

    previous_page_count = current_page_count - 1
    next_page_count = current_page_count + 1

    next_page_url = get_next_page(base_url, new_base_url, next_page_count,
                                  limit)
    previous_page_url = get_previous_page(base_url, new_base_url,
                                          previous_page_count, limit)

    if current_page_count > 1:
        # if current_page_count > 1 there should be a previous page url
        pagination_object['previousPage'] = previous_page_url

    if pages_count >= next_page_count:
        # if pages_count >= next_page_count there should be a next page url
        pagination_object['nextPage'] = next_page_url

    if meta_message:
        pagination_object['message'] = meta_message

    return limit, offset, pagination_object


@QueryParser.parse_queries
def pagination_helper(*args, **kwargs):
    """Paginates records of a model.

    Usage:
        To use this function, the positional arguments (args) must be supplied in the right order e.g

        Example1: pagination_helper(model, schema)
        In the above example the keyword arguments will be set to their default values (exclude=EXCLUDED_FIELDS,
        only=None, extra_query=None)

        The the keyword arguments (kwargs) are optional i.e. any or none of the kwargs could be supplied e.g

        Example2: pagination_helper(model, schema, exclude=EXCLUDED_FIELDS, only=['name', 'type'], extra_query=None)


    Args:
        model (class): Model to be paginated
        schema (class): Schema to be used for serialization
        extra_query (dict): Extra queries to be performed on the model
        exclude (list): Fields to be excluded by the schema provided
        only (list): Fields to be included by the schema provided

    Returns:
        tuple: Returns a tuple containing the paginated data and the
            paginated meta object or returns a tuple of None depending on
            whether the limit and page object is provided
    """

    model, schema, = args

    extra_query, exclude, only, include_deleted = (kwargs.get(
        'extra_query', None), kwargs.get('exclude', EXCLUDED_FIELDS),
                                                   kwargs.get('only', None),
                                                   kwargs.get(
                                                       'include_deleted',
                                                       False))
    query = model.query_(request.args, include_deleted=include_deleted)

    records_query = query.filter_by()

    # Checks if they are extra queries to perform on the model
    if extra_query and isinstance(extra_query, dict):
        try:
            records_query = records_query.filter_by(**extra_query)
        except:
            # Raise a validation error if the keys in the extra
            # queries are not part of the models fields
            raise ValidationError(
                {'message': serialization_errors['invalid_field']})

    records_count = records_query.count()
    limit, offset, pagination_object = generate_metadata(records_count)
    records = records_query.offset(offset).limit(limit)

    data = schema(
        many=True, exclude=exclude, only=only).dump(records.all()).data

    if include_deleted:
        data = handle_delete_condition(exclude, schema, only, records)

    return data, pagination_object


def handle_delete_condition(exclude, schema, only, records):
    """returns resource data including deleted resources in case a
    resources is requested with include=deleted params
    """

    # define request args to send to dump method
    args = {'include': 'deleted'}
    exclude_ = exclude.copy()
    if 'deleted' in exclude_:
        # allow deleted feild to be included in results of deleted objects
        exclude_.remove('deleted')
    data = schema(
        many=True, exclude=exclude_, only=only).dump(
            records.all(), request_args=args).data
    return data


def list_paginator(list_data, paginate=None):
    """Paginate data that is in list form

    Args:
        list_data (list): the list of data to paginate
        paginate (bool): if false return all else paginate

    Returns:
        tuple: A tuple with the paginated items and the pagination metadata
    """
    if paginate == False:
        return list_data, None
    limit, offset, meta = generate_metadata(len(list_data))
    results = list_data[offset:offset + limit]
    return results, meta


def get_param_based_url(base_url):
    """ Method to get base url if request is param based 
    args:
        base_url(str): the base request url
    returns:
        new_base_url(str): The request url with query params
    """
    query_param = get_query_param()
    if query_param:
        new_base_url = f'{base_url}?{query_param[0]}'
        return new_base_url


def get_first_page(base_url, new_base_url, limit):
    """ Method to get the first paginated page
    args:
        base_url(str): The base request url
        new_base_url(str): The request url with query params
        limit(int): The count of data to be returned
    returns:
        first_page(str): The first paginated page
    """
    first_page = f'{new_base_url}&page=1&limit={limit}' if new_base_url \
        else f'{base_url}?page=1&limit={limit}'
    return first_page


def get_next_page(base_url, new_base_url, next_page_count, limit):
    """ Method to get the first paginated page
    args:
        base_url(str): The base request url
        new_base_url(str): The request url with query params
        next_page_count(int): The count of pages after the current page
        limit(int): The count of data to be returned
    returns:
        next_page_url(str): The next paginated page
    """
    next_page_url = f'{new_base_url}&page={next_page_count}&limit={limit}' \
        if new_base_url else f'{base_url}?page={next_page_count}&limit={limit}'
    return next_page_url


def get_previous_page(base_url, new_base_url, previous_page_count, limit):
    """ Method to get the first paginated page
    args:
        base_url(str): The base request url
        new_base_url(str): The request url with query params
        previous_page_count(int): The count of pages before the current page
        limit(int): The count of data to be returned
    returns:
        previous_page_url(str): The previous paginated page
    """
    previous_page_url = f'{new_base_url}&page={previous_page_count}&limit={limit}' \
        if new_base_url else f'{base_url}?page={previous_page_count}&limit={limit}'
    return previous_page_url


def get_current_page(base_url, new_base_url, pages_count, limit):
    """ Method to get the current page url
    args:
        base_url(str): The base request url
        new_base_url(str): The request url with query params
        pages_count(int): The total count of pages
        limit(int): The count of data to be returned
    returns:
        current_page_url(str): The current paginated page
    """
    current_page_url = f'{new_base_url}&page={pages_count}&limit={limit}' \
        if new_base_url else f'{base_url}?page={pages_count}&limit={limit}'
    return current_page_url


def get_query_param():
    """ Method to get the query param keys from requests args
    returns
        list: the query param
    """
    query_param = re.findall(r'\?(.*)', request.url)
    if query_param and 'page' in query_param[0]:
        query_param = re.findall(r'(.*)\&page', query_param[0])
    return query_param


def get_pagination_option():
    """A function to get the pagination option passed
    in the query params
    Returns:
        bool: pagination option"""

    paginate = False if request.args.to_dict().get(
        'pagination', '').upper().strip() == 'FALSE' else True

    return paginate
