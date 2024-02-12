"""Test module for request notification"""

# Standard library
from unittest.mock import patch, Mock

# tasks
from api.tasks.notifications.request import RequestNotifications, SendEmail

from api.utilities.enums import RequestStatusEnum
from api.utilities.constants import YOU, ACTIVO_SYSTEM
from api.utilities.emails.email_templates import email_templates

# app config
from config import AppConfig


@patch(
    "api.utilities.emails.email_factories.concrete_sendgrid.ConcreteSendGridEmail.send_mail_with_template"
)
class TestRequestNotification:
    """Test the requester status method"""

    def test_notify_on_status_change_from_open_to_in_progress_succeeds(
            self, init_db, new_request, request_ctx,
            mock_request_two_obj_decoded_token, new_user):
        """Should send email when the request status changes from open to in progress.

        Args:
            new_request (obj): fixture to get request data
        Returns:
            None
        """
        new_user.save()
        AppConfig.MAIL_SERVICE = 'sendgrid'

        request = new_request.save()
        RequestNotifications.requester_status.delay = Mock(
            side_effect=RequestNotifications.requester_status)

        request.update_(status=RequestStatusEnum.in_progress)
        data = SendEmail.send_mail_with_template.call_args[1]

        assert data['template_id'] == email_templates['requester_status'][
            'sendgrid']['id']
        assert data['template_data']['status'] == RequestStatusEnum.in_progress
        assert data['template_data']['assignee'] == request.responder.name
        assert data['template_data']['subject'] == request.subject
        assert data['template_data']['username'] == request.requester.name
        assert request.status == RequestStatusEnum.in_progress
        assert request._old_status != RequestStatusEnum.in_progress
        assert SendEmail.send_mail_with_template.called

    def test_notify_on_status_change_from_in_progress_to_completed_succeeds(
            self, init_db, new_request, request_ctx,
            mock_request_two_obj_decoded_token, new_user):
        """Should send email when the reequest status changes from in progress to completed.

        Args:
            new_request (obj): fixture to get request data

        Returns:
            None
        """
        new_user.save()
        AppConfig.MAIL_SERVICE = 'sendgrid'
        request = new_request.save()
        request.update_(status=RequestStatusEnum.completed)

        data = SendEmail.send_mail_with_template.call_args[1]

        assert data['template_id'] == email_templates['requester_status'][
            'sendgrid']['id']
        assert data['template_data']['status'] == RequestStatusEnum.completed
        assert data['template_data']['assignee'] == request.responder.name
        assert data['template_data']['subject'] == request.subject
        assert data['template_data']['username'] == request.requester.name
        assert request.status == RequestStatusEnum.completed
        assert request._old_status != RequestStatusEnum.completed
        assert SendEmail.send_mail_with_template.called

    def test_notify_on_status_change_from_completed_to_closed_succeeds(
            self, init_db, new_request, request_ctx,
            mock_request_two_obj_decoded_token, new_user):
        """Should send email when the reequest status changes from completed to closed.
        Args:
            new_request (obj): fixture to get request data
   
        Returns:
            None
        """
        new_user.save()
        AppConfig.MAIL_SERVICE = 'sendgrid'
        request = new_request.save()
        request.update_(status=RequestStatusEnum.closed)

        data = SendEmail.send_mail_with_template.call_args[1]

        assert data['template_id'] == email_templates['requester_status'][
            'sendgrid']['id']

        assert data['template_data']['status'] == RequestStatusEnum.closed
        assert data['template_data']['subject'] == request.subject
        assert data['template_data']['username'] == request.requester.name
        assert data['template_data']['assignee'] == YOU
        assert request.status == RequestStatusEnum.closed
        assert request._old_status != RequestStatusEnum.closed
        assert SendEmail.send_mail_with_template.called

    def test_notify_on_status_change_from_completed_to_closed_by_system_succeeds(
            self, init_db, create_new_request, request_ctx,
            mock_request_two_obj_decoded_token, new_user):
        """Should send email when the reequest status changes from completed to closed by the syatem.
 
        Args:
            new_request (obj): fixture to get request data
    
        Returns:
            None
        """
        new_user.save()
        AppConfig.MAIL_SERVICE = 'sendgrid'
        request = create_new_request.save()
        request.update_(status=RequestStatusEnum.closed, closed_by_system=True)

        data = SendEmail.send_mail_with_template.call_args[1]

        assert data['template_id'] == email_templates['closed_by_system'][
            'sendgrid']['id']
        assert data['template_data']['status'] == RequestStatusEnum.closed
        assert data['template_data']['subject'] == request.subject
        assert data['template_data']['username'] == request.requester.name
        assert data['template_data']['assignee'] == ACTIVO_SYSTEM
        assert request.status == RequestStatusEnum.closed
        assert request._old_status != RequestStatusEnum.closed
        assert SendEmail.send_mail_with_template.called
