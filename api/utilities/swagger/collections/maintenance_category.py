"""
This module contains maintenance category collection definitions for use by swagger UI
"""

from ..collections import api


maintenance_category_namespace = api.namespace(
    'maintenance category',
    description='A collection of maintenance category related endpoints',
    path='/maintenance-categories'
)
