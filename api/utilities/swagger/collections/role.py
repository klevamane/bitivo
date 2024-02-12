"""
This module contains role collection definitions for use by swagger UI
"""

from ..collections import api


role_namespace = api.namespace(
    'roles',
    description='A collection of role related endpoints',
    path='/roles'
)
