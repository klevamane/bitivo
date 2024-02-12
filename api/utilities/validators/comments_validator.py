# models
from ...models import Request, Schedule

# enums
from ...utilities.enums import ParentType

# errors
from ...utilities.error import raises


def check_parent_type_value_exists(data):
    """Checks whether the existing parent type matches the parent type provided

    Args:
        data (dict): The deserialized request data

    Raises:
        Validation error: If the existing parent types do not match the provided parent type
    """
    parent_type = data.get('parentType', None)
    if parent_type and parent_type not in ParentType.get_all():
        raises('invalid_choice', 400, 'parentType', ['Request', 'Schedule'])


def validate_parent_id_matches_parent_type(data):
    """Checks whether the parent id matches the parent type provided

    Args:
        data (dict): The deserialized request data

    Raises:
        Validation error: If the parent id and parent type do not match
    """
    parent_id = data.get('parentId', None)
    parent_type = data.get('parentType', None)
    parent_model = Request if parent_type == 'Request' or parent_type == None else Schedule
    if parent_id:
        model_data = parent_model.get_or_404(parent_id)
