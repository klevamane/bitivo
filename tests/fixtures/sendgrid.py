"""Module with slack_helper fixtures """

# Third Party Modules
import pytest
from slackclient import SlackClient
from api.utilities.emails.email_factories.concrete_sendgrid import ConcreteSendGridEmail
from collections import namedtuple

@pytest.fixture(scope='function')
def mock_sendgrid_send_call(monkeypatch):
    """Fixture for monkey patching sendgrid send metho
    Args:
        monkeypatch

    Return: 
        None
    """
    response_dict = dict(status_code=202)
    response = namedtuple("SendGrid", response_dict.keys())(*response_dict.values())

    monkeypatch.setattr(ConcreteSendGridEmail,
                        'send', lambda self, **kwargs: response)
