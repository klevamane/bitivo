"""
Permissions helper function modules
"""
from sqlalchemy import text

# database
from api.models.database import db

# Constants
from ..constants import FULL_ACCESS, NO_ACCESS

# Utilities
from ..sql_queries import sql_queries


def check_user_permissions(token_id, resource_name, permission_type):
    """
    Method to check if user has permission on a given resource

    Args:
        token_id (str): user token id
        permission_type (str): permission type
        resource_name (str): resource name

    Returns:
        bool: True for success or False for failure
    """

    sql_query = sql_queries['check_user_permissions'].format(
        token_id, resource_name, NO_ACCESS, FULL_ACCESS, permission_type)

    # execute the query and get back sqlalchemy result proxy object
    result_proxy = db.engine.execute(text(sql_query))

    # cast result proxy to a list of records
    records = list(result_proxy)
    # True if records is not empty otherwise False and user has no permission
    return True if records else False
