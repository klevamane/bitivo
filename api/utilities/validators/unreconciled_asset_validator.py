from api.utilities.error import raises
from datetime import datetime


def validate_request_param(request):
    """ validate the request parameters passed.

    Args:
        request(object):request object recieved in the views

    Returns:
        parameter(dict): returns the validated request parameter values
    """

    parameter_keys = ('startDate', 'endDate', 'page', 'limit')
    parameter_dict = request.args.to_dict()

    [
        raises('invalid_param_key', 400, parameter_keys)
        for key in parameter_dict if key not in parameter_keys
    ]

    datetime_dict = get_dates_dict(parameter_dict)
    # validate the parameter keys values.
    for param, date_value in datetime_dict.items():
        if not date_value:
            raises('missing_entry', 400, param)
        try:
            date_stripped = datetime.strptime(date_value, '%Y-%m-%d')
            parameter_dict[param] = "'{}'::date".format(date_stripped)

        except ValueError:
            raises('invalid_date', 400, date_value)
            
    parameter_dict['skip_filter'] = True

    return parameter_dict

def get_dates_dict(param_dict):
    """Will generate a list for dates only
    Args:
        param_dict(dict): gets all the key from the request arguments
    Returns:
        (dict): contains startDate, endDate, both or none
    """

    parameter_keys = ('startDate', 'endDate')
    datetime_dict ={}
    for param_key, param_value in param_dict.items():
        if param_key in parameter_keys:
            datetime_dict[param_key] = param_value

    return datetime_dict
