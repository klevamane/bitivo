# Models
from api.models import Request, RequestType, User

# Helpers
from ..error import raise_error

# Enum
from api.utilities.enums import RequestStatusEnum

# Error
from ..error import raise_error_helper
from api.utilities.error import raises

# Messages
from ..messages.error_messages import request_errors, serialization_errors


def check_requester_id_exists(requester_id):
    """Checks whether a requester exists and whether the id is valid

    Args:
        requester_id (str): The id of the requester

    Raises:
        ValidationError: If requester_id is invalid or requester does not
            exist
    """
    user = User.exists(requester_id, 'token_id')
    if not user:
        raise_error('requester_not_found')


def validate_requester_and_request_type_as_member_of_center(data):
    """Checks if a user or requestype belongs to the specified center

    Args:
        data (dict): The request object

    Raises:
        ValidationError: If a requester or request type does not belong to the specified center

    """
    requester_id = data.get('requester_id')
    request_type_id = data.get('request_type_id')
    center_id = data.get('center_id')
    user = User.query_().filter_by(
        token_id=requester_id, center_id=center_id).first()
    request_type = RequestType.query_().filter_by(
        id=request_type_id, center_id=center_id).first()
    if not user:
        raise_error(
            'requester_not_found_in_center',
            'requesterId',
            fields='requesterId')
    if not request_type:
        raise_error(
            'request_type_not_found_in_center',
            'requesterTypeId',
            fields='requestType')


def validate_requester_is_not_responder(data):
    """Checks that a requester is not a responder

    Args
        data (dict): The request object

    Raises:
        ValidationError: If a requester is also a responder
    """
    requester_id = data.get('requester_id')
    request_type = data.get('request_type_id')
    center_id = data.get('center_id')
    requester_is_responder = RequestType.query_().filter_by(
        id=request_type, center_id=center_id,
        assignee_id=requester_id).first()
    if requester_is_responder:
        raise_error(
            'requester_cannot_be_responder',
            'requesterId',
            fields='requesterId')


def request_id_exists(request_id):
    """ Checks whether a request exists
     Args:
        request_id (str): The id of the request

    Raises:
        ValidationError: request does not exist

    """
    if not Request.exists(request_id, 'id'):
        raise_error('not_found', 'Request')


def validate_user_availability(assignee_id, request, user_placeholder):
    """Validates the availability of a user

    This method validates if the user is a valid user and also checks if the user
    exists in the center of the request

    Args:
        assignee_id (string): The id of the user
        request (dict): The current request
        user_placeholder (string): This the the placeholder of the value to be placed on
        the error message

    Raises:
        ValidationError: If the user does not exist, or the user is not found
        in the request center
    """
    user_exists = User.exists(assignee_id, 'token_id')
    if not user_exists:
        raise_error_helper(True, serialization_errors, 'generic_not_found',
                           user_placeholder)
    validate_user_exist_in_a_center(assignee_id, request.center_id)


def validate_cannot_close_request(status, update_data):
    """Ensures that a responder cannot close a request

    A request responder should be unable to close a request,
    this function handles the rejection of a responder
    trying to close a request

    Args:
        status (string): The request status
        update_data (string): The data to update the request

    Raises:
        ValidationError: When a responder is tying to close a request
    """
    if update_data.get('status') == RequestStatusEnum.closed:
        raise_error_helper(True, request_errors, 'cannot_close_request',
                           status)


def validate_user_exist_in_a_center(user_token_id, center_id):
    """Validates if a user belong to the specified center

    Args:
        user_token_id (string): The user token id
        center_id (string): The center id

    Raises:
        ValidationError: If a user does not belong to the specified center
    """

    user = User.query_().filter_by(
        token_id=user_token_id, center_id=center_id).first()
    if not user:
        raise_error_helper(True, serialization_errors, 'user_not_found',
                           'Assignee')



def sanitize_requester_data_for_open_status(update_data):
    """Handles scenarios for a user updating unauthorized fields on their request,
    i.e, ['status', 'assignee_id', 'center_id']

    Args:
        update_data (dict): The request data to be updated

    Returns:
        update_date (dict) : The request data to be updated
    """

    status = 'status' in update_data
    assignee_id = 'assignee_id' in update_data
    center_id = 'center_id' in update_data

    fields_mapper = {
        '0': 'status',
        '1': 'assignee',
        '2': 'center Id'
    }

    names = sanitize_helper(status, assignee_id, center_id, fields_mapper)

    if len(names) == 1:
        validate_single_field(status, assignee_id, center_id)
    elif len(names) == 2:
        raises('requester_two_fields', 403, names[0], names[1])
    elif len(names) == 3:
        raises('requester_three_fields', 403, names[0], names[1], names[2])
    else:
        return update_data

def sanitize_helper(status, assignee_id, center_id, fields_mapper):
    """Returns names of unauthorized feilds mapped from their indexes

    Args:
        status (bool): True if status field in in update data
        assignee_id(bool): True if assignee_id field in in update data
        center_id(bool): True if center_id field in in update data
        mapper(dict): Dictionary to help map indexs to feild names

    Returns:
        names(list) : List of mapped field names
    """

    checks = [status, assignee_id, center_id]
    fields = []

    for index, item in list(enumerate(checks)):
        fields.append(index) if item else None

    names = list(map(lambda item: fields_mapper[str(item)], fields))

    return names

def validate_single_field(status, assignee_id, center_id):
    """Raises a validation error in case a requester tries to update,
    an of the fields in ['satutus', 'assignee_id', 'center_id'] on
    request.

    Args:
        status (bool): True if status feild in in update data
        assignee_id(bool): True if assignee_id field in in update data
        center_id(bool): True if center_id field in in update data

    Returns:
        Validation Error (error): Error message with status code 403
    """
    if status:
        raises('request_status_update', 403, 'status')
    elif assignee_id:
        raises('request_assignee_update', 403, 'assignee')
    elif center_id:
        raises('request_center_update', 403, 'center Id')


def remove_whitespaces(data):
    """Validates that a field does not have white spaces

    Args:
        data: The data to be validated

    Returns:
        The data that has been validated
    """
    if data.get('description'):
        data['description'] = " ".join(data.get('description').split())

    if data.get('subject'):
        data['subject'] = " ".join(data['subject'].split())

    return data
