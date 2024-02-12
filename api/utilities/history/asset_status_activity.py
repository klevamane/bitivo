from flask import request

# Utilities
from api.utilities.enums import AssetStatus


def asset_status_activity_on_repair_log(asset_id, prev_status, session):
    """
    Record the activity on the asset status to the history
    table

    Args:
        asset_id(String):  The asset id
        prev_status(String): Status of the asset before update
        session(Object): The current database session
        
    Returns:
        None
    """

    if prev_status != AssetStatus.IN_REPAIRS.value:
        actor = request.decoded_token['UserInfo']
        from api.models import History
        msg = f"status changed from {prev_status} to {AssetStatus.IN_REPAIRS.value} by {actor['name']}"
        data = {
            "resource_id": asset_id,
            "resource_type": 'Asset',
            "actor_id": actor['id'],
            "action": 'edit',
            "activity": msg
        }
        history = History(**data)
        session.add(history)
