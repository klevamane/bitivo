"""
This module contains request type collection definitions for use by swagger UI
"""

from ..collections import api


request_type_namespace = api.namespace(
    'request type',
    description='A collection of request type related endpoints',
    path='/request-types'
)
