"""
This module contains request collection definitions for use by swagger UI
"""

from ..collections import api


request_namespace = api.namespace(
    'requests',
    description='A collection of request related endpoints',
    path='/requests'
)
