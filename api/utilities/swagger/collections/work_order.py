"""
This module contains user collection definitions for use by swagger UI
"""
from ..collections import api

work_order_namespace = api.namespace(
    'work orders',
    description='A collection of work order related endpoints',
    path='/work-orders')
