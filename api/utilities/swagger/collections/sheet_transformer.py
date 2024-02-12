"""
This module contains request collection definitions for use by swagger UI
"""

from ..collections import api


sheet_transform_namespace = api.namespace(
    'sheets transformation',
    description='A collection of sheets transforms',
    path='/sheets'
)
