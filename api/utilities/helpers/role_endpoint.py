# Models
from ...models import ResourceAccessLevel, Permission


def update_resource_access_levels(role_id, resource_access_levels):
    """
    This function update the given permissions in the resource_access_levels of a role
    Args:
        role_id (str): The id of a given role
        resource_access_levels (list): list of permissions
    """
    permissions_mapper = {
        permission.id: permission
        for permission in Permission.query_().all()
    }
    for permission in resource_access_levels:
        resource_access_level = ResourceAccessLevel.query.filter_by(
            role_id=role_id, resource_id=permission['resource_id']).first()
        if not resource_access_level:
            resource_access_level = ResourceAccessLevel(
                role_id=role_id, resource_id=permission['resource_id'])
            resource_access_level.save()

        permissions = [
            permissions_mapper.get(permission_id)
            for permission_id in list(set(permission['permission_ids']))
        ]
        update_data = {'permissions': permissions}
        resource_access_level.update_(**update_data)
