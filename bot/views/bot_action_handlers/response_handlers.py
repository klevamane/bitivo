"""Module to handle bot response handlers"""

from api.models import HotDeskRequest, User
from api.schemas.hot_desk import HotDeskRequestSchema
from api.utilities.enums import HotDeskRequestStatusEnum
from api.utilities.helpers.env_resource_adapter import adapt_resource_to_env
from bot.attachments.buttons.common.menu import approval_buttons
from bot.tasks.slack_bot import BotTasks
from bot.utilities.bugsnag import post_bugsnag_exception
from bot.utilities.constants import REJECT
from bot.utilities.helpers.bot_helpers import store_approval_response, remove_approval_response
from bot.views.bot_action_handlers.notification_handlers import NotificationHandlers
from config import AppConfig
from ...utilities.slack.slack_helper import SlackHelper

slack_helper = SlackHelper()


class ResponseHandlers:
    """Handles everything related to a hot desk response"""

    @staticmethod
    def approval_menus(assignee_email="", requester_email="", hot_desk_ref_no="", hot_desk_id=""):
        """Returns a successful message to slack user.
        Args:
            assignee_email(): the email of the assignee
            requester_email(): the email of the requester
            hot_desk_ref_no(): ref number of the hot desk
            hot_desk_id(): the id of the hot desk
        Returns:
            (str): Message sent successfully.
        """
        user = slack_helper.get_user_by_email(requester_email)["name"]

        response = slack_helper.post_message_to_user(
            f"@{user} has just booked *hot desk - {hot_desk_ref_no}*",
            approval_buttons, assignee_email)
        store_approval_response(hot_desk_id, response)

        rep2 = AppConfig.HOT_DESK_ASSIGNEE2
        countdown = int(AppConfig.BOT_COUNTDOWN)
        adapt_resource_to_env(
            BotTasks.send_notification_to_ops_rep2.send_with_options(
                args=(hot_desk_ref_no, rep2, user, response), delay=countdown))

    @staticmethod
    def reject_hotdesk_handler(action_dict):
        """Method that calls the reject hot desk class method
        Args:
        action_dict (dict): dictionary containing action details.
        Returns:
            (dict): message
        """
        actions = action_dict.get('actions', None)

        if actions and actions[0]['name'] == 'reject':
            hot_desk_ref_no = ' '.join(
                action_dict['original_message']['text'].split()[-2:])[-7:-1]
            requester = action_dict['original_message']['text'].split()[0]

            adapt_resource_to_env(
                BotTasks.reject_hotdesk_request.send(action_dict,
                                                     hot_desk_ref_no))
            return {
                'text':
                f'Request by {requester} for *hot desk - {hot_desk_ref_no}* Declined! :disappointed:'
            }
    
    @classmethod
    def dialog(cls, **kwargs):
        """Method that shows a dialog when the reject button is clicked
        Args:
            **kwargs
                result(dict): dialog submission payload
        Returns: (dict): rejection message
        """
        result = kwargs['result']

        if result['actions'][0]['name'] == 'reject':
            title = 'Reason for rejecting'
            event_type = REJECT
            slack_helper.open_dialog(result['trigger_id'], title, event_type)
            hot_desk_ref_no = ' '.join(
                result['original_message']['text'].split()[-2:])[-7:-1]
            requester = result['original_message']['text'].split()[0]

        return {
            'text':
            f'Request by {requester} for *hot desk - {hot_desk_ref_no}* Declined! :disappointed:'
        }

    @staticmethod
    def handle_hotdesk_request(result, hot_desk_ref_no):
        """Instance method which handles approve and reject actions
        Args:
            result (dict): Parameter containing data to handle user's request
            hot_desk_ref_no (str): the hot desk ref number of the hot desk requested
        Returns:
            (str): data of the hot desk
        """
        hot_desk_request_schema = HotDeskRequestSchema()

        assignee_action = result['actions'][0]['value']
        reason = ''
        if result.get('submission'):
            reason = result['submission']['reason']
        try:

            hot_desk_object = HotDeskRequest.query_().filter_by(
                hot_desk_ref_no=hot_desk_ref_no).first()

            if hot_desk_object.status.value == HotDeskRequestStatusEnum.pending.value:

                hot_desk_request_data = hot_desk_request_schema.load_object_into_schema(
                    dict(status=assignee_action, reason=reason), partial=True)

                hot_desk_object.update_(**hot_desk_request_data)

                requester_email = User.get(hot_desk_object.requester_id).email
                requester = slack_helper.get_user_by_email(requester_email)
                requester_name = requester.get('name')
                NotificationHandlers.slack_dm(requester_name, requester_email,
                                           hot_desk_ref_no, assignee_action,
                                           reason)
                remove_approval_response(hot_desk_object.id)
                return hot_desk_request_schema.dump(hot_desk_object).data

        except Exception as e:
            post_bugsnag_exception(e, 'We could not handle this request')
