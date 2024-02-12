"""Module for testing the send email helper function."""
import pytest
from flask import render_template
from jinja2.exceptions import TemplateNotFound

from api.utilities.emails.email_templates import email_templates
from api.utilities.helpers.get_mailing_params import get_mailing_params
from api.utilities.messages.error_messages import serialization_errors

from main import create_app
from config import AppConfig


class TestSendEmailHelper:
    def test_get_mailing_params_with_correct_sendgrid_data_succeeds(self):
        """Test that getting mailing params with correct sendgrid data passes"""
        AppConfig.MAIL_SERVICE = 'sendgrid'
        mock = email_templates['assign_request_to_technician']
        data = get_mailing_params('assign_request_to_technician',
                                  mock['default_data']['subject'],
                                  mock['default_data'])
        
        assert data['template_id'] == mock['sendgrid']['id']
        assert data['template_data']['username'] == mock['default_data'][
            'username']
        assert data['template_data']['assignee'] == mock['default_data'][
            'assignee']
        assert data['template_data']['subject'] == mock['default_data'][
            'subject']

    def test_get_mailing_params_with_correct_mailgun_data_succeeds(self):
        """Test that getting mailing params with correct mailgun data passes"""
        AppConfig.MAIL_SERVICE = 'mailgun'
        mock = email_templates['assign_request_to_technician']
        with create_app().app_context():
            data = get_mailing_params('assign_request_to_technician',
                                      mock['default_data']['subject'],
                                      mock['default_data'])
            assert data['mail_html_body'] == render_template(
                mock['local']['template'], data=mock['default_data'])
            assert data['mail_subject'] == mock['default_data']['subject']

    def test_get_mailing_params_with_invalid_email_template_key_fails(self):
        """Test that getting mailing params with an email template key
        that does not exist, fails.
        """
        with pytest.raises(KeyError) as error:
            get_mailing_params('-LYkbiRi8um4hraPp2M0', 'subject',
                               {'data': 'default'})
        assert serialization_errors['not_found'].format('Template key') in str(
            error.value)

    def test_get_mailing_params_with_invalid_email_template_fails(self):
        """Test that getting mailing params with an email template
        that does not exist, fails.
        """
        AppConfig.MAIL_SERVICE = 'mailgun'
        email_templates['low_in_stock']['local'][
            'template'] = '/email/-LYkbiRi8um4hraPp2M0.html'
        with create_app().app_context() and \
                pytest.raises(TemplateNotFound) as error:
            get_mailing_params('low_in_stock', 'subject', {'data': 'default'})
        assert serialization_errors['not_found'].format(
            'Email template') in str(error.value)
