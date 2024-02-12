import json
from .error import raises


def json_dump_or_load_data(data, parse_type):
    """JSON dump a list of dictionaries

    Args:
        data (list of dictionaries): the list of dictionaries to be
        json dumped
        parse_type (string): one of either 'dumps' or 'loads'

    Returns:
        dumped_data: a list of json dumped objects
    """
    return [
        json.dumps(item) if parse_type == 'dumps' else json.loads(item)
        for item in data
    ]


def json_parse_objects(data=[], parse_type='dumps'):
    """
    checks type of recieved data if its a list
    and returns the value of json_dump_or_load_data method

    Args:
        data (list of dictionaries): the list of dictionaries to be
        json dumped
        parse_type (string): one of either 'dumps' or 'loads'
    """
    if isinstance(data, list):
        return json_dump_or_load_data(data, parse_type)
    # raise error if data provided is not of type list
    raises('invalid_data_type', 400)


def json_parse_request_data(request_data):
    if request_data.get('attachments'):
        request_data['attachments'] = json_parse_objects(
            request_data.get('attachments', []))
