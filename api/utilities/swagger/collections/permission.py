"""
This module contains permission collection definitions for use by swagger UI
"""

from ..collections import api

permission_namespace = api.namespace(
    'permissions',
    description='A collection of permissions related endpoints'
)
