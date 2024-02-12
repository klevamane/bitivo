# Third Party Libraries
from sendgrid.helpers.mail import Mail

# System
from datetime import datetime
from os import environ
from unittest.mock import Mock

# System libraries
from unittest.mock import patch

# Services
from api.services.schedule_notification import schedule_due_date_notifier, SendEmail

# Utilities
from api.utilities.emails.email_templates import email_templates

# app config
from config import AppConfig


class TestScheduleDueDateNotifier:
    """Test schedule due date email notifications."""

    def test_schedule_email_notification_on_when_due_date_is_not_today_fails(
            self, init_db, new_schedule):
        """Test email notification succeeds when a schedule due date is reached

         Args:
            mock_send_mail(MagicMock): A sendgrid mock instance
            init_db(SQLAlchemy): fixture to initialize the test database
            new_schedule(Schedule): fixture for creating a new schedule that is due today
         """
        new_schedule.save()
        schedule_due_date_notifier()
        response = schedule_due_date_notifier()

        assert response == False

    def test_schedule_email_notification_on_due_date_succeeds(
            self, init_db, new_user, new_test_schedule):
        """Test email notification succeeds when a schedule due date is reached

         Args:
            init_db(SQLAlchemy): fixture to initialize the test database
            new_user: fixture to create a new user
            new_test_schedule(Schedule): fixture for creating a new schedule that is due today
         """
        AppConfig.MAIL_SERVICE = 'mailgun'
        new_test_schedule.save()
        new_user.save()
        SendEmail.send_mail_with_template = Mock()
        response = schedule_due_date_notifier()
        mail_obj = SendEmail.send_mail_with_template.call_args[1]

        assert SendEmail.send_mail_with_template.called
        assert mail_obj['recipient'] == new_user.email
        assert mail_obj['mail_subject'] == new_user.name
        assert mail_obj['mail_html_body']
        assert response
