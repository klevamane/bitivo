# System libraries

from flask import render_template
from jinja2.exceptions import TemplateNotFound

from ..messages.error_messages import serialization_errors
from ..emails.email_templates import email_templates
from ..emails.hot_desk_email_template import hot_desk_email_template

from config import AppConfig


def get_mailing_params(template_key, subject, data, template='general_template'):
    """The function constructs and returns mailing parameters based on the email
    service that will be used to send the email.

    Args:
        template_key (str): the dictionary key that holds the email template to be used
        subject (str): the subject of the email
        data (obj): the dynamic data needed to customise the email
        template(str): the template to use
                    
    Returns:
        dict: email parameters that can be passed to the email service
    """

    all_templates = {
        'general_template': email_templates,
        'hot_desk_email_template': hot_desk_email_template,
    }
    main_email_template = all_templates.get(template)
    if not main_email_template.get(template_key, None):
        raise KeyError(
            serialization_errors['not_found'].format('Template key'))

    if AppConfig.MAIL_SERVICE == 'sendgrid':
        template_id = main_email_template[template_key]['sendgrid']['id']
        return dict(template_id=template_id, template_data=data)

    try:
        html_template = render_template(
            main_email_template[template_key]['local']['template'], data=data)
    except Exception:
        raise TemplateNotFound(
            serialization_errors['not_found'].format('Email template'))
    return dict(mail_subject=subject, mail_html_body=html_template)
