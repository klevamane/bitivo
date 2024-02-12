# Helpers
from api.utilities.error import raises


def validate_query_param_values(request_args, query_values, query_key):
    query_param = request_args.to_dict()
    if query_param.get(query_key, None) and query_param[
            query_key] not in query_values:
        return raises(
            'invalid_query_wrong_value',
            400,
            query_key,
            query_param.get(query_key, None))
