"""Module for testing shedule notifications."""

# System libraries
from unittest.mock import patch, Mock

# Tasks
from api.tasks.notifications.schedule import SchedulesNotifications, SendEmail

# Enum
from api.utilities.enums import ScheduleStatusEnum

# app config
from config import AppConfig


class TestSchedulesNotifications:
    """Test assigning a work order schedule"""

    def test_send_assigner_notification_succeds(
            self, init_db, new_test_schedule_completed, new_test_user,
            new_work_order_for_schedules):
        """Test email nofitication succeeds when an assignee marks a work order has done.
        
        Args:
            init_dd: Initialises the database
            new_test_user: Returns the recipient which we use to get the email
            new_work_order_for_schedules: Returns the work_order_schedule which is used to get the work order title.
            new_test_schedule_completed: When a shedule for a particular is marked as done.
        Returns:
            None
        """
        AppConfig.MAIL_SERVICE = 'mailgun'
        schedule = new_test_schedule_completed.save()

        SchedulesNotifications.send_work_order_notification.delay = Mock(
            side_effect=SchedulesNotifications.send_work_order_notification)
        SendEmail.send_mail_with_template = Mock()
        schedule.update_(status=ScheduleStatusEnum.done)
        template_data = SendEmail.send_mail_with_template.call_args[1]

        assert SendEmail.send_mail_with_template.called
        assert template_data['recipient'] == new_test_user.email
        assert template_data[
            'mail_subject'] == new_work_order_for_schedules.title
        assert template_data['mail_html_body']
