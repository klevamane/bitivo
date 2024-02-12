# Utilities
from .abstract_send_email import AbstractSendEmail
from .concrete_sendgrid import ConcreteSendGridEmail
from .concrete_flask_mail import ConcreteFlaskMail
from .concrete_mailgun import ConcreteMailgunEmail

CONCRETE_EMAIL_SENDER_MAPPER = {
    'sendgrid': ConcreteSendGridEmail,
    'flask-mail': ConcreteFlaskMail,
    'mailgun': ConcreteMailgunEmail
}


def build_email_sender(sender):
    """Function used to build email sender class from concrete classes

    Args:
        sender (str): a string representing the concrete class
    """

    concrete_email_sender_class = CONCRETE_EMAIL_SENDER_MAPPER.get(
        str(sender).lower())

    if not concrete_email_sender_class:
        raise NotImplementedError(
            f'You must implement the {sender} concrete class or choose one of the following {[concrete_class for concrete_class in CONCRETE_EMAIL_SENDER_MAPPER]}'
        )

    try:
        if not isinstance(concrete_email_sender_class(), AbstractSendEmail):
            raise Exception(
                f'{sender} concrete class must inherit from  AbstractSendEmail'
            )
    except TypeError:
        raise Exception(
            f'{sender} object of type {type(concrete_email_sender_class)} is not callable'
        )

    return concrete_email_sender_class
