# System libraries
from unittest.mock import patch

# Utilities
from api.utilities.emails.email_factories.concrete_mailgun import ConcreteMailgunEmail


@patch(
    "requests.post"
)
class TestSendEmailMailgun:
    """Test sending email"""

    def test_sendemail_without_template_succeeds(self, mock_requests):
        """Test sending email without template succeeds

        Args:
            mock_requests(MagicMock): A requests.post mock instance

        """
        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = {
            'id': 'mail_id', 'message': 'Queued. Thank you.'}

        response = ConcreteMailgunEmail.send_mail_without_template(
            recipient='test@email.com',
            mail_subject='test subject',
            mail_body='test body')

        assert response['id'] == 'mail_id'
        assert response['message'] == 'Queued. Thank you.'

    def test_sendemail_with_template_succeeds(self, mock_requests):
        """Test sending email with template succeeds

        Args:
            mock_requests(MagicMock): A requests.post mock instance

        """
        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = {
            'id': 'mail_id', 'message': 'Queued. Thank you.'}

        response = ConcreteMailgunEmail.send_mail_with_template(
            recipient='test@email.com',
            mail_subject='test subject',
            mail_html_body='<html><body>Mail body</body></html>')

        assert response['id'] == 'mail_id'
        assert response['message'] == 'Queued. Thank you.'

    def test_sendemail_fails(self, mock_requests):
        """Test sending email with invalid API key

        Args:
            mock_requests(MagicMock): A requests.post mock instance
        """

        mock_requests.return_value.status_code = 401

        response = ConcreteMailgunEmail.send_mail_without_template(
            recipient='test@email.com',
            mail_subject='test subject',
            mail_body='test body')

        assert response == False
