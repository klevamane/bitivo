"""
This module contains user collection definitions for use by swagger UI
"""
from ..collections import api

user_namespace = api.namespace(
    'users',
    description='A collection of user related endpoints',
    path='/people'
)
