"""Module for request category assignee email notifications"""
# Celery
from main import celery_app

# App Config
from config import AppConfig

# SQLAlchemy
from sqlalchemy.orm.attributes import get_history

# models
from api.models import User, Schedule, WorkOrder

# utilities
from . import SendEmail
from api.utilities.helpers.env_resource_adapter import adapt_resource_to_env
from ...utilities.helpers.get_mailing_params import get_mailing_params

# Enum
from api.utilities.enums import ScheduleStatusEnum


class SchedulesNotifications:
    """Executes email notification for schedules"""

    @classmethod
    def schedule_status_notification_handler(cls, schedule_instance):
        """Sends notification to required user(s)

        This function uses the schedule work order instance to send an email to the requester, 
        reponder or both  when a status changes to done.

        Args:
            schedule_instance(obj): Object of the schedule model 

        Return:
            None
        """
        # Gets assigner id, assignee id and work order id from the schedule model
        assigner_id = schedule_instance.created_by
        if assigner_id:
            assignee_id = schedule_instance.assignee_id
            work_order_id = schedule_instance.work_order_id

            notify_assigner = adapt_resource_to_env(
                SchedulesNotifications.send_work_order_notification.delay)
            notify_assigner(assigner_id, assignee_id, work_order_id)

    @staticmethod
    @celery_app.task(name='notify_assigner_work_order_completed')
    def send_work_order_notification(assigner_id, assignee_id, work_order_id):
        """sends email notification to a requester when work order status changes to done.

        Args:
            *args
                assigner_id(str): The assignerID for the work order schedule
                assignee_id (str): The assigneeID for the work order schedule
                work_order_id (str): The work_order_id for the work order schedule

        Returns:
            None
        """

        assigner_name = User.get(assigner_id).name
        assigner_email = User.get(assigner_id).email

        work_order = WorkOrder.get(work_order_id).title

        assignee = User.get(assignee_id).name

        data = {
            'assigner_name': assigner_name,
            'assignee_name': assignee,
            'work_order': work_order,
            'domain': AppConfig.DOMAIN
        }

        params = get_mailing_params('notify_assigner_work_order_complete',
                                    work_order, data)

        params = dict(recipient=assigner_email, **params)

        SendEmail.send_mail_with_template(**params)
