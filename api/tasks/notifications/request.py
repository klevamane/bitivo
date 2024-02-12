"""Module for request category assignee email notifications"""
# Celery
from main import celery_app

# Sendgrid
from . import SendEmail

# SQLAlchemy
from sqlalchemy.orm.attributes import get_history

# models
from api.models import Request, User

# App config
from config import AppConfig

# utilities
from api.utilities.emails.email_templates import email_templates
from api.utilities.enums import RequestStatusEnum
from api.utilities.helpers.env_resource_adapter import adapt_resource_to_env
from api.utilities.constants import YOU, ACTIVO_SYSTEM
from ...utilities.helpers.get_mailing_params import get_mailing_params

# Enum
from api.utilities.enums import RequestStatusEnum


class RequestNotifications:
    """Executes email notification for requests"""

    @staticmethod
    @celery_app.task(name='request_category_assignee')
    def notify_request_type_assignee(*args):
        """sends email notification to a request type assignee.

         Args:
            *args:
                request_type_id (string): The request type id
                requester_id (string): The requester id

         Returns:
            None
         """

        request_id, requester_id = args

        # get the requester's name through the requester's id
        requester = User.get(requester_id).name

        # get the request's details
        request = Request.get(request_id)

        # get assignee email and name
        assignee_email = request.responder.email
        assignee_name = request.responder.name

        # create a dictionary of variables and get mailing parameters.
        data = {
            'assignee_name': assignee_name,
            'request_category_name': request.request_type.title,
            'requester': requester,
            'id': request_id,
            'domain': AppConfig.DOMAIN
        }

        params = get_mailing_params('logged_category_request',
                                    data["request_category_name"], data)

        params = dict(recipient=assignee_email, **params)

        SendEmail.send_mail_with_template(**params)

    @classmethod
    def notify_request_type_assignee_handler(cls, request):
        """Method that handles sending email notifications
         to the request_type_assignee

        Args:
            request (obj): An instance of the Request model

        Returns:
            None
        """

        # set the requester_id and request_id
        requester_id = request.requester_id
        request_id = request.id
        notify_assignee = adapt_resource_to_env(
            RequestNotifications.notify_request_type_assignee.delay)
        notify_assignee(request_id, requester_id)

    @celery_app.task(name='notify_technician')
    def notify_technician(*args):
        """Sends email notification to a technician. 

            Args:
               *args:
                  technician_name (string): The name of the technician 
                  technician_email (string): The technician email
                  responder_name (string): The request type assignee name
                  request_subject (string): The request subject
                     
            Returns:
               None
            """

        technician_name, technician_email, responder_name, request_subject, request_id = args

        data = {
            'username': technician_name,
            'assignee': responder_name,
            'subject': request_subject,
            'id': request_id,
            'domain': AppConfig.DOMAIN
        }

        params = get_mailing_params('assign_request_to_technician',
                                    request_subject, data)

        params = dict(recipient=technician_email, **params)

        SendEmail.send_mail_with_template(**params)

    @classmethod
    def notify_technician_handler(cls, request):
        """The event handler for notifying a technician.

         Args:
            request (obj): An instance of the Request model

         Returns:
            None
         """
        assignee_id_changed = get_history(request, 'assignee_id')[0]

        technician = request.assignee
        if technician and assignee_id_changed:
            notify_technician = adapt_resource_to_env(
                cls.notify_technician.delay)
            notify_technician(technician.name, technician.email,
                              request.responder.name, request.subject,
                              request.id)

    @classmethod
    def get_request_template_key(cls, status):
        return 'closed_by_system' if status else 'requester_status'

    @staticmethod
    @celery_app.task(name='status_report')
    def requester_status(*args):
        """sends email notification to a requester when request status changes.

        Args:
            *args:
                closed_by_system(bool): If the request is closed by the system
                status(str): The request status
                subject(str): The request subject title
                responder_name (str): The responder id
                requester_name (str): The requester name
                requester_email (str): The requester email

        Returns:
            None
        """
        closed_by_system, status, subject, responder_name, requester_name, requester_email, request_id = args

        assignee = None
        auto_closed = False

        if status == RequestStatusEnum.in_progress or status == RequestStatusEnum.completed:
            assignee = responder_name
        elif status == RequestStatusEnum.closed and closed_by_system:
            assignee = ACTIVO_SYSTEM
            auto_closed = True
        elif status == RequestStatusEnum.closed:
            assignee = YOU

        data = {
            'username': requester_name,
            'assignee': assignee,
            'subject': subject,
            'status': status,
            'id': request_id,
            'domain': AppConfig.DOMAIN
        }

        params = get_mailing_params(
            RequestNotifications.get_request_template_key(auto_closed),
            subject, data)

        params = dict(recipient=requester_email, **params)

        SendEmail.send_mail_with_template(**params)

    @classmethod
    def status_change_handler(cls, request):
        """The event handler status change.
         Args:
            request (obj): An instance of the Request model
         Returns:
            None
        """
        new_status = request.status
        closed_by_system = request.closed_by_system
        old_status = request._old_status
        in_progress = RequestStatusEnum.in_progress.value
        completed = RequestStatusEnum.completed.value
        closed = RequestStatusEnum.closed.value
        already_in_progress = new_status == in_progress and new_status != old_status
        already_completed = new_status == completed and new_status != old_status
        already_closed = new_status == closed and new_status != old_status
        already_closed_by_requester = already_closed and not closed_by_system
        already_closed_by_system = already_closed and closed_by_system
        if already_in_progress or already_completed or already_closed_by_requester or already_closed_by_system:
            requester_status_func = adapt_resource_to_env(
                cls.requester_status.delay)
            requester_status_func(request.closed_by_system, request.status,
                                  request.subject, request.responder.name,
                                  request.requester.name,
                                  request.requester.email, request.id)
