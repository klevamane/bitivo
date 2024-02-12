"""Module to handle bot request handlers"""
# Utilities
from bot.utilities.user_hot_desk import get_pending_or_approved_hot_desk
from bot.utilities.slack.slack_helper import SlackHelper

from api.utilities.helpers.env_resource_adapter import adapt_resource_to_env
from bot.utilities.constants import (HOT_DESK,
                                     ASSIGNED_HOTDESK_MSG,
                                     PENDING_HOTDESK_MSG)
# Tasks
from bot.tasks.slack_bot import BotTasks
from bot.utilities.constants import HOT_DESK
from ...attachments.buttons.common.menu import cancel_request_button

slack_helper = SlackHelper()

class RequestHandlers:
    """Handles everything related to making a hot desk request"""

    @classmethod
    def request_hot_desk_handler(cls, **kwargs):
        """Method that calls the request hot desk class method
        Args:
            cls (instance): class instance
            result (dict): dictionary containing action details.
        Returns:
            (dict): message
        """
        result = kwargs['result']
        requester_email = slack_helper.user_info(
            result['user']['id'])['profile']['email']
        # Run as a background task
        adapt_resource_to_env(BotTasks.notify_hot_desk_ineligible_requester.send(
            requester_email, result['user']['name']))
        hot_desk_result = get_pending_or_approved_hot_desk(requester_email)
        if hot_desk_result:
            return {'text':
                    ASSIGNED_HOTDESK_MSG.format(
                        hot_desk_result['hotDeskRefNo'])
                    if hot_desk_result['status'] == 'approved'
                    else PENDING_HOTDESK_MSG.format(hot_desk_result['hotDeskRefNo'])}
        if result['actions'][0]['name'].upper() == HOT_DESK:
            request_hot_desk_task = adapt_resource_to_env(
                BotTasks.request_hot_desk.send)
            request_hot_desk_task(result)

        seat_no = result['actions'][0]['value']
        return {
            'text':
            f'Your request for *hot desk - {seat_no}* has been submitted :smiley:',
            'attachments':
            cancel_request_button
        }
