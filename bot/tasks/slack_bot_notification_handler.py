# Local imports
from main import dramatiq
from main import cache

# Enums
from api.utilities.enums import HotDeskRequestStatusEnum

# Models
from api.models import User, HotDeskRequest, HotDeskResponse

from config import AppConfig

# Utilities
from ..utilities.bugsnag import post_bugsnag_exception
from ..utilities.slack.slack_helper import SlackHelper, get_slack_hot_desk_users_list
from ..utilities.helpers.bot_helpers import (check_if_user_email_is_in_google_sheet)
from ..utilities.constants import PERMANENT_SEAT_MSG


slack_helper = SlackHelper()


class NotificationHandler:
    """Class that handles slack bot notification"""
    @staticmethod
    @dramatiq.actor
    def send_notification_to_ops_rep2(hotdesk, rep2, user, response):
        """Method to send the second responder both email and slack notifications
        Args:
            rep2 (str): second responder email
            user (str): requester name
            hotdesk (str): hot desk reference number

        """
        from ..views.bot_actions import ActionResource
        action_resource = ActionResource()

        rep3 = AppConfig.HOT_DESK_ASSIGNEE3

        try:
            action_resource.ops_slack_notifications(
                response, NotificationHandler.send_notification_to_ops_rep3, rep2, user,
                hotdesk, rep3)
        except Exception as e:
            post_bugsnag_exception(e, f'Could not notify ops rep 2 - {rep2}')

    @staticmethod
    @dramatiq.actor
    def send_notification_to_ops_rep3(hotdesk, rep3, user, response):
        """Method to send the third responder both email and slack notifications
        Args:
            rep3 (str): third responder email
            user (str): requester name
            hotdesk (str): hot desk reference number

        """
        from ..views.bot_actions import ActionResource
        action_resource = ActionResource()
        try:
            action_resource.ops_slack_notifications(
                response, NotificationHandler.notify_to_lagos_ops, rep3, user, hotdesk, '')
        except Exception as e:
            post_bugsnag_exception(e, f'Could not notify ops rep 3 - {rep3}')

    @staticmethod
    @dramatiq.actor
    def notify_to_lagos_ops(hotdesk, nextrep='', user='', response=''):
        """Method to notify the Lagos ops team for hot desk decision violation
        Args:
            nextrep (str): responder email
            user (str): requester name
            hotdesk (str): hot desk reference number
        Returns:
            Sends an escalation email to the ops team

        """
        from api.tasks.notifications.hot_desk import HotDeskNotifications
        from ..views.bot_actions import ActionResource
        action_resource = ActionResource()

        hot_desk_object = HotDeskRequest.query_().filter_by(
            hot_desk_ref_no=hotdesk).first()

        if hot_desk_object and hot_desk_object.status == HotDeskRequestStatusEnum.pending:
            try:
                hot_desk_id = hot_desk_object.id
                third_assignee_id = User.get_by_email(
                    AppConfig.HOT_DESK_ASSIGNEE3).token_id
                hotdesk_response = HotDeskResponse.query_().filter_by(
                    hot_desk_request_id=hot_desk_id,
                    assignee_id=third_assignee_id).first()
                # update the assignee
                hotdesk_response.update_(is_escalated=True)
                # send a slack message to the requester.
                action_resource.requester_slack_notification(hot_desk_object)
                # send email to Lagos ops.
                return HotDeskNotifications.send_notification_to_lagos_ops.send()
            except Exception as e:
                post_bugsnag_exception(e, 'Could not notify lagos ops')

    @staticmethod
    @dramatiq.actor
    def update_slack_ops_team(*args):
        """Method to update the decision button of responder after hot desk violation
        Args:
            ts (str): timestamp of slack notification initially sent to responder
            channel (str): bot channel
            rep (str): hot desk responder email
            requester(str): requester name
            hot_desk_ref_no (str): hot desk reference number
        """
        ts, channel, rep, requester, hot_desk_ref_no = args
        try:
            user = slack_helper.get_user_by_email(rep)
            username = user.get('name', '') if user else ''
            # cancels the approve and reject buttons
            return slack_helper.update_message_to_user(
                f"""Time's up! @{requester}'s request for *hot desk {hot_desk_ref_no}*
                has been forwarded to @{username} for approval""",
                ts, channel)
        except Exception as e:
            post_bugsnag_exception(
                e, 'Could not remove the accept reject buttons for the representatives ')

    @staticmethod
    @dramatiq.actor
    def notify_requester(hotdesk, requester_id):
        """Method to notify requester if request does not receive a response.
        Args:
            hotdesk (str): hot desk reference number
            requester_id (str): requester token_id
        """
        hot_desk_object = HotDeskRequest.query.filter_by(
            hot_desk_ref_no=hotdesk, requester_id=requester_id).order_by(
                HotDeskRequest.created_at.desc()).first()

        if hot_desk_object and hot_desk_object.status == HotDeskRequestStatusEnum.pending:
            try:
                requester_email = User.query_().filter_by(
                    token_id=requester_id).first().email
                requester_name = slack_helper.get_user_by_email(
                    requester_email)["name"]
                attachments = ""
                message = f"""Hey @{requester_name}, your request for *hot desk - {hotdesk}*
                    is yet to be attended to. """ \
                    "You can log a complaint on `# ask-activo` channel."

                return slack_helper.post_message_to_user(message, attachments, requester_email)
            except Exception as e:
                post_bugsnag_exception(e, 'Could not notify requester')

    @staticmethod
    @dramatiq.actor
    def notify_hot_desk_ineligible_requester(requester_email, requester_name):
        """Method to notify requester who has been assigned a permanent seat.
        Args:
            requester_email (str): requester email
            requester_name (str): requester name
        Returns:
            Sends a slack notification to the hot desk requester
        """
        try:
            user_email = check_if_user_email_is_in_google_sheet(requester_email)
            seat_location = cache.get('permanent_seat')
            ineligible_user = []
            if not user_email:
                ineligible_user.append(requester_email)
                cache.set('ineligible_user_list', ineligible_user, timeout=50)
                attachments = ''
                message = f"Hey @{requester_name}, {PERMANENT_SEAT_MSG.format(seat_location)}"
                return slack_helper.post_message_to_user(
                    message, attachments, requester_email)
            cache.set('ineligible_user_list', ineligible_user)
        except Exception as error:
            post_bugsnag_exception(
                error, f'Could not notify user')

    @staticmethod
    @dramatiq.actor
    def notify_user_after_hotdesk_cancellation(name, email):
        attachments = ""
        message = f"Hey @{name}, \n Your hot desk has been successfully *cancelled*"
        slack_helper.post_message_to_user(message, attachments,
                                          email)
