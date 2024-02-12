"""Module for mocking resources"""
from flask import g
from unittest.mock import Mock
from config import AppConfig


def adapt_resource_to_env(resource):
    """Helper function to mock resources.

    Args:
        resource (object): The resource to be mocked depending on environment

    Returns:
        A dummy function if mocked else the resource

    """
    env = AppConfig.FLASK_ENV

    if env == 'testing' and not isinstance(resource, Mock):
        resource = lambda *args: args
    if 'seed' in g:
        resource = lambda *args: args
    return resource
