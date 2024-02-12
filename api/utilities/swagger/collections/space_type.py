"""
This module contains request collection definitions for use by swagger UI
"""

from ..collections import api

space_namespace = api.namespace(
    'spaces',
    description='A collection of spaces related endpoints',
    path='/spaces'
)
