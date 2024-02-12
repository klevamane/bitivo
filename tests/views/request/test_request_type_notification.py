"""Module for testing request type notifications."""
# System libraries
from unittest.mock import patch, Mock

from api.utilities.emails.email_templates import email_templates
from api.tasks.notifications.request_type import RequestTypeNotification, SendEmail

# app config
from config import AppConfig


class TestRequestTypeNotification:
    def test_request_type_email_notification_when_assignee_is_the_same_as_assigner_fails(
            self, init_db, new_request_type, new_user, new_user_two):
        """Tests that the  notification is not sent when a user assignee is assigner

        Should not send the email notification when a user assigns himself a
        requestType

        Args:
            init_db(SQLAlchemy): fixture to initialize the test database
            new_user (obj): Fixture to load new user obj.

        Returns:
            None
         """
        RequestTypeNotification.send_request_type_email.delay = Mock(
            side_effect=RequestTypeNotification.send_request_type_email)

        SendEmail.send_mail_with_template = Mock()

        new_user.save()
        new_request_type.created_by = new_user.token_id
        new_request_type.assignee_id = new_user.token_id
        new_request_type.save()
        assert not SendEmail.send_mail_with_template.called

    def test_request_type_email_notification_succeeds(
            self, init_db, new_request_type, new_user, new_user_two):
        """Test email notification succeeds when a user assigned to a request type

        Args:
            init_db(SQLAlchemy): fixture to initialize the test database
            new_user (obj): Fixture to load new user obj.

        Returns:
            None
         """
        AppConfig.MAIL_SERVICE = 'sendgrid'
        RequestTypeNotification.send_request_type_email.delay = Mock(
            side_effect=RequestTypeNotification.send_request_type_email)

        SendEmail.send_mail_with_template = Mock()

        new_user.save()
        new_user_two.save()
        new_request_type.created_by = new_user_two.token_id
        new_request_type.assignee_id = new_user.token_id
        new_request_type.save()

        data = SendEmail.send_mail_with_template.call_args[1]

        assert data['template_id'] == email_templates["request_type_assigned"][
            'sendgrid']["id"]
        assert data['template_data'][
            'request_category_name'] == new_request_type.title
        assert data['template_data']['username'] == new_user.name
        assert data['template_data']['user'] == new_user_two.name
        assert SendEmail.send_mail_with_template.called
