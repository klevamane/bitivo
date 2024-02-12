from datetime import datetime as dt

from api.utilities.constants import REQUEST_FIELDS
from ..enums import RequestStatusEnum
from ..messages.error_messages import request_errors, serialization_errors
from ..error import raise_error_helper
from ...models import RequestType

from ..validators.request_validators import validate_cannot_close_request, \
    validate_user_availability, sanitize_requester_data_for_open_status


def responder_update(*args):
    """Function to handle request by a responder

     Args:
        args (*): variable number of arguments

     Returns:
        dict: status and updated date time
    """
    update_data, request = args
    status = request.status.value
    assignee_id = update_data.get('assignee_id')

    if update_data.get('status') is None and update_data.get(
            'assignee_id') is None:
        raise_error_helper(True, serialization_errors, 'missing_input_field',
                           'Status')

    is_not_open = status != RequestStatusEnum.open.value and \
        status != RequestStatusEnum.in_progress.value
    raise_error_helper(is_not_open, request_errors, 'cannot_update', status)
    if status == RequestStatusEnum.open.value:
        return_value = dict(status=status)
        update_return_value_if_assigneid_is_passed(assignee_id, request,
                                                   return_value)
        new_status = update_data.get('status')
        validate_cannot_close_request(status, update_data)

        # validate responder input if a new status is passed
        update_return_value_if_new_status_is_passed(
            new_status, return_value, status, request.assignee_id)
        return return_value

    validate_cannot_close_request(status, update_data)
    status_update_data = update_data.get('status')

    if status_update_data == RequestStatusEnum.open and request.status != RequestStatusEnum.open:
        raise_error_helper(True, request_errors, 'cannot_change', status,
                           RequestStatusEnum.open.value)

    # returns the updated status and the date time as the current time
    if status_update_data:
        return {
            "status": status_update_data,
            status_update_data.value + '_at': dt.now()
        }
    validate_user_if_assignee_is_passed(assignee_id, request)
    return {"assignee_id": update_data.get('assignee_id')}


def requester_update(*args):
    """Function to handle request update by a requester

         Args:
            args (*): variable number of arguments

         Returns:
            dict: The update request data
    """

    update_data, request = args
    status = request.status.value

    if status != RequestStatusEnum.open.value and status != RequestStatusEnum.completed.value:
        raise_error_helper(True, request_errors, 'requester_no_update', status)
    if status == RequestStatusEnum.completed.value:
        new_status = update_data.get('status')
        status_is_none = new_status is None
        raise_error_helper(status_is_none, request_errors, 'missing_status',
                           status)
        status_not_close = new_status != RequestStatusEnum.closed
        raise_error_helper(status_not_close, request_errors,
                           'close_completed_request', status)
        return {"status": new_status, 'closed_at': dt.now()}

    if status == RequestStatusEnum.open.value:
        update_data = sanitize_requester_data_for_open_status(update_data)
        validate_request_type_center(request, update_data)

    for key in update_data.keys():
        verify_accessible_field(key, REQUEST_FIELDS)

    return update_data


def verify_accessible_field(key, data):
    """Verify if field can be accessible

        Args:
           data (List): The list of request fields
           key (String): a request field
        """
    if key not in data:
        edited_key = key.replace("_", " ")
        raise_error_helper(True, request_errors,
                           "You cannot update inaccessible field",
                           edited_key)


def validate_request_type_center(request, update_data):
    """Validates the request type center id

       Args:
           request (dict): The request object
           update_data (obj): The data to be update an existing request
       """
    if update_data.get('request_type_id') is not None:
        request_type_id = update_data.get('request_type_id')
        request_type = RequestType.get(request_type_id)
        check_if_request_center_matches_request_type_center(
            request, request_type)


def check_if_request_center_matches_request_type_center(request, request_type):
    """Check if the request center and the request type center is the same

    Args:
        request (dict): The request object
        request_type (obj): the request type object

    Raises:
         ValidationError: if the request center is not the same as the request type center id
    """
    if request.center_id != request_type.center_id:
        raise_error_helper(True, request_errors,
                           'request_update_request_type_center_mismatch')


def user_update_data(current_user_id, requester_id):
    """Function to map user request action

     Args:
        current_user_id (str): The Id of the currently logged in user
        requester_id (str): The Id of the user that made the request

     Returns:
        dict: The user type action to be implemented
    """
    if current_user_id == requester_id:
        return requester_update
    else:
        return responder_update


def update_return_value_if_new_status_is_passed(new_status, return_value,
                                                status, request_assignee_id):
    """Adds and update as status key to the dictionary passed.
     This function adds a status key to the dictionary passed and updates the
     status value with the status argument passed.
     It first validates that the new status passed is "in progress". if so,
     it checks if the request already has an assignee, or if an assignee id
     was passed the in request body, if these conditions fails, an exception
     is raised, else the function updates the request status to "in progress"
      and updates the "inProgressAt" date-time field

     Args:
         new_status (str): The new status
         return_value (dict): The request update data
         status (str): The current request status before update
         request_assignee_id: The existing assignee id of the request to be
          updated

     Returns:
         dict : It returns a dictionary with the updated status and the
         respective date-time
     """

    if new_status:
        is_not_in_progress = new_status != RequestStatusEnum.in_progress
        raise_error_helper(is_not_in_progress, request_errors, 'cannot_change',
                           status, new_status.value)

        return_value.update(
            dict(
                status=RequestStatusEnum.in_progress, in_progress_at=dt.now()))


def update_return_value_if_assigneid_is_passed(assignee_id, request,
                                               return_value):
    """Set the assignee Id with the input json field
     This function sets the request update data to the assignee_id field
     passed from the the request json input
     Args:
         assignee_id (str): The assignee token_id
         request (dict): The current request
         return_value (dict): The request update data
     Returns:
         dict : It returns a dictionary with the updated assignee Id
     """
    if assignee_id:
        validate_user_availability(assignee_id, request, 'Assignee')
        return_value['assignee_id'] = assignee_id


def validate_user_if_assignee_is_passed(assignee_id, request):
    if assignee_id:
        validate_user_availability(assignee_id, request, 'Assignee')
