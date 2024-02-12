"""
This module contains global search collection definitions for use by swagger UI
"""

from ..collections import api

global_search_namespace = api.namespace(
    'global search',
    description='A collection of global search related endpoints',
    path='/search'
)
