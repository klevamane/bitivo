"""Module that validates the query parameter
for getting hot_desk_allocation_report
"""
from ..error import raises
from ...utilities.constants import HOT_DESK_REPORT_FREQUENCY


def validate_query_param(request, query_keys):
    """
    Function that validates the request query param of the get all hot-
    desk allocation endpoint

    Args (request): Request object

    """
    if request.args:
        parameter_dict = request.args.to_dict()
        [
            raises('invalid_query_key', 400, query_keys) \
                for key in parameter_dict
            if key not in query_keys
        ]


def validate_frequency_value(frequency):
    """
    Function that validates the value passed to the 
    frequency query param

    Args (frequency): Value passed to the frequency query param

    """
    if frequency not in HOT_DESK_REPORT_FREQUENCY:
        raises('invalid_choice', 400, 'frequency', HOT_DESK_REPORT_FREQUENCY)
