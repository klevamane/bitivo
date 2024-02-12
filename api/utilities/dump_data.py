"""Module that dumps data"""

def dump_data(*args):
    """Dumps data
    Args:
        schema(object): model schema
        query_obj(object): query object
        deleted(str): value of the request args

    Returns: Response data 
    """
    schema, query_obj, deleted, arg = args
    data = schema.dump(query_obj, request_args=arg).data \
        if deleted == 'deleted' else schema.dump(query_obj).data
    return data
