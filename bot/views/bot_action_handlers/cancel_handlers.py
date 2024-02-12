"""Module to handle bot cancel handlers"""

from main import cache

from api.utilities.helpers.env_resource_adapter import adapt_resource_to_env
from bot.tasks.slack_bot import BotTasks
from bot.utilities.constants import (
    CANCEL_HOTDESK_TITLE, CANCEL_HOTDESK, CANCEL_MSG, NO_CANCEL_REASON,
    PREDEFINED_CANCEL_REASONS)
from ...utilities.slack.slack_helper import SlackHelper
from ..slack_bot import SlackBotResource
from ...attachments.elements.reasons import cancel_reason_options, other_reason_text

slack_helper = SlackHelper()


class CancelHandlers:
    """Handle everything related to canceling hot desks"""

    @staticmethod
    def cancel_hot_desk_handler(action_dict):
        """Method that calls the cancel hot desk
        Args:
            action_dict (dict): dictionary containing action details.
        Returns:
            (text): message to return to the user
        """
        reason = action_dict['submission']['cancelled_reason'].strip()

        email = action_dict['actions'][0]['value']

        user_name = action_dict['user']['name']

        adapt_resource_to_env(BotTasks.cancel_hot_desk.send(email, reason))

        adapt_resource_to_env(BotTasks.notify_user_after_hotdesk_cancellation.send(user_name, email))

    @classmethod
    def cancel_hot_desk_reason(cls, **kwargs):
        """Method that handles the cancel hot desk message menu
        **kwargs
                result(dict): message menu payload
        Returns: (dict): cancelled message
        """
        result = kwargs['result']
        if(result['actions'][0]['selected_options'][0]['value'] == 'others'):
            title = CANCEL_HOTDESK_TITLE
            event_type = CANCEL_HOTDESK
            slack_helper.open_dialog(result['trigger_id'], title, event_type, element=other_reason_text)
        else:
            reason = result['actions'][0]['selected_options'][0]['value']
            cache.set('reason', reason, timeout=50)
            return cancel_reason_options(reason)

        return {'text': CANCEL_MSG}

    @classmethod
    def cancel_hot_desk_button_handler(cls, **kwargs):
        """Method that calls the cancel hot desk request method
        Args:
            cls (instance): class instance
            result (dict): dictionary containing action details.
        Returns:
            function call
        """
        result = kwargs['result']
        bot_task = SlackBotResource()
        return bot_task.cancel_hot_desk(result['user']['name'],
                                        result['user']['id'],
                                        result['channel']['id'])

    @classmethod
    def submit_cancel_hot_desk_reason(cls, **kwargs):
        """Method that handles the cancel hot desk selected options
        **kwargs
                result(dict): message menu payload
        Returns: (dict): cancelled message to the user
        """
        action_dict = cache.get('result')
        reason = cache.get('reason')
        user_name = action_dict['user']['name']
        if reason not in PREDEFINED_CANCEL_REASONS:
            return {'text': NO_CANCEL_REASON}
        action_dict['submission'] = {'cancelled_reason': reason}
        CancelHandlers.cancel_hot_desk_handler(action_dict)
        return {'text': CANCEL_MSG}
