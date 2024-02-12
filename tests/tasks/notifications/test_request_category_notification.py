"""Test module for request assignee notification"""

# Standard library
from unittest.mock import Mock

# tasks
from api.tasks.notifications.request import RequestNotifications, SendEmail

# utilities
from api.utilities.emails.email_templates import email_templates

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1


class TestRequestAssigneeNotification:
    """Test the request category assignee method"""

    def test_request_category_assignee_notification_succeeds(
            self, client, init_db, auth_header, new_request):
        """Should return a 201 status code and new request data when data provided
        in request is valid

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request (dict): fixture to create a new request
        """
        AppConfig.MAIL_SERVICE = 'sendgrid'
        # mocking the celery delay
        RequestNotifications.notify_request_type_assignee \
            .delay = Mock(side_effect=RequestNotifications
                          .notify_request_type_assignee)

        # mocking the sendGrid email concrete
        SendEmail.send_mail_with_template = Mock()

        # create a new request
        request = new_request.save()

        # get arguments being passed to the send_mail_with_template_method
        data = SendEmail.send_mail_with_template.call_args[1]

        # assertions
        assert data['recipient'] == request.request_type.assignee.email
        assert data['template_id'] == email_templates[
            'logged_category_request']['sendgrid']['id']
        assert data['template_data']['assignee_name'] == request.request_type \
            .assignee.name
        assert data['template_data']['requester'] == request.requester.name
        assert data['template_data']['request_category_name'] == request \
            .request_type.title
        SendEmail.send_mail_with_template.assert_called()
