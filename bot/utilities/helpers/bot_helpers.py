# Local imports
from main import cache
from sqlalchemy import or_

# Utilities
from bot.utilities.constants import (SOMETHING_WENT_WRONG,
                                     CENTERS, CENTER_CHILDREN, OPS_CANCEL_UPDATE)
from bot.utilities.slack.slack_helper import SlackHelper
from bot.utilities.provision_user import provision_user
from bot.utilities.slack.slack_helper import get_slack_hot_desk_users_list

# Models
from api.models import User


def store_centers(response):
    """Function to check if a user did /activo again for some reason in the
     the middle of requesting for hot desk.
     response(dict): what the list of buttons rendered on slack workspace as centers is.
     its basically what construct the menus you see when you do /activo on a workspace
    Returns: none

    """
    cache.set('navigation_list', [response])


def back_navigation_helper(output_dict, choice):
    """ A function to check what buttons were clicked and wether there is need to
    to store the result of the button click for later usage.
    button click for approve, reject,cancel etc does not require anything to be
    stored
    output_dict(dict): dict containing the current menu for the previous button click
    choice: the button clicked by a user
    Returns: none

    """
    not_none = output_dict.get(
        'attachments', False)  # incase the click on a button did not
    # go the next menu for some reason and a user need to click again
    choice_list = []
    choice_list.extend(CENTERS)
    choice_list.extend(CENTER_CHILDREN)
    navigation_list = cache.get('navigation_list')

    # we want to ensure that even if for some reason a user clicks a button but they are not moved
    # to the next menu, duplicate entries are not cached
    if choice in choice_list and output_dict not in navigation_list and not_none:
        navigation_list.append(output_dict)
        cache.set('navigation_list', navigation_list)

        # or f l o o r is meant to cater for the case there is a list of floor list to choose from
    elif 'f l o o r' in choice and output_dict not in navigation_list and not_none:
        navigation_list.append(output_dict)
        cache.set('navigation_list', navigation_list)


def render_previous_menus(*args, **kwargs):
    """ A function to return the appropriate menu based on what point the back button is clicked
    Returns: message or message attatchement

    """

    try:
        navigation_list = cache.get('navigation_list')
        size = len(navigation_list)
        if size in [2, 3, 4]:
            navigation_list.pop()
            cache.set('navigation_list', navigation_list)
            return_ = navigation_list[size-2]
        else:
            return_ = {'text': SOMETHING_WENT_WRONG}

    except (AttributeError, IndexError):
        return_ = {'text': SOMETHING_WENT_WRONG}
    finally:
        return return_

def process_dialog_error_data(error_data):
    """Process the dialog error message to display to the user
    Args:
        error_data(Dict): dictionary with field name as key
        and error data as value
        Returns
            Dictionary of all the errors
    """
    data = {'errors': []}
    for field_name, error_value in error_data.items():
        current_error = {
            'name': field_name,
            'error': error_value
        }
        data['errors'].append(current_error)
    return data

def store_approval_response(hot_desk_id, response):
    """ A function that store the approval response for an hotdesk
    Args:
        hot_desk_id (str): id of the hotdesk
        response (str): the reason for cancelling hot desk
    Returns:
        cache: set the approval_responses cache
    """
    approval_responses = cache.get('approval_responses')
    if not approval_responses:
        approval_responses = {}
    approval_responses[hot_desk_id] = {
        'ts': response['ts'], 'channel': response['channel']}
    cache.set('approval_responses', approval_responses)


def update_approval_response_on_cancel(hot_desk):
    """ A function that gets the approval responses
    Args:
        hot_desk (str): the hotdesk that was requested
    Returns:
        slack: update the approval menu chat
    """
    slack_helper = SlackHelper()
    approval_responses = cache.get('approval_responses')
    hot_desk_id = hot_desk['id']
    hot_desk_approval_response = approval_responses[hot_desk_id]
    if hot_desk_approval_response:
        responder_name = hot_desk['approver']['name']
        hot_desk_ref_no = hot_desk['hotDeskRefNo']
        requester_name = hot_desk['requester']['name']
        time_stamp = hot_desk_approval_response["ts"]
        channel = hot_desk_approval_response["channel"]
        msg = OPS_CANCEL_UPDATE.format(
            responder_name, requester_name, hot_desk_ref_no)

        slack_helper.update_message_to_user(msg, time_stamp, channel)
        remove_approval_response(hot_desk_id)


def remove_approval_response(hot_desk_id):
    """ A function that removes a response data from the approval_responses
        cache
    Args:
        hot_desk_id (str): id of the hotdesk
    """
    approval_responses = cache.get('approval_responses')
    if approval_responses:
        del approval_responses[hot_desk_id]
        cache.set('approval_responses', approval_responses)


def get_requester_and_assignee(requester_email, assignee_email):
    """Method to get the requester and assignee data
    Args:
        requester_email(str): requester email
        assignee_email(str): assignee email
    Returns:
        requester (obj): requester object
        assignee (obj): assignee object"""
    users = User.query_().filter(
        or_(User.email == requester_email, User.email == assignee_email)).all()
    requester = get_requester_or_assignee(users, requester_email)
    assignee = get_requester_or_assignee(users, assignee_email)
    if not requester:
        requester = provision_user(requester_email)
    return requester, assignee


def get_requester_or_assignee(users, user_email):
    """Function to get requester or assignee data
    Args:
        users(obj): Users object from the db
        user_email(str): email of the user
    Returns:
        user (obj): assignee or requester object"""
    user_object = next((user for user in (user for user in users)
                        if user.email == user_email), None)
    return user_object


def get_ineligible_user_email(requester_email):
    """Method to check if a user email exists in the cached list if ineligible users
    Args:
        requester_email(str): requester email
    Returns:
        user_email (list): Ineligible user email"""

    users_email_list = cache.get('ineligible_user_list')
    if not users_email_list:
        users_email_list = check_if_user_email_is_in_google_sheet(
            requester_email)
    user_email = [
        user_email for user_email in users_email_list
        if user_email == requester_email]
    return user_email


def check_if_user_email_is_in_google_sheet(requester_email):
    """Method to check if a user email exists in the
        list if eligible users from the google sheet
    Args:
        requester_email(str): requester email
    Returns:
        user_email (list): Ineligible user email"""

    hotdesk_eligible_users = get_slack_hot_desk_users_list()
    user_email = [
        user_email.lower() for user_email in hotdesk_eligible_users
        if user_email.lower() == requester_email
    ]
    users_email = [] if not user_email else [user_email]
    return users_email
