"""
slack helper module
"""
import requests

from slackclient import SlackClient

from ..bugsnag import post_bugsnag_exception
from main import cache

from ...attachments.elements.reasons import reject_reason

from config import AppConfig


def get_slack_hot_desk_floors():
    """Method which gets all hot desk floors
    Returns: list
    """
    return cache.get('slack_hot_desk_floors')


def get_slack_hot_desk_floors_with_cancel():
    """Method which gets all hot desk floors with cancel button included
    Returns: list
    """
    return cache.get('slack_hot_desk_floors_with_cancel')


def get_slack_hot_desk_list():
    """
    Method which gets list of hot desks
    Returns: list
    """
    return cache.get('slack_hot_desk_list')


def get_slack_hot_desk_users_list():
    """
    Method which gets list of hot desk eligible users
    Returns: list
    """
    return cache.get('hot_desk_users_list')


def get_slack_floors():
    """Method which gets all floors
    Returns: list
    """
    return cache.get('floors')


class SlackHelper:
    """
    slack helper class
    """

    def __init__(self):
        """
        constructor
        """
        self.slack_token = AppConfig.SLACK_BOT_TOKEN
        self.slack_client = SlackClient(self.slack_token)
        self.slack_user_token = AppConfig.SLACK_USER_TOKEN
        self.slack_test_url = AppConfig.SLACK_TEST_URL

    def is_alive(self):
        """Check if the slack api service is up
        Returns:
            (bool): True if the service works as expected else false
        """
        headers = {"Content-type": "application/json",
                   "Authorization": f"Bearer {self.slack_user_token}"}
        payload = {"test": "test"}
        response = requests.post(
            url=self.slack_test_url, params=payload, headers=headers)
            
        return True if response.status_code == 200 else False


    def post_message_to_channel(self, msg, attachments, user_id, channel_id):
        """Method to post messages to slack workspace.
         Args:
            attachments (list): slack ui objects
            msg (str)
         Returns: function call
        """
        try:
            return self.slack_client.api_call(
                "chat.postEphemeral",
                channel=channel_id,
                text=msg,
                user=user_id,
                username='activo_test_bot',
                parse='full',
                attachments=attachments,
                icon_emoji=':robot_face:',
                as_user=False)
        except Exception as e:
            post_bugsnag_exception(
                e, f'Could not post slack message - {msg} to {user_id}')

    def post_message_to_user(self, msg, attachments, email):
        """
        Sends a direct message to a user.
        Args:
        msg : Takes in the text to be sent to the user.
        attachments: Takes in any additional extention to the message to send to the user.
        email: Takes in the email of the user you want to send a direct message to.
        Returns:
            slack: Sends a direct slack message to user.
        """
        user = self.get_user_by_email(email)
        username = user.get('name', '') if user else ''

        try:
            return self.slack_client.api_call(
                "chat.postMessage",
                channel=f'@{username}',
                text=msg,
                username='activo',
                parse='full',
                attachments=attachments,
                icon_emoji=':building_construction:',
                as_user=True)
        except Exception as e:
            post_bugsnag_exception(
                e, f'Could not post message to user - {username}')

    def get_user_by_email(self, email):
        """
        Returns the name of the user with the email
        Args:
        email (str): takes up an email to use it for verification
        Returns:
        (str): username
        """
        try:
            response = self.slack_client.api_call(
                'users.lookupByEmail', email=email)
            return response['user']
        except Exception as e:
            post_bugsnag_exception(
                e, f'Could not retrieve info for user by email - {email}')

    def update_message_in_channel(self, msg, attachments, ts, channel_id):
        """
        Updates a message in a channel.
        Args:
        msg : Takes in the text to be sent to the user.
        attachments: Takes in any additional extention to the message.
        ts: Takes in the timestamp of the message to be updated.
        Returns:
            slack: Sends a direct slack message to user.
        """
        try:
            return self.slack_client.api_call(
                "chat.update",
                msg=msg,
                channel=channel_id,
                ts=ts,
                parse='full',
                as_user=True,
                attachments=attachments)
        except Exception as e:
            post_bugsnag_exception(
                e,
                f'Could not update slack with message - {msg} @ channel - {channel_id}'
            )

    def user_info(self, uid):
        """
        Returns user information
        Args:
            uid (str): takes up a user id to use it for verification
        Returns:
            user_info(dict): a dictionary containing user info
        """
        try:
            response = self.slack_client.api_call("users.info", user=uid)
            return response['user']
        except Exception as e:
            post_bugsnag_exception(
                e, f'Could not retrieve info for user - {uid}')

    def open_dialog(self, trigger_id, title, event_type, element=reject_reason):
        """Method that triggers a dialog
        Args:
            trigger_id (str): id that triggers the dialog
            title(str): The title of the dialog
            event_type(str): the event to be handled by the dialog
            element(List): List of the dict of objects to be displayed

        Returns: function call
        """
        try:
            return self.slack_client.api_call(
                "dialog.open",
                trigger_id=trigger_id,
                dialog={
                    "title":
                    title,
                    "submit_label":
                    "Submit",
                    "callback_id":
                    event_type,
                    "notify_on_cancel":
                    True,
                    "elements": element,
                })
        except Exception as e:
            post_bugsnag_exception(e,'Could not open slack dialog')

    def update_message_to_user(self, msg, ts, channel_id):
        """
        Updates a message to user
        Args:
        msg : Takes in the text to be sent to the user.
        attachments: Takes in any additional extention to the message.
        ts: Takes in the timestamp of the message to be updated.
        Returns:
            slack: Sends a direct slack message to user.
        """

        try:
            return self.slack_client.api_call(
                "chat.update",
                text=msg,
                channel=channel_id,
                ts=ts,
                parse='full',
                attachments="null",
                as_user=True)
        except Exception as e:
            post_bugsnag_exception(e, f'Could not update slack with message - {msg} @ channel - {username}')

