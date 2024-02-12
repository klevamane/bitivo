import json, requests
from requests.exceptions import HTTPError
from api.models import User
from ..utilities.constants import USER_NOT_FOUND
from ..utilities.slack.slack_helper import SlackHelper
from api.schemas.user import UserSchema
from bot.utilities.bugsnag import post_bugsnag_exception
from config import AppConfig


def provision_user(user_email):
    """Gets a user detail from the oauth service and stores it in the database
    Args:
        user_email (str): user email
    Returns:
        (dict): An object of the user saved in the database
    Raises:
        HTTPError: A HTTPError
    """
    slack_helper = SlackHelper()

    try:
        response = get_user_from_andela_auth_service(user_email)
        response.raise_for_status()
        data = response.json()
        values = data.get('values', [])
        user_details = values[0] if len(values) > 0 else None
        new_user_data = dict(
            token_id=user_details['id'],
            email=user_details['email'],
            name=f'{user_details["first_name"]} {user_details["last_name"]}',
            image_url=user_details['picture'])
        new_user = User(**new_user_data)
        new_user.save()
        return new_user

    except HTTPError as e:
        raise e
    except Exception as e:
        post_bugsnag_exception(
            e, f'Could not get details for user - {user_email}')
        slack_helper.post_message_to_user(USER_NOT_FOUND, None, user_email)

def get_user_from_andela_auth_service(user_email):
    """Gets a user detail from the oauth service
    Args:
        user_email (str): user email
    Returns:
        (obj): Response object from the oauth service
    """
    url = AppConfig.AUTH_URL
    token = AppConfig.USER_TOKEN
    bearer_token = '{0} {1}'.format('Bearer', token)
    payload = {'email': user_email}
    headers = {'Authorization': bearer_token}
    response = requests.get(url, params=payload, headers=headers)
    return response

def is_andela_auth_service_alive():
    """Check if the andela oauth service is up
    Returns:
        (bool): True if the service works as expected else false
    """
    response = get_user_from_andela_auth_service('test@andela.com')
    return True if response.status_code == 200 else False
