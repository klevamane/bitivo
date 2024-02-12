"""
This module contains request collection definitions for use by swagger UI
"""

from ..collections import api

stock_count_namespace = api.namespace(
    'stock count',
    description='A collection of stock count endpoints',
    path='/stock-count'
)
