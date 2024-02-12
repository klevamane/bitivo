"""
A set of mock data for space
"""
VALID_SPACE_DATA = {
    "name": "epic tower",
    "parent_id": "xxx",
    "space_type_id": "yyy",
    "center_id": '1'
}


def create_space_data(
        name,
        centerId,
        spaceTypeId,
        parentId=None,
        id=None,
):
    data = {
        "name": name,
        "centerId": centerId,
        "spaceTypeId": spaceTypeId,
    }

    if parentId:
        data['parentId'] = parentId

    if id:
        data['id'] = id

    return data
