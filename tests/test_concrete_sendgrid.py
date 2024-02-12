from api.utilities.emails.email_factories.concrete_sendgrid import ConcreteSendGridEmail
from sendgrid.helpers.mail import Mail
from unittest.mock import Mock, patch



class TestConcreteSendGridEmail:
    def test_send_mail_with_template_method_succeeds(self, mock_sendgrid_send_call,
                                                     init_db):
        """Should call the send method

        Args:
            mock_sendgrid_send_call(fixture): the mocked version of the send method
            init_db(fixture): to initialise db

        """
        recipient = "mock_recipient@email.com"
        template_id = "mock_template_id"
        template_data = {'first_name': 'unknown', 'last_name': 'your_name'}
        
        output = ConcreteSendGridEmail.send_mail_with_template(recipient, template_id,
                                                      template_data)
        assert output.status_code == 202
