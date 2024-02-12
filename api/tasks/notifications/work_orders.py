"""Module for work order assignee email notifications"""

# Models
from api.models import User

# Celery
from main import celery_app

# App config
from config import AppConfig

# SQLAlchemy
from sqlalchemy.orm.attributes import get_history

# Utilities
from api.utilities.emails.email_templates import email_templates
from api.utilities.helpers.env_resource_adapter import adapt_resource_to_env
from ...utilities.helpers.get_mailing_params import get_mailing_params

# SenGrid
from . import SendEmail


class WorkOrderNotifications:
    """Executes email notification for work orders"""

    @staticmethod
    @celery_app.task(name='work_orders_assignee')
    def notify_assignee_work_order(details):
        """sends email notification to an assignee.

        Args:
            assignee_id (str): The id of the assignee
            assigner_id (str): The id of the sender
            workorder_title (str): work order title

        Returns:
            None
        """

        # get the assigner's name
        assigner = User.get(details["created_by"])
        assigner_name = assigner.name

        # checks if the work order has been updated
        if details["updated_by"]:
            assigner_name = User.get(details["updated_by"]).name

        # get the assignee's details through the id provided
        assignee = User.get(details["assignee_id"])
        assignee_name = assignee.name
        assignee_email = assignee.email

        # create a dictionary of variables and get mailing parameters.
        data = {
            'username': assignee_name,
            'workOrder': details["title"],
            'assignerName': assigner_name
        }

        if details["old_assignee"] and details["new_assignee"] != details[
                "old_assignee"]:

            old_assignee = User.get(details["old_assignee"][0])
            reassign_data = {
                "username": old_assignee.name,
                "newAssignee": assignee_name,
                "workOrderTitle": details["title"],
                "domain": AppConfig.DOMAIN
            }
            reassign_params = get_mailing_params(
                'reassignee_work_order', details["title"], reassign_data)
            reassign_params = dict(
                recipient=old_assignee.email, **reassign_params)
            SendEmail.send_mail_with_template(**reassign_params)

        params = get_mailing_params('notify_assignee_work_order',
                                    details["title"], data)
        params = dict(recipient=assignee_email, **params)
        SendEmail.send_mail_with_template(**params)

    @classmethod
    def notify_assignee_handler(cls, target):
        """Method that handles sending email notifications
        to the assignee

        Args:
            target (obj): An instance of the work order model

        Returns:
            None
        """
        # gets history of work order assignee
        assignee_id_history = get_history(target, 'assignee_id')
        new_assignee = assignee_id_history[0]
        old_assignee = assignee_id_history[2]

        # gets details of the work order
        details = {
            "created_by": target.created_by,
            "title": target.title,
            "assignee_id": target.assignee_id,
            "updated_by": target.updated_by,
            "new_assignee": new_assignee,
            "old_assignee": old_assignee
        }

        if details["created_by"]:
            send_notify_work_order = adapt_resource_to_env(
                WorkOrderNotifications.notify_assignee_work_order.delay)
            send_notify_work_order(details)
