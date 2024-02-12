"""Module for handling sending of emails"""
# Third-party libraries
from flask_mail import Message

# Application instance
from manage import mail, app

# Celery
from main import celery_app


class Email():
    """Class for sending emails"""

    @staticmethod
    @celery_app.task(name='send_smtp_email')
    def send_mail(title, recipients, body, attachment_data={}):
        """Sends an email using smtp.gmail.com mail server
        Args:
            title (str): Title of the email to be sent
            recipients (list): A list containing the emails of recipients
            body (string): The body of the mail to be sent
            error (bool): The type of mail to send (success or error)
            attachment_data (dict): A dict with a StringIO object and a filename
        Raises:
            ValidationError: exception raised if email sending fails
        """
        with app.app_context():
            message = Message(title, recipients=recipients, body=body)
            Email.process_file(attachment_data, message)
            mail.send(message)

    def attach_file(attachment, message):
        """Attaches file(s) to the emails to be sent
        Args:
            attachment_data (dict/list/tuple): An object with a StringIO object and a filename
        Returns:
            None
        """
        file, file_name = attachment.get('file'), attachment.get('name')
        file_type = file_name.split('.')[-1]
        message.attach(file_name, f'application/{file_type}', file.getvalue())
        file.close()

    def is_list_or_tuple(attachment_data):
        """checks if attachment_data is a list or a tuple
        Args:
            attachment_data (dict/list/tuple): An object with a StringIO object and a filename
        Returns:
            bool
        """

        return isinstance(attachment_data, list) or isinstance(
            attachment_data, tuple)

    def process_file(attachment_data, message):
        """Processes the attachment
        Args:
            attachment_data (dict/list/tuple): An object with a StringIO object and a filename
            message (list): A list containing the emails of recipients
        """

        if attachment_data:
            if not Email.is_list_or_tuple(attachment_data):
                attachment_data = (attachment_data, )
            for attachment in attachment_data:
                Email.attach_file(attachment, message)
