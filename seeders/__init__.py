""" Module for seeding sample data into the database """

# Standard library
from collections import OrderedDict

# Third party
from sqlalchemy import text

# App config
from config import AppConfig

# Local Imports
from .seed_asset_category import seed_asset_category
from .seed_asset import seed_asset
from .seed_roles import seed_roles
from .seed_center import seed_center
from .seed_user import seed_user
from .seed_permissions import seed_permissions
from .seed_space_type import seed_space_type
from .seed_space import seed_space
from .seed_resource import seed_resources
from .seed_resource_access_levels import seed_resource_access_levels
from .seed_stock_count import seed_stock_count
from .seed_request_type import seed_request_type
from .seed_request import seed_request
from .seed_comment import seed_comments
from .seed_work_order import seed_work_order
from .seed_schedule import seed_schedule
from .seed_maintenance_category import seed_maintenance_category
from .seed_hot_desk_request import seed_hot_desk_request

# Database
from api.models.database import db


def seed_db(resource_name=None):
    """Checks the argument provided and matches it to the respective seeder

    Args:
        resource_name (str): Name of resource

    Return:
        func: calls a function with the resource name as arguments
    """

    resource_order_mapping = OrderedDict({
        'centers':
        seed_center,
        'asset_categories':
        seed_asset_category,
        'space_types':
        seed_space_type,
        'spaces':
        seed_space,
        'permissions':
        seed_permissions,
        'resources':
        seed_resources,
        'roles':
        seed_roles,
        'users':
        seed_user,
        'asset':
        seed_asset,
        'resource_access_levels':
        seed_resource_access_levels,
        'stock_counts':
        seed_stock_count,
        'request_types':
        seed_request_type,
        'requests':
        seed_request,
        'comments':
        seed_comments,
        'maintenance_category':
        seed_maintenance_category,
        'work_orders':
        seed_work_order,
        'schedules':
        seed_schedule,
        'hot_desk_requests':
        seed_hot_desk_request
    })

    # Determines whether data to be seeded will be cleaned or not
    # It's set to False since in development all data will be truncated
    # before seeding & hence no need for cleaning.
    clean_seed_data = False

    if resource_name:
        return resource_order_mapping.get(resource_name)()

    if AppConfig.FLASK_ENV in ('development', 'testing'):
        from subprocess import call
        call(["flask", "truncate"])
        clean_seed_data = True

    for _, resource in resource_order_mapping.items():
        resource(clean_seed_data)
