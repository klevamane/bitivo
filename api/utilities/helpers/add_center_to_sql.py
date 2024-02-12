from flask import request
from api.models import User


def add_center_to_query(query, model='assets'):
    """Append the center_id of the user to the query
    Args:
        query (str): SQL query string
    Returns:
        (str): SQL query with center_id if user is not a super_user
    """
    user = User.get(request.decoded_token['UserInfo']['id'])
    if not user.role.super_user:
        if model == 'assets':
            query = query.replace('AND asset.center_id IS NOT NULL',
                                  "AND asset.center_id ='{}'".format(user.center_id))
            
            query = query.replace('AND stock_counts.center_id IS NOT NULL',
                                  "AND stock_counts.center_id ='{}'".format(user.center_id))

        if model == 'requests':
            query = query.replace('r.center_id IS NOT NULL',
                                  "r.center_id ='{}'".format(user.center_id))
        return query
    return query
