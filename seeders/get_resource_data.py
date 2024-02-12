# Model
from api.models import Resource, Role


def get_resource_data():
    """Return the resource access level data.

    Returns:
        (List): List of dictionary containing role name,id, and resource id, name
    """

    resources = Resource.query_().all()

    titles = [
        'Activo Developer', 'Director of Operations', 'Operations Associate',
        'Operations Coordinator', 'Operations Manager', 'Regular User',
        'Office Assistant', 'Operations Intern', 'Admin'
    ]

    roles = Role.query_().filter(Role.title.in_(titles)).all()

    data = []
    for role in roles:
        data.append([
            {
                'role_id':role.id,
                'resource_id': record.id,
                'role_name':role.title,
                'resource_name': record.name
            } for record in resources])

    return data
