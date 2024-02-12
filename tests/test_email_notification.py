# System libraries
from unittest.mock import patch, Mock
from python_http_client import UnauthorizedError, GatewayTimeoutError

# Third Party Libraries
import sendgrid
import pytest


# Services
from api.services.email_notification import low_asset_count_notifier, SendEmail

# Utilities
from api.utilities.emails.email_factories.concrete_sendgrid import ConcreteSendGridEmail
from api.utilities.emails.email_factories.concrete_flask_mail import ConcreteFlaskMail
from api.utilities.emails.email_factories.abstract_send_email import AbstractSendEmail
from api.utilities.emails.email_factories.send_email_builder import build_email_sender
from api.utilities.enums import AssetStatus

# mock data
from tests.mocks.email import Error

# app config
from config import AppConfig


@patch(
    "api.services.email_notification.SendEmail"
)
class TestLowAssetCountNotifier:
    """Test email notifications"""

    def test_email_notification_with_no_user_fails(self, test_mock,
                                                   init_db, new_roles):
        """Test that notification fails when no user has Ops Associate role

        Args:
            test_mock(MagicMock): A mailgun mock instance
            init_db(SQLAlchemy): fixture to initialize the test database
            new_roles(Role) : Fixture for creating new roles
        """
        new_roles[-2].save()
        response = low_asset_count_notifier()

        assert response == False

    def test_email_notification_low_in_stock_with_user_succeds(
            self, test_mock, init_db, new_test_user, new_asset_category,
            asset_with_attrs):
        """Test email notification succeeds when an asset count is low in stock

        Args:
            test_mock(MagicMock): A mailgun mock instance
            init_db(SQLAlchemy): fixture to initialize the test database
            new_test_user(User): fixture for creating a new user with Ops Associate role
            new_asset_category(AssetCategory): fixture for creating a new asset category
            asset_with_attrs(Asset): fixture for creating asset with attributes

        """
        AppConfig.MAIL_SERVICE = 'mailgun'
        new_asset_category.save()

        new_test_user.save()

        asset_with_attrs.save()

        response = low_asset_count_notifier()

        assert response == True

    def test_email_notification_running_low_with_user_succeds(
            self, test_mock, init_db, new_test_user, new_asset_category,
            asset_with_attrs):
        """Test email notification succeeds when an asset count is running low
         Args:
            test_mock(MagicMock): A mailgun mock instance
            init_db(SQLAlchemy): fixture to initialize the test database
            new_test_user(User): fixture for creating a new user with Ops Associate role
            new_asset_category(AssetCategory): fixture for creating a new asset category
            asset_with_attrs(Asset): fixture for creating asset with attributes
         """
        AppConfig.MAIL_SERVICE = 'mailgun'
        with patch("api.services.email_notification.asset_counter"
                   ) as mock_asset_counter:
            mock_asset_counter.return_value = [('asset_category_name', 50, 25,
                                                30)]
            new_asset_category.save()
            new_test_user.save()
            asset_with_attrs.save()
            response = low_asset_count_notifier()
            assert response == True


    #  The test_send_email_notification_low_stock_successfully test is commented out because
    # the stock level notification mail feature has currently
    # been disabled as a request by the Operations Associate team

    def test_send_email_notification_low_stock_successfully(self, test_mock, init_db, new_test_user, new_asset_category, asset_with_attrs):
        """Test sends email notification successfully when asset count is low in stock
        Args:
            test_mock(MagicMock): A mailgun mock instance
            init_db(SQLAlchemy): fixture to initialize the test database
            new_test_user(User): fixture for creating a new user with Ops Associate role
            new_asset_category(AssetCategory): fixture for creating a new asset category
            asset_with_attrs(Asset): fixture for creating asset with attributes
        """
        new_asset_category.save()
        new_test_user.save()
        asset_with_attrs.save()
        AppConfig.MAIL_SERVICE = 'mailgun'
        response = low_asset_count_notifier()

        # template_data = test_mock.send_mail_with_template.call_args[1]

        # assert test_mock.send_mail_with_template.called
        # assert template_data['recipient'] == new_test_user.email
        # assert template_data['mail_subject'] == f"{new_asset_category.name} is low in stock"
        # assert template_data['mail_html_body']
        assert response


@patch(
    "api.utilities.emails.email_factories.concrete_sendgrid.ConcreteSendGridEmail.SENDGRID_CLIENT"
)
class TestSendEmail:
    """Test sending email"""

    def test_sendemail_without_template_succeeds(self, mock_send_mail):
        """Test sending email without temaplate succeeds

        Args:
            mock_send_mail(MagicMock): A sendgrid mock instance

        """

        mock_send_mail.client.mail.send.post.return_value = True

        response = ConcreteSendGridEmail.send_mail_without_template(
            recipient='test@email.com',
            mail_subject='test subject',
            mail_body='test body')

        assert response == True

    def test_sendemail_with_invalid_api_key_fails(self, mock_send_mail):
        """Test sending email with invalid api key fails

        Args:
            mock_send_mail(MagicMock): A sendgrid mock instance
        """

        mock_send_mail.client.mail.send.post.side_effect = UnauthorizedError(
            Error())

        response = ConcreteSendGridEmail.send(sendgrid.helpers.mail.Mail())

        assert response == False

    def test_sendemail_with_gatewate_timeout_error_fails(self, mock_send_mail):
        """Test during sending email if a GateWayTimeOutError is raised, email sending fails

        Args:
            mock_send_mail(MagicMock): A sendgrid mock instance
        """

        mock_send_mail.client.mail.send.post.side_effect = GatewayTimeoutError(
            Error())

        response = ConcreteSendGridEmail.send(sendgrid.helpers.mail.Mail())

        assert response == False


class TestFlaskMailConcreteClass:
    """Test sending mail using Flask-mail API"""

    @patch(
        "api.utilities.emails.email_factories.concrete_flask_mail.ConcreteFlaskMail.send"
    )
    def test_sendemail_without_template_succeeds(self, mock_send_mail):
        """Test sending email without template succeeds

        Args:
            mock_send_mail(MagicMock): A sendgrid mock instance

        """
        mock_send_mail.return_value = True

        response = ConcreteFlaskMail.send_mail_without_template(
            recipient='test@gmail.com',
            mail_subject='test subject',
            mail_body='test body')
        assert response == True

    @patch(
        "api.utilities.emails.email_factories.concrete_flask_mail.ConcreteFlaskMail.send"
    )
    def test_sendemail_with_html_template_succeeds(self, mock_send_mail):
        """Test sending email without template succeeds

        Args:
            mock_send_mail(MagicMock): A sendgrid mock instance

        """
        mock_send_mail.return_value = True

        response = ConcreteFlaskMail.send_mail_with_html_template(
            recipient='test@gmail.com',
            mail_subject='test subject',
            mail_html_body='<div style="color:red"><b>test body</b></div>')
        assert response == True

    @patch(
        "flask_mail.Mail.send"
    )
    def test_send_mail_succeeds(self, mock_send_mail):
        """Test sending mail using FlaskMail succeeds

        Args:
            mock_send_mail(MagicMock): A sendgrid mock instance

        """
        mock_send_mail.return_value = True
        response = ConcreteFlaskMail.send({})

        assert response == True


class TestAbstractSendMail:
    """Tests the AbstractSendEmail class"""

    def test_creates_concrete_send_mail_succeeds(self):
        """Tests that using the AbstractSendEmail succeeds without throwing exceptions"""

        AbstractSendEmail.send_mail_without_template(
            'recipient', 'mail_subject', 'mail_body')
        AbstractSendEmail.send('test')

        assert True

    def test_create_concrete_sendmail_without_overriding_base_implementation_fails(
            self):
        """Tests creating a concrete class from  AbstractSendEmail class without overriding the abstract methods fails"""

        class TestConcrete(AbstractSendEmail):
            pass

        with pytest.raises(TypeError):
            TestConcrete()


class TestSendEmailBuilder:
    """Tests the build_email_sender function"""

    def test_email_builder_with_improper_base_class_fails(self):
        """Tests that building a concrete class not inherited from AbstractSendEmail class fails"""
        with patch.dict(
            "api.utilities.emails.email_factories.send_email_builder.CONCRETE_EMAIL_SENDER_MAPPER",
                {'test': list}):

            with pytest.raises(Exception):
                build_email_sender('test')

    def test_email_builder_with_non_callable_object_fails(self):
        """Tests that building a concrete class not inherited from AbstractSendEmail class fails"""
        with patch.dict(
            "api.utilities.emails.email_factories.send_email_builder.CONCRETE_EMAIL_SENDER_MAPPER",
                {'test': 'non-callable'}):

            with pytest.raises(Exception):
                build_email_sender('test')

    def test_email_builder_with_no_matching_concrete_class_fails(self):
        """Tests that if no matching concrete class is found, building fails"""

        with pytest.raises(NotImplementedError):
            build_email_sender('test')


class TestNotificationAssetStatuses:
    """Tests that the AssetStatus has not been modified"""

    def test_notification_asset_statuses_exist_succeeds(self):
        """Tests that the INVENTORY, OK_IN_STORE and AVAILABLE statuses are in the AssetStatus"""
        assert AssetStatus.INVENTORY in AssetStatus
        assert AssetStatus.OK_IN_STORE in AssetStatus
        assert AssetStatus.AVAILABLE in AssetStatus
