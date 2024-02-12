""" Module for validating hot desk resource """

from ..error import raises
from ..constants import HOT_DESK_STATUS_VALUE, HOT_DESK_TRUE_VALUE, HOT_DESK_CANCELLATION_VALUE


def validate_hot_desk_status(status):
    """ Function that validates hot desk requests status
    args:
        status(str): Hot desk request status
    raises:
        validation errors.
    """
    if not status:
        raises('required_param_key', 400, 'status')
    if status and status not in HOT_DESK_STATUS_VALUE:
        raises('invalid_request_param', 400, 'status query param value',
               ', '.join(HOT_DESK_STATUS_VALUE))


def validate_param_value(param_value):
    """ Function that validates hot desk param value
     args:
         param_value(str): Hot desk request param value
     raises:
         validation errors.
     """
    value = param_value.lower().strip()
    if value not in HOT_DESK_TRUE_VALUE:
        raises('invalid_request_param', 400, 'param value',
               ', '.join(HOT_DESK_TRUE_VALUE))

def validate_cancellation_reason(cancellation_reason):
    """ Function that validates hot desk cancellation reason param value
     args:
         cancellation_reason(str): Hot desk cancellation reason param value
     raises:
         validation errors.
     """
    if not cancellation_reason:
        raises('required_param_key', 400, 'cancellation reason')
    if cancellation_reason not in HOT_DESK_CANCELLATION_VALUE:
        raises('invalid_request_param', 400, 'cancellation reason param value',
               ', '.join(HOT_DESK_CANCELLATION_VALUE))
