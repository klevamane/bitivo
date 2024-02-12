def check_prefix(key):
    """
    Depending on the prefix at the beginning of a key,
    a tuple of prefix, key and operator is returned

    Parameters:
        key (str): the key of the url query
    """
    # Check if there is an expected prefix
    query_mapper = {
        'report': ('', 'status', 'eq'),
        'requester': ('', 'requester_id', 'eq')
    }
    if key.startswith('start'):
        return ('start', key[5:], 'ge')
    elif key.startswith('end'):
        return ('end', key[3:], 'le')
    elif key in query_mapper:
        return query_mapper.get(key)
    else:
        return ('', key, '')
