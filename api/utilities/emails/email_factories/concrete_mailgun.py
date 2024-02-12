import requests

from api.utilities.emails.email_factories.abstract_send_email import (
    AbstractSendEmail)

# app config
from config import AppConfig


class ConcreteMailgunEmail(AbstractSendEmail):
    MAILGUN_API_KEY = AppConfig.MAILGUN_API_KEY
    MAILGUN_DOMAIN_NAME = AppConfig.MAILGUN_DOMAIN_NAME
    MAILGUN_SENDER = AppConfig.MAILGUN_SENDER
    REQUEST_URL = f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN_NAME}/messages'

    @classmethod
    def send_mail_without_template(cls, recipient, mail_subject, mail_body):
        """Class Method for sending non-template email using Mailgun API

       Args:
           recipient (str): the receiving email address.
           mail_body (str): the email body.
           mail_subject (str): the email subject.

       Returns:
           dict: returns a dictionary id and message on success.
           Bool: returns a boolean False on failure.
       """
        mail = {
            'from': cls.MAILGUN_SENDER,
            'to': recipient,
            'subject': mail_subject,
            'text': mail_body
        }

        return cls.send(mail)

    @classmethod
    def send_mail_with_template(cls,
                                recipient,
                                mail_subject,
                                mail_html_body,
                                attachments=None):
        """Class method for sending template emails using Mailgun API

       Args:
           recipient (str): the receiving email address.
           mail_subject (str): the email subject.
           mail_html_body(str): the email html body.
           attachments(tuple): list of attachments

       Returns:
           dict: returns a dictionary id and message on success.
           Bool: returns a boolean False on failure.
       """

        mail = {
            'from': cls.MAILGUN_SENDER,
            'to': recipient,
            'subject': mail_subject,
            'html': mail_html_body,
        }

        return cls.send(mail, attachments)

    @classmethod
    def send(cls, mail, attachments=None):
        """Class Method that handles sending mail using Mailgun API

        Args:
            mail(dict): a dictionary containing sender,recipient and mail body.
            attachments(tuple) a list of attachments
        Returns:
            dict: returns a dictionary id and message on success.
            Bool: returns a boolean False on failure.
        """
        response = requests.post(
            cls.REQUEST_URL,
            files=attachments,
            auth=('api', cls.MAILGUN_API_KEY),
            data=mail)
        if response.status_code == 200:
            return response.json()
        return False
