""" mock history data """
from .user import user_one

user_one_id = user_one.id

histories = [
    {
        "resource_id": "-LPUuJEW8lBVV_R1CsQw",
        "resource_type": "Asset",
        "actor_id": user_one_id,
        "action": "Delete",
        "activity": "Removed from Activo"
    },
    {
        "resource_id": "-LPUuJEW8lBVV_R1CsQw",
        "resource_type": "Asset",
        "actor_id": user_one_id,
        "action": "Edited",
        "activity": "changed custom attributes"
    },
    {
        "resource_id": "-LPUuJEW8lBVV_R1CsQw",
        "resource_type": "Asset",
        "actor_id": user_one_id,
        "action": "Edited",
        "activity": "changed tag from AND to XZY"
    },
    {
        "resource_id": "-LPUuJEW8lBVV_R1CsQw",
        "resource_type": "Asset",
        "actor_id": user_one_id,
        "action": "Add",
        "activity": "Added to Activo"
    },
]
