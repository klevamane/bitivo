"""
This module contains schedule collection definitions for use by swagger UI
"""

from ..collections import api


schedule_namespace = api.namespace(
    'schedules',
    description='A collection of schedule related endpoints'
)
