"""Module to seed resource access level table"""

# Models
from api.models import Resource, ResourceAccessLevel, Role, Permission
from api.models.database import db

# Utilities
from api.utilities.helpers.seeders import clean_seed_data

# Resource access level mapper
from .resource_access_level_mapper import resource_access_level_mapper

# Seed data
from .seed_data import get_env_based_data


def abstract_resource_access_level_data(data, mapper):
    """abstract the resource access level list to be seeded

    Args:
        data (list): List of dictionary of resources and roles
        mapper (dict) : Dictionary of resource, role and permission mapper
    """
    access_levels_list = []
    for res in data:
        permission_resources = mapper.get(res['role_name'])
        permission_access = permission_resources.get(res['resource_name'])
        if permission_access:
            permission = Permission.query_().filter_by(
                type=permission_access).first()
            access_levels_list.append(
                ResourceAccessLevel(
                    role_id=res['role_id'],
                    resource_id=res['resource_id'],
                    permissions=[permission]))
    return access_levels_list


def seed_resource_access_levels(clean_data=False):
    """Seeds sample resource access levels for all the roles

    Args:
        clean_data (bool): Determines if seed data is to be cleaned.
    """

    access_levels_data = get_env_based_data('resource_access_level')

    if not clean_data:
        access_levels_data = clean_seed_data('resource_access_level',
                                             access_levels_data, True)

    access_levels_list = []
    for data in access_levels_data:
        access_levels_list.extend(
            abstract_resource_access_level_data(data,
                                                resource_access_level_mapper))

    db.session.add_all(access_levels_list)
    db.session.commit()
