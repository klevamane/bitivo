"""Module for validating analytics request"""

# Standard Library
from functools import wraps

# Third Party Library
from flask import request

# Local Module
from ..error import raises


def report_query_validator(report_queries):
    """Validates report query

    Checks if the report query is one of the item in the report_queries

    Args:
        report_queries (list): a list of supported queries
    Returns:
        function
    """

    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            report_query = request.args.get('report', '').lower().strip()

            if report_query and report_query not in report_queries:
                raises('invalid_request_param', 400, 'report query', ', '.join(report_queries))
            else:
                # to make the function wrapped by the decorator accept more
                # arguments and report_query has to be passed, to whatever
                # function the decorator is used for, remember to make
                # report_query the last positional argument for the function
                return func(*args, report_query, **kwargs)

        return decorated_function

    return decorator


def hot_desk_query_validator(hot_desk_queries):
    """
    Validates the query param passed to the hot-desks endpoint

    Checks if the query parameter is in the hot_desk_queries, raises error otherwise

    Args:
        hot_desk_queries (list): a list of supported query parameters
    Returns:
        function

    """

    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            hotdesk_query = request.args.to_dict()
            query_key = hotdesk_query_key(hotdesk_query, hot_desk_queries)

            if query_key in hot_desk_queries:
                return func(*args, hotdesk_query[query_key], **kwargs)
            raises('invalid_request_param', 400, 'query param', ', '.join(hot_desk_queries))
        return decorated_function

    return decorator


def hotdesk_query_key(hotdesk_query, hot_desk_queries):
    """
    A function to get query_key from hot desk request query params

    args:
        hotdesk_query(dict): A dict with query param key and value
        hot_desk_queries(list): A list of hot desk query param keys
    return:
        query_key(str): query key passed by user or
                        Raises validation error
    """
    if not hotdesk_query:
        raises('invalid_request_param', 400, 'query param', ' or '.join(hot_desk_queries))
    for query_key in hotdesk_query:
        return query_key
