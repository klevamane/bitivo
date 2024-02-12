from . import SendEmail

from sqlalchemy.orm.attributes import get_history

# Models
from api.models import User

#Utilities
from api.utilities.helpers.env_resource_adapter import adapt_resource_to_env
from api.utilities.helpers.get_mailing_params import get_mailing_params
from api.utilities.emails.email_templates import email_templates
from api.utilities.constants import HOT_DESK_EMAIL_TEMPLATE

from main import celery_app, dramatiq
from config import AppConfig


class HotDeskNotifications:
    """Notifications helper and celery app sender"""

    @staticmethod
    @dramatiq.actor
    def send_notification_to_lagos_ops():
        """Method that sends an escalation email to the ops
        team
        """
        LAGOS_OPS_TEAM = AppConfig.LAGOS_OPS_TEAM
        params = get_mailing_params('escalate_email',
                                    "Unhandled Hot Desk Request", {}, 
                                    HOT_DESK_EMAIL_TEMPLATE)
        params = dict(recipient=LAGOS_OPS_TEAM, **params)
        return SendEmail.send_mail_with_template(**params)

    @staticmethod
    def send_notifications_handler(target):
        """Method that handles sending an assignee notifications when a
        hot desk request is made
        Args:
            *args:
                target(str) Object of the last inserted hotdesk request
        """
        requester = User.get(target.requester_id)
        requester_name = requester.name

        desk_info = target.hot_desk_ref_no.split(" ")
        requester_email = requester.email
        floor = desk_info[-2]
        seat_number = desk_info[-1]
        email_notify = adapt_resource_to_env(
            HotDeskNotifications.send_notification.send)
        LAGOS_OPS_TEAM = AppConfig.LAGOS_OPS_TEAM
        email_notify(LAGOS_OPS_TEAM, requester_name, floor, seat_number,
                     requester_email)

    @staticmethod
    @dramatiq.actor
    def send_notification(*args):
        """"Method that sends an assignee notifications when a
        hot desk request is made
         Args:
            *args:
                assignee_email(str): Email of requester
                floor(str): Floor Number of Hot Desk
                seat_number(str): Seat number of Hot Desk
                requester_name(str): Name of requester
                requester_email(str): Email of requester
         """
        assignee_email, requester_name, floor, seat_number, \
            requester_email = args
        template_data = {
            "floor": floor,
            "seatNumber": seat_number,
            "requesterName": requester_name,
            "requesterEmail": requester_email,
            "assigneeEmail": assignee_email
        }
        params = get_mailing_params('notify_ops_hotdesk',
                                    "New Hot Desk Request", template_data, 
                                    HOT_DESK_EMAIL_TEMPLATE)
        params = dict(recipient=assignee_email, **params)
        return SendEmail.send_mail_with_template(**params)

    @staticmethod
    @dramatiq.actor
    def send_hot_desk_decision_notification(email_details):
        """"Method that sends rejection notifications
        Args:
            email_details(obj):
                requester_email(str): Email of requester
                requester_name(list): List of names/name of requester
                floor(str): Floor Number of Hot Desk
                reason(str): Reason for sending mail
                seat_number(str): Seat number of Hot Desk
                approver_name(list): List of names/name of approver
                status(str): Status of the request
        """
        reason, requester_name, floor, seat_number, first_name, last_name, requester_email, status = HotDeskNotifications.get_email_details(
            email_details)
        template_data = HotDeskNotifications.generate_template_data(
            reason, requester_name, floor, seat_number, first_name, last_name)

        if status == 'rejected':
            return HotDeskNotifications.send_hot_desk_notification_after_update('notify_hotdesk_rejection', 
            "Hot Desk Rejected", requester_email, template_data)
        if status == 'approved':
            return HotDeskNotifications.send_hot_desk_notification_after_update('notify_hotdesk_approval',
                                        "Hot Desk Approved", requester_email, template_data)
        if status == 'cancelled':
            return HotDeskNotifications.send_hot_desk_notification_after_update(
                'notify_hotdesk_cancelling', 'Hot Desk Cancelled', requester_email, template_data)

    @staticmethod
    def send_hot_desk_notification_after_update(template, subject, requester_email, template_data):
        """Method that handles sending after rejection updates
        Args:
            template(str): The dictionary key that holds the email template to be used
            subject(str): Subject of the notification
            requester_email(str): Email of requester
            template_data(dict): Template data
        """
        params = get_mailing_params(template, subject, template_data, HOT_DESK_EMAIL_TEMPLATE)
        params = dict(recipient=requester_email, **params)
        return SendEmail.send_mail_with_template(**params)

    @staticmethod
    def send_hot_desk_decision_handler(target):
        """Method that handles sending rejection notifications
        Args:
            target(obj) Object of the last inserted hotdesk request
        """
        requester = User.get(target.requester_id)
        reason = target.reason if target.reason else ''
        names = requester.name.split()

        first_name, last_name = (names[0], names[1]) if len(names) > 1 else (
            requester.name, "")

        new_status, unchanged, old_status = get_history(target, 'status')

        approver = User.get(target.assignee_id)

        approver_name = approver.name.split(
            " ") if approver and approver.email != requester.email else None

        if approver_name:
            decision_details = HotDeskNotifications.generate_details(
                target, approver_name, first_name, last_name)

            email_notify_rejection = adapt_resource_to_env(
                HotDeskNotifications.send_hot_desk_decision_notification.send)
            email_notify_rejection(decision_details)

    @staticmethod
    def generate_details(*args):
        """Method that generates details of email
        Args:
            approver_name(str): Name of approver
            target(obj): Object of the last inserted hotdesk request
            first_name(str): First name of requester
            last_name(str): Last name of requester
        """
        target, approver_name, first_name, last_name = args
        desk_info = target.hot_desk_ref_no.split(" ")
        return {
            "requester_name": [first_name, last_name],
            "requester_email": User.get(target.requester_id).email,
            "floor": desk_info[-2],
            "seat_number": desk_info[-1],
            "approver_name": approver_name,
            "reason": target.reason if target.reason else '',
            "status": target.status if isinstance(target.status, str) else target.status.value
        }

    @staticmethod
    def generate_template_data(*args):
        """Method that generates template data
        Args:
            requester_name(str): Name of requester
            floor(str): Floor Number of Hot Desk
            seat_number(str): Seat number of Hot Desk
            reason(str): Reason for sending mail
            first_name(str): First name of requester
            last_name(str): Last name of requester
        """
        reason, requester_name, floor, seat_number, first_name, last_name = args
        return {
            "requester_name": requester_name,
            "floor": floor,
            "seat_number": seat_number,
            "first_name": first_name,
            "last_name": last_name,
            "reason": reason
        }

    @staticmethod
    def get_email_details(email_details):
        """Method that gets email details
        Args:
            email_details(obj):
                requester_email(str): Email of requester
                requester_name(str): Name of requester
                floor(str): Floor Number of Hot Desk
                seat_number(str): Seat number of Hot Desk
                approver_name(str): Name of approver
                reason(str): Reason for sending mail
                status(str): Status of the request
        """
        requester_email, requester_name, floor, seat_number, approver_name, reason, status = (
            email_details["requester_email"], email_details["requester_name"],
            email_details["floor"], email_details["seat_number"],
            email_details["approver_name"], email_details["reason"],
            email_details["status"])
        requester_name = requester_name[0] + ' ' + requester_name[1] if len(
            requester_name) > 1 else ''
        first_name = approver_name[0]
        last_name = approver_name[1] if len(approver_name) > 1 else ""

        return reason, requester_name, floor, seat_number, first_name, last_name, requester_email, status
