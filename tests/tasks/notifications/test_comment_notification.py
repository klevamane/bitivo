"""Test module for comment notification"""

from sendgrid.helpers.mail import Mail

# Standard library
from unittest.mock import Mock

# tasks
from api.tasks.notifications.comment import CommentNotifications, SendEmail
from faker import Faker

# utilities
from api.utilities.emails.email_factories.concrete_sendgrid import \
    ConcreteSendGridEmail

from unittest.mock import patch
from api.utilities.emails.email_templates import email_templates
from api.models import Comment
from api.utilities.enums import ParentType

fake = Faker()

from config import AppConfig


class TestCommentNotification:
    """Test the request category assignee method"""

    def test_notify_responder_when_the_requester_comments_succeeds(
            self, init_db, new_requester, new_responder,
            new_request_by_requester):
        """Notifies relevant user when a comment is made

            Should notify the responder when the requester is the author
            of a comment

            Args:
                init_db (obj): fixture that contains the comment info
                new_requester (obj): fixture that contains a user that made a request
                new_responder(obj): fixture that contains the user to respond to the request
                new_request_by_requester(obj): fixture that contains the request that made by requester

        """

        AppConfig.MAIL_SERVICE = 'sendgrid'
        new_request_by_requester.save()
        request_id = new_request_by_requester.id
        author_id = new_request_by_requester.requester.token_id
       
        CommentNotifications.send_notification.delay = Mock(
            side_effect=CommentNotifications.send_notification)

        # mock the email sender
        SendEmail.send_mail_with_template = Mock()

        comment = Comment(
            body=fake.sentence(), parent_id=request_id, author_id=author_id)

        comment.save()

        # get arguements passed to email sender method
        data = SendEmail.send_mail_with_template.call_args[1]

        assert data['template_id'] == email_templates["request_comment"][
            'sendgrid']["id"]
        assert data['recipient'] == \
            new_request_by_requester.responder.email
        assert data['template_data'][
            "subject"] == new_request_by_requester.subject
        assert data['template_data'][
            "username"] == new_request_by_requester.responder.name
        assert data['template_data'][
            "assignee"] == new_request_by_requester.requester.name

        assert SendEmail.send_mail_with_template.called

    def test_notify_requester_when_the_responder_comments_succeeds(
            self, init_db, new_request_by_requester):
        """Notify relevant user when a comment is made

            Should notify the requester  when the responder is the author
            of a comment

            Args:
                init_db (obj): fixture that contains the comment info
                new_request_requester (obj): fixture that contains a user that made a request
                new_request_responder(obj): fixture that contains the user to respond to the request
                new_request_by_requester(obj): fixture that contains the request that made by requester

        """
        AppConfig.MAIL_SERVICE = 'sendgrid'
        new_request_by_requester.save()
        request_id = new_request_by_requester.id
        author_id = new_request_by_requester.responder.token_id

        CommentNotifications.send_notification.delay = Mock(
            side_effect=CommentNotifications.send_notification)

        # mock the email sender
        SendEmail.send_mail_with_template = Mock()

        comment = Comment(
            body=fake.sentence(), parent_id=request_id, author_id=author_id)
        comment.save()

        data = SendEmail.send_mail_with_template.call_args[1]

        assert data['template_id'] == email_templates["request_comment"][
            'sendgrid']["id"]
        assert data['recipient'] == \
               new_request_by_requester.requester.email
        assert data['template_data'][
            "subject"] == new_request_by_requester.subject
        assert data['template_data'][
            "username"] == new_request_by_requester.requester.name
        assert data['template_data'][
            "assignee"] == new_request_by_requester.responder.name
        assert SendEmail.send_mail_with_template.called

    def test_notify_both_the_responder_and_request_when_the_author_is_neither_of_them_succeeds(
            self, init_db, new_mock_user, new_request_by_requester):
        """Notify relevant user when a comment is made

            Should notify the requester  and the responder when the
            author of the request is neither the requester nor the responder

            Args:
                init_db (obj): fixture that contains the comment info
                new_request_by_requester(obj): fixture that contains the request that made by requester

        """
        AppConfig.MAIL_SERVICE = 'sendgrid'
        new_request_by_requester.save()
        new_mock_user.save()
        request_id = new_request_by_requester.id
        author_id = new_mock_user.token_id

        CommentNotifications.send_notification.delay = Mock(
            side_effect=CommentNotifications.send_notification)

        # mock the email sender
        SendEmail.send_mail_with_template = Mock()

        comment = Comment(
            body=fake.sentence(), parent_id=request_id, author_id=author_id)

        comment.save()

        mail_obj_one, mail_obj_two = SendEmail.send_mail_with_template.call_args_list

        mail_obj_one, mail_obj_two = mail_obj_one[1], mail_obj_two[1]

        requester_email = new_request_by_requester.requester.email
        responder_email = new_request_by_requester.responder.email

        assert mail_obj_one['template_id'] == mail_obj_two['template_id']
        assert (mail_obj_one['recipient'] == requester_email) or (
            mail_obj_one['recipient'] == responder_email)
        assert (mail_obj_two['recipient'] == requester_email) or (
            mail_obj_two['recipient'] == responder_email)
        assert email_templates["request_comment"]['sendgrid'][
            "id"] == mail_obj_one['template_id']
        assert mail_obj_one['template_data'][
            "subject"] == new_request_by_requester.subject
        assert mail_obj_two['template_data'][
            "subject"] == new_request_by_requester.subject

        assert SendEmail.send_mail_with_template.called

    def test_notify_assignee_when_assigner_comment_work_order_schedule_succeeds(
            self, init_db, new_schedule_with_assigner,
            new_work_order_with_assigner, new_user, new_user_two):
        """Notifies assignee when assigner comments on the work order schedules succeeds

            Args:
                init_db (obj): fixture that contains the comment info
                new_schedule_with_assigner (obj): fixture that contains a schedule
                new_work_order_with_assigner(obj): fixture that contains work order
                new_user(obj): fixture that contains the request new user
                new_user_two(obj): fixture that contains the new user two

        """

        AppConfig.MAIL_SERVICE = 'mailgun'
        new_schedule_with_assigner.save()
        new_work_order_with_assigner.save()
        new_user_two.save()
        new_user.save()

        schedule_id = new_schedule_with_assigner.id
        author_id = new_schedule_with_assigner.assignee_id

        CommentNotifications.send_notification.delay = Mock(
            side_effect=CommentNotifications.send_notification)
        # mocks the email sender
        SendEmail.send_mail_with_template = Mock()

        comment = Comment(
            body=fake.sentence(),
            parent_id=schedule_id,
            author_id=author_id,
            parent_type=ParentType.Schedule)

        comment.save()
        schedule_comment = comment.body
        sender_name = new_user.name
        work_order_title = new_work_order_with_assigner.title

        # get arguements passed to email sender method
        data = SendEmail.send_mail_with_template.call_args[1]
        assert data['recipient'] == new_user_two.email
        assert SendEmail.send_mail_with_template.called
        assert schedule_comment and sender_name and work_order_title in data[
            'mail_html_body']

    def test_notify_assigner_when_assignee_comment_schedule_succeeds(
            self, init_db, new_schedule_with_assigner,
            new_work_order_with_assigner, new_user, new_user_two):
        """Notifies assigner when assignee comments on the work order schedules succeeds

            Args:
                init_db (obj): fixture that contains the comment info
                new_schedule_with_assigner (obj): fixture that contains a schedule
                new_work_order_with_assigner(obj): fixture that contains work order
                new_user(obj): fixture that contains the request new user
                new_user_two(obj): fixture that contains the new user two

        """

        AppConfig.MAIL_SERVICE = 'mailgun'
        new_schedule_with_assigner.save()
        new_work_order_with_assigner.save()
        new_user_two.save()
        new_user.save()

        schedule_id = new_schedule_with_assigner.id
        author_id = new_work_order_with_assigner.created_by

        CommentNotifications.send_notification.delay = Mock(
            side_effect=CommentNotifications.send_notification)

        # mock the email sender
        SendEmail.send_mail_with_template = Mock()

        comment = Comment(
            body=fake.sentence(),
            parent_id=schedule_id,
            author_id=author_id,
            parent_type=ParentType.Schedule)

        comment.save()

        schedule_comment = comment.body
        sender_name = new_user_two.name
        work_order_title = new_work_order_with_assigner.title

        data = SendEmail.send_mail_with_template.call_args[1]
        assert data['recipient'] == new_user.email
        assert schedule_comment and sender_name and work_order_title in data[
            'mail_html_body']
        assert SendEmail.send_mail_with_template.called

    def test_notify_assigner_assignee_when_work_order_comment_by_other_users_succeeds(
            self, init_db, new_mock_user, new_schedule_with_assigner,
            new_work_order_with_assigner, new_user, new_user_two):
        """Notifies assigner and assignee when work-schedule is
            commented by other users succeeds

            Args:
                init_db (obj): fixture that contains the comment info
                new_schedule_with_assigner (obj): fixture that contains a schedule
                new_work_order_with_assigner(obj): fixture that contains work order
                new_user(obj): fixture that contains the request new user
                new_user_two(obj): fixture that contains the new user two

        """
        AppConfig.MAIL_SERVICE = 'mailgun'

        new_schedule_with_assigner.save()
        new_work_order_with_assigner.save()
        new_mock_user.save()
        new_mock_user.save()
        schedule_id = new_schedule_with_assigner.id
        author_id = new_mock_user.token_id

        CommentNotifications.send_notification.delay = Mock(
            side_effect=CommentNotifications.send_notification)

        # mock the email sender
        SendEmail.send_mail_with_template = Mock()

        comment = Comment(
            body=fake.sentence(),
            parent_id=schedule_id,
            author_id=author_id,
            parent_type=ParentType.Schedule)

        comment.save()
        assignee = new_user.email
        assigner = new_user_two.email

        mail_obj_one, mail_obj_two = SendEmail.send_mail_with_template.call_args_list
        mail_obj_one, mail_obj_two = mail_obj_one[1], mail_obj_two[1]

        assert (mail_obj_one['recipient'] == assignee) or (
            mail_obj_one['recipient'] == assigner)
        assert (mail_obj_two['recipient'] == assignee) or (
            mail_obj_two['recipient'] == assigner)
        assert mail_obj_one[
            'mail_subject'] == new_work_order_with_assigner.title
        assert mail_obj_two[
            'mail_subject'] == new_work_order_with_assigner.title
        assert SendEmail.send_mail_with_template.called
