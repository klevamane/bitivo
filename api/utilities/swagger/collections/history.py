"""
This module contains history collection definitions for use by swagger UI
"""

from ..collections import api

history_namespace = api.namespace(
    'history',
    description='A collection of history related endpoints'
)
