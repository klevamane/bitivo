"""Module for validating request-types input data"""

# Model
from api.models import User, RequestType
from flask import request

# validator
from ..error import raises, raise_error_helper
from api.utilities.messages.error_messages import serialization_errors

from ..constants import REQUEST_TYPE_TIME_MAX_VALUES, VALID_TIME_UNITS

joined_error_phrase = ' or '.join(VALID_TIME_UNITS)


def validate_request_types_date(time_dict, time_type):
    """ Validates closureTime, resolution time and response time in incoming request
    
    Args:
        time_dict (dict): A dictionary containing the days, hours and minutes
        time_type (str): the time type eg closureTime, resolutionTime or responseTime
    Returns:
       (dict): dictionary of time field
       None: when the request method is not a PATCH and the time_dict is not a dictionary
    """

    request_is_patch = request.method == 'PATCH'
    field_is_missing = time_dict is None and not request_is_patch
    raise_error_helper(field_is_missing, serialization_errors,
                       'missing_fields', time_type)

    default_time_dict = {time_unit: 0 for time_unit in VALID_TIME_UNITS}

    if not isinstance(time_dict, dict):  # default all the units to zero
        return raise_error_helper(not request_is_patch, serialization_errors,
                                  'invalid_request_type_time', time_type,
                                  joined_error_phrase)

    validate_request_types_date_helper(time_dict, time_type)
    sum_of_time_values = sum(time_dict.values())
    sum_is_lte_0 = sum_of_time_values <= 0
    comma_seperated_time_types = ', '.join(VALID_TIME_UNITS)
    raise_error_helper(sum_is_lte_0, serialization_errors, 'invalid_date_sum',
                       time_type, comma_seperated_time_types, '0')

    default_time_dict.update(**time_dict)

    return default_time_dict


def validate_request_types_date_helper(time_dict, time_type):
    """Checks the value of each time_type

    This function takes the a time_dict that contains days, minutes or hours
    and a time_type such as closureTime, responseTime or resolutionTime

    It performs validaion on each type in the time_dict by checking that:
        - days is >=0
        - hours >= 0 and <= 24
        - minutes >= 0 and <= 60
    Args:
        time_dict (dict) : with keys days, minutes or hours
        time_type:

    Returns:
        None

    Raises
        ValidationError:
            when the days, hours or minutes has an invalid value
    """

    for time_unit_from_user, time_value in time_dict.items():
        time_unit_is_valid = time_unit_from_user not in VALID_TIME_UNITS
        raise_error_helper(time_unit_is_valid, serialization_errors,
                           'invalid_request_type_time', time_type,
                           joined_error_phrase)

        max_value = REQUEST_TYPE_TIME_MAX_VALUES[time_unit_from_user]
        time_value_is_integer_and_gte_zero = \
            isinstance(time_value, int) and time_value >= 0

        time_unit_is_days = time_unit_from_user == "days"
        time_value_is_valid = time_value_is_integer_and_gte_zero and (
            time_unit_is_days or
            (not time_unit_is_days and time_value <= max_value))

        error_args_mapper = {
            'days': ['invalid_day_in_date_input', time_type, 'days', '0']
        }

        error_args = error_args_mapper.get(
            time_unit_from_user,
            ['invalid_date_input', time_unit_from_user, max_value])

        raise_error_helper(not time_value_is_valid, serialization_errors,
                           *error_args)


def validate_user_a_member_of_center(data):
    """ Checks if a user belong to the specified center

    Args:
        data (dict): A dictionary containing the request object

    Raises:
        ValidationError: If a user does not belong to the specified center
    """
    assignee_id = data.get('assignee_id')
    center_id = data.get('center_id')
    user = User.query_().filter_by(
        token_id=assignee_id, center_id=center_id).first()
    if not user:
        raises('user_not_found', 400, 'User')


def validate_request_type_exist_in_center(data, request_type_id):
    """ Checks if a request type already exist in a center

        If the request URL method is a PATCH meaning we want
        to update a request type, error will not be raised

    Args
        data (dict): A dictionary containing the request object

    Raises:
        ValidationError: If a request type already exist in a center
    """

    request_type = RequestType.query_() \
    .filter_by(center_id=data.get('center_id'), title=data.get('title')).first()

    if request.method == 'PATCH':
        if request_type:
            request_type = request_type.id != request_type_id

    if request_type:
        raises('exists', 400, data.get('title'))
