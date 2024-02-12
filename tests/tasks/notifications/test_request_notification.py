"""Module for testing request type notifications."""
# Standard library
import json
from unittest.mock import Mock

# Tasks
from api.tasks.notifications.request import RequestNotifications, SendEmail

# Utilites
from api.utilities.constants import CHARSET
from api.utilities.emails.email_templates import email_templates

# app config
from config import AppConfig

api_v1_base_url = AppConfig.API_BASE_URL_V1


class TestRequestNotifications:
    def test_technician_email_notification_succeeds(
            self, init_db, auth_header, client, new_user, new_request,
            request_ctx, mock_request_two_obj_decoded_token):
        """Test notify technician

        Should send email to technician when assigned to handle a request

        Args:
            init_db(SQLAlchemy): fixture to initialize the test database
            client (FlaskClient): Fixture to get flask test client.
            new_user: Fixture to create a new user
            new_request: Fixture to create a new request

        Returns:
            None
         """
        AppConfig.MAIL_SERVICE = 'sendgrid'
        user = new_user.save()
        request = new_request.save()

        # mock notify method to be called with out celery task
        RequestNotifications.notify_technician.delay = Mock(
            side_effect=RequestNotifications.notify_technician)

        # mock the email sender
        SendEmail.send_mail_with_template = Mock()

        # assign a request to a technician
        request.update_(assignee_id=user.token_id)

        # get arguments passed to email sender method
        data = SendEmail.send_mail_with_template.call_args[1]

        # assert that email notification is sent to an assignee
        assert request.assignee is not None
        assert SendEmail.send_mail_with_template.called
        assert data['recipient'] == request.assignee.email
        assert data['template_id'] == email_templates[
            'assign_request_to_technician']['sendgrid']['id']
        assert data['template_data']['username'] == request.responder.name
        assert data['template_data']['assignee'] == request.assignee.name
        assert data['template_data']['subject'] == request.subject
