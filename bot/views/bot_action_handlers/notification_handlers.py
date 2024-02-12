"""Module to handle bot notification handlers"""

from api.models import HotDeskRequest, User
from api.schemas.hot_desk import HotDeskRequestSchema
from api.utilities.enums import HotDeskRequestStatusEnum
from api.utilities.helpers.env_resource_adapter import adapt_resource_to_env
from bot.attachments.buttons.common.menu import approval_buttons
from bot.tasks.slack_bot import BotTasks
from bot.utilities.helpers.bot_helpers import store_approval_response
from config import AppConfig
from ...utilities.slack.slack_helper import SlackHelper
from ...attachments.buttons.common.menu import cancel_request_button

slack_helper = SlackHelper()


class NotificationHandlers:
    """Handle everything related to bot notification"""

    @staticmethod
    def slack_dm(*args):
        """Sends messages to user in a workspace
        Args:
            *args
                requester_name(str): requester name
                requester_email(str): requester name
                hot_desk_ref_no(str): hot desk reference number
                assignee_action(str): assigness button action
                reason(str): reason for rejection
        """
        requester_name, requester_email, hot_desk_ref_no, assignee_action, reason = args

        attachments = ""
        message = f"Hey @{requester_name}, \n Your request for *hot desk - {hot_desk_ref_no}* has been {assignee_action}"
        message = message if assignee_action == 'approved' else message + \
            f". \n *Reason:* {reason}"
        attachments = cancel_request_button if assignee_action == 'approved' else attachments
        slack_helper.post_message_to_user(message, attachments,
                                          requester_email)

    @staticmethod
    def ops_slack_notifications(prev_response, func, *args):
        """Method to send notifications to responders on slack
        Args:
            rep (str): responder email
            user (str): requester name
            hotdesk (str): hot desk reference number
            func (method): Method that sends notification to responder on slack
        Returns:
            None
        """
        rep, user, hotdesk, nextrep = args
        hot_desk_object = HotDeskRequest.query_().filter_by(
            hot_desk_ref_no=hotdesk).first()

        hot_desk_request_schema = HotDeskRequestSchema()
        ts = prev_response["ts"]
        channel = prev_response["channel"]

        if hot_desk_object.status.value == 'pending':
            try:
                assignee_id = User.query_().filter_by(
                    email=rep).first().token_id

                hot_desk_request_data = hot_desk_request_schema.load_object_into_schema(
                    dict(assignee_id=assignee_id), partial=True)

                hot_desk_object.update_(**hot_desk_request_data)
                # Update the first notification the responder gets
                BotTasks.update_slack_ops_team(ts, channel, rep, user, hotdesk)

                response = slack_helper.post_message_to_user(
                    f"@{user} has just booked *hot desk - {hotdesk}*",
                    approval_buttons, rep)

                # Store the response in a cache
                store_approval_response(hot_desk_object.id, response)
                countdown = int(AppConfig.BOT_COUNTDOWN)
                adapt_resource_to_env(
                    func.send_with_options(
                        args=(hotdesk, nextrep, user, response),
                        delay=countdown))

            except Exception as e:
                raise e

    @staticmethod
    def requester_slack_notification(hotdesk):
        """Method to send notifications to requester's on slack
        Args:
            hotdesk (object): hot desk model object
        """
        if hotdesk.status == HotDeskRequestStatusEnum.pending:
            try:
                countdown = int(AppConfig.BOT_COUNTDOWN)
                adapt_resource_to_env(
                    BotTasks.notify_requester.send_with_options(
                        args=(hotdesk.hot_desk_ref_no, hotdesk.requester_id),
                        delay=countdown))

            except Exception as e:
                raise e
