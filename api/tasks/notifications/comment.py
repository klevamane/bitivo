"""Send comment emails module"""

# Models
from ...models import User, Request, WorkOrder, Schedule

# Main
from main import celery_app

# App config
from config import AppConfig

# Utilities
from . import SendEmail
from ...utilities.helpers.env_resource_adapter import adapt_resource_to_env
from ...utilities.helpers.get_mailing_params import get_mailing_params


class CommentNotifications:
    """Executes send request type email notifications"""

    @classmethod
    def process_request_comment(cls, comment_instance):
        """ process request comments by sending notification to either
        assignee or assigner or both of them on when request is commented

        Args:
            comment_instance (obj): The current model instance

        """
        # retrieves requester_id, responder_id, and subject from the Request model
        request = Request.get(comment_instance.parent_id)
        requester_id = request.requester_id
        responder_id = request.responder_id
        subject = request.subject

        # gets the author_id of the comment
        author_id = comment_instance.author_id

        recipients_mapper = {
            requester_id: [responder_id],
            responder_id: [requester_id]
        }

        value_data = comment_instance.parent_type.value

        mail_recipient_ids = recipients_mapper.get(
            author_id, [requester_id, responder_id])

        send_notification = adapt_resource_to_env(cls.send_notification.delay)
        for mail_recipient_id in mail_recipient_ids:
            send_notification(subject, mail_recipient_id, author_id,
                              value_data, comment_instance.parent_id)

    @classmethod
    def process_schedule_comment(cls, comment_instance):
        """
            process work order schedule comments by sending notification to either
            assignee or assigner or both of them on when work-order is commented

        Args:
            comment_instance (obj): The current model instance

        """

        schedule = Schedule.get(comment_instance.parent_id)
        assignee = schedule.assignee_id
        work_order_title = WorkOrder.get(schedule.work_order_id).title
        work_order_assigner = WorkOrder.get(schedule.work_order_id).created_by
        author_id = comment_instance.author_id

        recipients_mapper = {
            assignee: [work_order_assigner],
            work_order_assigner: [assignee]
        }
        value = comment_instance.parent_type.value
        comment = comment_instance.body

        mail_recipient_ids = recipients_mapper.get(
            author_id, [assignee, work_order_assigner])
        send_notification = adapt_resource_to_env(cls.send_notification.delay)
        for mail_recipient_id in mail_recipient_ids:

            send_notification(
                work_order_title,
                mail_recipient_id,
                author_id,
                value,
                comment_instance.parent_id,
                comment=comment)

    @classmethod
    def comment_notification_handler(cls, comment_instance):
        """
            Handles notification between `Request` or `Schedule` email notification
             to generate by running a boolean
        Args:
            comment_instance (obj): The current model instance
        Returns:
                func: with condition to return either `process_request_comment
                        or `process_schedule_comment`

        """
        if comment_instance.parent_type.value == 'Request':
            return cls.process_request_comment(comment_instance)
        elif comment_instance.parent_type.value == 'Schedule':
            return cls.process_schedule_comment(comment_instance)

    @staticmethod
    @celery_app.task(name="comment_notifier")
    def send_notification(*args, **kwargs):
        """Send comment email notifications

            Args:
                subject (str): The request subject
                recipient_id (str): The id of the recipient that would receive
                    the email
                author_id (str): The id of the author of the comment
                instance_value(str): parent_type value
                comment(str): comment message
                comment_id(str):The request id

            Returns:
                None

        """
        comment = kwargs.pop('comment', None)
        subject, recipient_id, author_id, instance_value, request_id = args
        [recipient_email, recipient_name] = \
            User.query_().filter_by(token_id=recipient_id).with_entities(
                User.email, User.name).first()
        [author] = User.query_().filter_by(token_id=author_id)\
            .with_entities(User.name).first()

        if instance_value == 'Schedule':
            template_data = {
                'recipient': recipient_name,
                "sender": author,
                "work_order": subject,
                "comment": comment,
                'domain': AppConfig.DOMAIN
            }
            params = get_mailing_params(
                'notify_assignee_or_assigner_on_comment', subject,
                template_data)

        elif instance_value == 'Request':
            template_data = {
                'username': recipient_name,
                'assignee': author,
                'subject': subject,
                'id': request_id,
                'domain': AppConfig.DOMAIN
            }
            params = get_mailing_params('request_comment', subject,
                                        template_data)

        params = dict(recipient=recipient_email, **params)

        SendEmail.send_mail_with_template(**params)
