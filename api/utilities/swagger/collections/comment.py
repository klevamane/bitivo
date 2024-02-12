"""
This module contains comment collection definitions for use by swagger UI
"""

from ..collections import api


comment_namespace = api.namespace(
    'comments',
    description='A collection of comment related endpoints'
)
