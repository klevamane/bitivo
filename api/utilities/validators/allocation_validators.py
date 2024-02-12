# models
from ...models import User, Space, Asset
from ...models.asset import AssigneeType

# helpers
from ..error import raise_error

# validators
from .validate_id import is_valid_id
from .space_exists_in_center_validator import check_space_exists


def check_target_id(model, id_, invalid_error=None, non_existing_error=None):
    """Checks whether the id is valid and exists
    Args:
        model (str): The target model
        id_ (str): The id of the user/space
        error_key (str): The error message key
    Raises:
        ValidationError: If is invalid or id does not exist
    """
    if not is_valid_id(id_):
        raise_error(invalid_error)
    if not model.exists(id_) and not User.exists(id_, 'token_id'):
        raise_error(non_existing_error)


def validate_assignee_id(assignee_id):
    """Checks whether an assignee exists and whether the id is valid
    Args:
        assignee_id (str): The id of the assignee
    Returns:
        None
    """
    check_target_id(Space, assignee_id,
                    'invalid_assignee_id',
                    'assignee_not_found')


def validate_assignee_type(assignee_type):
    """Validator for checking whether an assignee type is valid
    Args:
        assignee_type (str): The type of the assignee
    Raises:
        ValidationError: If the assignee type has an invalid value
    """
    allowed_types = {AssigneeType.space.value, AssigneeType.user.value}
    if assignee_type.lower() not in allowed_types:
        raise_error('invalid_assignee_type', assignee_type)


def validate_id_matches_type(data):
    """Checks whether the assignee matches the assignee type provided
    Args:
        data (dict): The deserialized request data
    Raises:
        Validation error: If the assignee id and type do not match
    """
    assignee_id = data.get('assignee_id')
    assignee_type = data.get('assignee_type', '').lower()
    assignee_types = {'user': User, 'space': Space}
    if assignee_id and assignee_type:
        assignee = assignee_types[assignee_type].get(assignee_id)
        if not isinstance(assignee, assignee_types.get(assignee_type)):
            raise_error('non_matching_assignee_type', fields=['assigneeType'])


def validate_id_and_type_both_present(data):
    """Validates that the assignee and assignee type are both present
    Checks if one of either assigneeId or assigneeType is in the data.
    If it is, it makes sure both are present.
    (useful for the PATCH request where not all fields are required)
    Args:
        data (dict): Dictionary containing the request data
    Raises:
        ValidationError: If both assignee id and type are not present
    """
    fields = ('assigneeId' in data, 'assigneeType' in data)
    if any(fields) and not all(fields):
        missing = 'assigneeType' if fields[0] else 'assigneeId'
        raise_error('assignee_id_and_type_required', fields=[missing])


def validate_space_in_center(data):
    """Checks whether the assignee space is in the center provided
    Args:
        data (dict): The deserialized request data
    Raises:
        ValidationError: If the space is not in the center
    """
    assignee_id = data.get('assignee_id')
    assignee_type = data.get('assignee_type')
    if assignee_id and assignee_type == AssigneeType.space.value:
        # if the center_id is present in the request we use that to verify,
        # else we use the current center_id of the asset
        center_id = data.get('center_id')
        if not center_id and 'asset_id' in data:
            center_id = Asset.get(data.get('asset_id')).center_id
        if center_id:
            check_space_exists(assignee_id, center_id)


def check_user_token_id(id, invalid_error, not_found_error):
    """
    This function checks if a user token id exists
    Args:
        id (str): The id to be validated
        invalid_error (str): The error message index for invalid data
        not_found_error (str): The error message index for not found data
    """
    if not is_valid_id(id):
        raise_error(invalid_error)
    if not User.exists(id, 'token_id'):
        raise_error(not_found_error)

def validate_requester_id(requester_id):
    """
    Checks whether a hotdesk requester is valid and id exists
    """
    check_user_token_id(requester_id, 'invalid_requester_id', 'requester_not_found')

def validate_complainant_id(complainant_id):
    """ 
    This function checks the validity of the complainant id
     Args:
        complainant_id (str): complainant id
     Returns:
        None
     """
    check_user_token_id(complainant_id, 'invalid_complainant_id', 'complainant_not_found')
