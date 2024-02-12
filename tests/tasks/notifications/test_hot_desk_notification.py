"""Module for testing lagos ops email notifications after a hot-desk request."""
# System libraries
from unittest.mock import patch, Mock

from api.tasks.notifications.hot_desk import HotDeskNotifications, SendEmail
# from bot.tasks.slack_bot import BotTasks

# app config
from config import AppConfig

# enum
from api.utilities.enums import HotDeskRequestStatusEnum

# Models
from api.models import User, HotDeskRequest


class TestHotDeskMailNotification:
    """Used to desk hot desk notification"""

    def test_send_ops_notification_succeeds(self, init_db,
                                            new_hot_desk_request):
        """Test email notification succeeds when user makes hotdesk request
        Args:
        new_hot_desk_request: to create a new HotDesk
        Returns:
        None
        """
        AppConfig.MAIL_SERVICE = 'mailgun'
        HotDeskNotifications.send_notification.send = Mock(
            side_effect=HotDeskNotifications.send_notification)

        desk_info = new_hot_desk_request.hot_desk_ref_no.split(" ")
        SendEmail.send_mail_with_template = Mock()
        new_hot_desk_request.save()
        template_data = SendEmail.send_mail_with_template.call_args[1]
        assert SendEmail.send_mail_with_template.called
        assert template_data['mail_subject'] == 'New Hot Desk Request'
        assert template_data['recipient'] == AppConfig.LAGOS_OPS_TEAM

    def test_send_rejection_notification_succeeds(self, init_db,
                                                  new_hot_desk_request):
        """Test email notification succeeds when user makes hotdesk request
        Args:
        new_hot_desk_request: to create a new HotDesk
        Returns:
        None
        """
        AppConfig.MAIL_SERVICE = 'mailgun'
        HotDeskNotifications.send_hot_desk_decision_notification.send = Mock(
            side_effect=HotDeskNotifications.
            send_hot_desk_decision_notification)

        SendEmail.send_mail_with_template = Mock()

        new_hot_desk_request.save()
        hot_desk = HotDeskRequest.query_().filter_by(id=new_hot_desk_request.id).first()
        hot_desk.update_(status=HotDeskRequestStatusEnum.rejected,
                    reason='you are not eligible')

        requester_email = User.query_().filter_by(
            token_id=hot_desk.requester_id).first().email

        template_data = SendEmail.send_mail_with_template.call_args[1]
        assert SendEmail.send_mail_with_template.called
        assert template_data['mail_subject'] == 'Hot Desk Rejected'
        assert template_data['recipient'] == requester_email

    def test_send_approval_notification_succeeds(self, init_db,
                                                 new_hot_desk_request):
        """Test email notification succeeds when user makes hotdesk request
        Args:
        new_hot_desk_request: to create a new HotDesk
        Returns:
        None
        """
        AppConfig.MAIL_SERVICE = 'mailgun'
        HotDeskNotifications.send_hot_desk_decision_notification.send = Mock(
            side_effect=HotDeskNotifications.
            send_hot_desk_decision_notification)

        SendEmail.send_mail_with_template = Mock()

        new_hot_desk_request.save()
        hot_desk = HotDeskRequest.query_().filter_by(id=new_hot_desk_request.id).first()
        hot_desk.update_(status=HotDeskRequestStatusEnum.approved)

        requester_email = User.query_().filter_by(
            token_id=hot_desk.requester_id).first().email

        template_data = SendEmail.send_mail_with_template.call_args[1]
        assert SendEmail.send_mail_with_template.called
        assert template_data['mail_subject'] == 'Hot Desk Approved'
        assert template_data['recipient'] == requester_email

    def test_send_notification_to_lagos_ops(self, init_db,
                                            new_hot_desk_request):
        """Test email notification succeeds when he hot desk request is not handled
        Args:
            new_hot_desk_request: to create a new HotDesk
        Returns:
            None
        """

        LAGOS_OPS_TEAM = 'ops@andela.com'
        AppConfig.MAIL_SERVICE = 'mailgun'
        hot_desk = new_hot_desk_request.save()
        HotDeskNotifications.send_notification_to_lagos_ops = Mock(
            side_effect=HotDeskNotifications.send_notification_to_lagos_ops())

        SendEmail.send_mail_with_template = Mock()
        assert SendEmail.send_mail_with_template.asset_called_once()
    
    def test_send_cancel_notification_succeeds(self, init_db,
                                                 new_today_hot_desk):
        """Test email notification succeeds when user cancel hotdesk request
        Args:
        new_hot_desk_request(Hotdesk): to create a new HotDesk
        Returns:
        None
        """
        AppConfig.MAIL_SERVICE = 'mailgun'
        HotDeskNotifications.send_hot_desk_decision_notification.send = Mock(
            side_effect=HotDeskNotifications.
            send_hot_desk_decision_notification)
    

        SendEmail.send_mail_with_template = Mock()

        hot_desk = new_today_hot_desk.save()
        hot_desk = HotDeskRequest.query_().filter_by(id=new_today_hot_desk.id).first()
        hot_desk.update_(
            status=HotDeskRequestStatusEnum.cancelled,
            reason='i am busy'
            )

        template_data = SendEmail.send_mail_with_template.call_args[1]
        assert SendEmail.send_mail_with_template.called
        assert template_data['mail_subject'] == 'Hot Desk Cancelled'
