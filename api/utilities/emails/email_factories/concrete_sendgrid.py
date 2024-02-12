"""Module for sending email using SendGrid API"""

# standard
from python_http_client.exceptions import (
    BadRequestsError, UnauthorizedError, UnsupportedMediaTypeError,
    ForbiddenError, PayloadTooLargeError, InternalServerError,
    GatewayTimeoutError)

# Third Party
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail, Personalization

# Utilities
from api.utilities.emails.email_factories.abstract_send_email import AbstractSendEmail

# App AppConfig
from config import AppConfig


class ConcreteSendGridEmail(AbstractSendEmail):

    SENDGRID_CLIENT = sendgrid.SendGridAPIClient(AppConfig.SENDGRID_API_KEY)
    DEFAULT_SENDER = Email(AppConfig.ACTIVO_MAIL_USERNAME)
    MAX_RESEND_TRIALS = 20

    @classmethod
    def send_mail_without_template(cls, recipient, mail_subject, mail_body):
        """Class Method for sending non-template email using sendgrid API

        Args:
            recipient (str): the receiving email address.
            mail_subject (str): the email subject.
            mail_body (str): the email body.

        Returns:
            dict: returns a dictionary containing status, headers and body  on success.
            Bool: returns a boolean False on failure.
        """

        to_email = Email(recipient)
        subject = mail_subject
        content = Content("text/plain", mail_body)
        mail = Mail(cls.DEFAULT_SENDER, subject, to_email, content)

        return cls.send(mail)

    @classmethod
    def send_mail_with_template(cls, recipient, template_id, template_data):
        """Class method for sending template emails using SendGrid API

       Args:
           recipient (str): the receiving email address.
           template_id (str): the SendGrid transactional template id
           template_data (dict): data to populate the template.

       Returns:
           dict: returns a dictionary containing status, headers and body  on success.
           Bool: returns a boolean False on failure.

       """
        mail = Mail()
        mail.from_email = cls.DEFAULT_SENDER
        mail.template_id = template_id
        p = Personalization()
        p.add_to(Email(recipient))
        p.dynamic_template_data = template_data
        mail.add_personalization(p)

        return cls.send(mail)

    @classmethod
    def send(cls, mail, trials=6):
        """Class Method that handles sending mail using SendGrid API

        Args:
            mail (instance): an instance of SendGrid's Mail class.
            trials (int): The maximum number OF time the email submit resent incase a GatewayTimeoutError is raised.

        Returns:
            dict: returns a dictionary containing status, headers and body  on success.
            Bool: returns a boolean False on failure.

        """
        response = False
        try:
            response = cls.SENDGRID_CLIENT.client.mail.send.post(
                request_body=mail.get())

        except (BadRequestsError, UnauthorizedError, UnsupportedMediaTypeError,
                ForbiddenError, PayloadTooLargeError, InternalServerError):
            pass
        except GatewayTimeoutError:
            if not (0 <= trials <= cls.MAX_RESEND_TRIALS):
                return False
            return cls.send(mail=mail, trials=trials - 1)

        return response
