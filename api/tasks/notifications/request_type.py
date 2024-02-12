"""Request email notifications module"""

# Third Party
from sqlalchemy.orm.attributes import get_history

# Main
from main import celery_app

#App config
from config import AppConfig

# Models
from api.models import User

# Utilities
from api.utilities.helpers.env_resource_adapter import adapt_resource_to_env
from ...utilities.helpers.get_mailing_params import get_mailing_params

from . import SendEmail


class RequestTypeNotification:
    """Executes request email notifications"""

    @staticmethod
    def request_type_notifier_handler(target):
        """Handler that runs when a new requestType is updated or inserted

        It processes the added row and sends a notification to  the assignee
        of the RequestType if the value exists

        Args:
            target(RequestType): the requesttype

        """

        # Checks for any changes in the assignee_id value
        new_value, _, old_value = get_history(target, 'assignee_id')
        assigner_id = target.updated_by if len(
            old_value) != 0 else target.created_by

        # The following block runs only if 'assignee_id' is newly added or updated
        assignee = target.assignee

        if assignee and new_value and assigner_id:
            request_type_notifier = adapt_resource_to_env(
                RequestTypeNotification.send_request_type_email.delay)

            assignee_email = assignee.email
            assignee_name = assignee.name
            request_type_title = target.title
            request_type_notifier(request_type_title, assignee_email,
                                  assignee_name, assigner_id)

    @staticmethod
    @celery_app.task(name='send_request_type_email')
    def send_request_type_email(title, assignee_email, assignee_name,
                                assigner_id):
        """Send request type email notifications.

        Sends the user that was assigned the RequestType a notification
        using the RequestType title and the user details

        Args:
            title(str): the title of the RequestType
            assignee_email(str): the email of the assignee
            assignee_name(str): the name of the assignee
            assigner_id(str): the token_id of the user that updated or created the request_type

        Returns:
            None
        """
        assigner = User.get(assigner_id)

        if assigner and assigner.email != assignee_email:

            template_data = {
                'username': assignee_name,
                'request_category_name': title,
                'user': assigner.name,
                'domain': AppConfig.DOMAIN
            }

            params = get_mailing_params('request_type_assigned',
                                        template_data['request_category_name'],
                                        template_data)

            params = dict(recipient=assignee_email, **params)

            SendEmail.send_mail_with_template(**params)
