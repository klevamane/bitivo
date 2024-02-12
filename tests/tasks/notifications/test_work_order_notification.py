"""Module for testing request type notifications."""

# System libraries
from unittest.mock import Mock

# Utilites
from api.utilities.emails.email_templates import email_templates
from api.utilities.emails.email_factories.concrete_sendgrid import \
    ConcreteSendGridEmail

# Tasks
from api.tasks.notifications.work_orders import WorkOrderNotifications, SendEmail

# app config
from config import AppConfig


class TestWorkOrderNotifications:
    """Test assigning a work order"""

    def test_work_order_email_notifications_succeeds(
            self, init_db, new_user_two, new_work_order, new_user):
        """Test notify user when work order assigned to them
        Should send email to assignee when assigned to a work order

        Args:
            init_db(func): fixture to initialize the test database
            auth_header(obj): fixture for user authentication
            new_user(obj): Fixture to create a new user
            new_user_two(obj): Fixture to create a new user
            new_work_order(obj): Fixture to create a new work order

        Returns:
            None
        """
        AppConfig.MAIL_SERVICE = 'sendgrid'
        new_user_two.save()

        WorkOrderNotifications.notify_assignee_work_order.delay = Mock(
            side_effect=WorkOrderNotifications.notify_assignee_work_order)

        # mock the email sender
        SendEmail.send_mail_with_template = Mock()

        new_work_order.created_by = new_user_two.token_id
        work_order = new_work_order.save()

        data = SendEmail.send_mail_with_template.call_args[1]

        assert SendEmail.send_mail_with_template.called
        assert data['template_id'] == email_templates[
            'notify_assignee_work_order']['sendgrid']['id']
        assert data['recipient'] == new_user.email
        assert data['template_data']['username'] == new_user.name
        assert data['template_data']['workOrder'] == work_order.title
        assert data['template_data']['assignerName'] == new_user_two.name

    def test_update_work_order_email_notifications_succeeds(
            self, init_db, new_user, new_user_two, updated_work_order):
        """Test notify user when work order is updated
        Should send email to assignee when work order is updated

        Args:
            init_db(func): fixture to initialize the test database
            auth_header(obj): fixture for user authentication
            new_user(obj): Fixture to create a new user
            new_user_two(obj): Fixture to create a new user
            updated_work_order(obj): Fixture for updated work order

        Returns:
            None
         """
        AppConfig.MAIL_SERVICE = 'sendgrid'
        new_user_two.save()
        new_user.save()
        WorkOrderNotifications.notify_assignee_work_order.delay = Mock(
            side_effect=WorkOrderNotifications.notify_assignee_work_order)

        # mock the email sender
        SendEmail.send_mail_with_template = Mock()

        work_order = updated_work_order.save()

        data = SendEmail.send_mail_with_template.call_args[1]

        assert SendEmail.send_mail_with_template.called
        assert data['template_id'] == email_templates[
            'notify_assignee_work_order']['sendgrid']['id']
        assert data['recipient'] == new_user.email
        assert data['template_data']['username'] == new_user.name
        assert data['template_data']['workOrder'] == work_order.title
        assert data['template_data']['assignerName'] == new_user.name

    def test_reassign_work_order_email_notifications_succeeds(
            self, init_db, new_user, new_user_two, new_request_user,
            updated_work_order, request_ctx,
            mock_request_two_obj_decoded_token):
        """Test notify user when work order is re-assigned
        Should send email to assignee when work order is updated
        Args:
            init_db(func): fixture to initialize the test database
            auth_header(obj): fixture for user authentication
            new_user(obj): Fixture to create a new user
            new_user_two(obj): Fixture to create a new user two
            new_request_user(obj):fixture for a user
            updated_work_order(obj): Fixture for updated work order
        Returns:
            None
        """

        AppConfig.MAIL_SERVICE = 'sendgrid'
        new_user_two.save()
        new_user.save()
        new_request_user.save()
        work_order = updated_work_order.save()

        WorkOrderNotifications.notify_assignee_work_order.delay = Mock(
            side_effect=WorkOrderNotifications.notify_assignee_work_order)
        work_order.get(work_order.id)
        SendEmail.send_mail_with_template = Mock()
        work_order.update_(
            title='changes', assignee_id=new_request_user.token_id)

        # mock send mail with template method

        get_templates = SendEmail.send_mail_with_template.call_args_list

        # template for informing a user work order has been reassigned
        old_assignee_template = get_templates[0][1]

        # Template for informing the new user of workorder being assigned to them
        new_assignee_template = get_templates[1][1]

        assert SendEmail.send_mail_with_template.called
        assert old_assignee_template['template_id'] == email_templates[
            'reassignee_work_order']['sendgrid']['id']
        assert old_assignee_template['recipient'] == new_user.email
        assert old_assignee_template['template_data'][
            'username'] == new_user.name
        assert old_assignee_template['template_data'][
            'workOrderTitle'] == work_order.title
        assert old_assignee_template['template_data'][
            'newAssignee'] == new_request_user.name

        assert new_assignee_template['template_id'] == email_templates[
            'notify_assignee_work_order']['sendgrid']['id']
        assert new_assignee_template['recipient'] == new_request_user.email
        assert new_assignee_template['template_data'][
            'username'] == new_request_user.name
        assert new_assignee_template['template_data'][
            'workOrder'] == work_order.title
        assert new_assignee_template['template_data'][
            'assignerName'] == new_user.name
