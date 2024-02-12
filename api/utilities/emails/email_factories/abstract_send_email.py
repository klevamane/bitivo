# Standard
import abc


class AbstractSendEmail(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def send_mail_without_template(cls, recipient, mail_subject, mail_body):
        """Abstract Class Method for sending non-template email using sendgrid API

        Args:
            recipient (str): the receiving email address.
            mail_subject (str): the email subject.
            mail_body (str): the email body.

        """
        pass

    @abc.abstractclassmethod
    def send(cls, mail, trials=6):
        """Abstract Class Method that handles sending mail using SendGrid API

        Args:
            mail (instance): an instance of SendGrid's Mail class.
            trials (int): The maximum number the  email submit resent in case a GatewayTimeoutError is raised.
        """
        pass
