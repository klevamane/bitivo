"""Module for sending email using Flask-Mail API"""

# Third-party libraries
from flask import current_app
from flask_mail import Message, Mail

# Utilities
from api.utilities.emails.email_factories.abstract_send_email import AbstractSendEmail

class ConcreteFlaskMail(AbstractSendEmail):
    """Concrete class for sending emails using Flask_Mail"""

    @classmethod
    def send_mail_without_template(cls, recipient, mail_subject, mail_body):
        """Method for sending  email using Flask_Mail API

        Args:
            recipient (str): the recipient address
            mail_subject (str): the email subject.
            mail_body (str): the email body.

        """
        return cls.send({
            'subject': mail_subject,
            'recipient': recipient,
            'body': mail_body
        })

    @classmethod
    def send_mail_with_html_template(cls, recipient, mail_subject, mail_html_body):
        """Method for sending email using with an html using Flask_Mail API

        Args:
            recipient (str): the recipient address
            mail_subject (str): the email subject.
            mail_html_body (str): the string representing the html that is to be passed to the body of the email.

        """

        message = {
            'subject': mail_subject,
            'recipient': recipient,
            'html': mail_html_body
        }

        return cls.send(message)

    @classmethod
    def send(cls, mail):
        """Method that handles sending mail using FlaskMail API

        Args:
            mail (instance): an instance of flask_mail's Message class.
        """
        with current_app.app_context():
            flask_mail = Mail(current_app)

        return flask_mail.send(Message(**mail))
