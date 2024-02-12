"""Module with slack_helper fixtures """

# Third Party Modules
import pytest
from slackclient import SlackClient


@pytest.fixture(scope='function')
def mock_slack_api_call(monkeypatch, new_user):
    """Fixture for monkey patching slack client api call
    Args:
        monkeypatch

    Return: 
        None
    """
    new_user.save()
    slack_response = {
        "MSG": "Make a HotDesk Request:",
        "user": {
            "name": new_user.name,
            "profile": {
                "id": "sampleId",
                "name": new_user.name,
                "email": new_user.email
            }
        }
    }
    monkeypatch.setattr(SlackClient,
                        'api_call', lambda self, arg, **kwargs: slack_response)


@pytest.fixture(scope='function')
def mock_slack_api_call_2(monkeypatch):
    """Fixture for monkey patching slack client api call
    Args:
        monkeypatch

    Return: 
        None
    """
    slack_response = {"user": {"profile": {"email": 'sample@andela.com'}}}
    monkeypatch.setattr(SlackClient,
                        'api_call', lambda self, arg, **kwargs: slack_response)
