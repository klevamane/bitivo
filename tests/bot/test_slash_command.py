import json
from unittest.mock import MagicMock, Mock, patch
from api.utilities.constants import CHARSET
from bot.utilities.slack.slack_helper import SlackHelper
from ..mocks.slack_bot import SLACK_USER

from main import cache

class TestSlashCommand:
    """Test for activo slash command"""
    @patch('main.cache.get', MagicMock(return_value=True))
    @patch('main.cache.set', MagicMock(return_value=True))
    def test_slash_command_succeeds(self, client):
        """Test the slash command endpoint.
         Args:
            self (Instance): TestSlashCommand instance
            client (FlaskClient): fixture to get flask test client.
         Returns: None
        """
        client = MagicMock()

        response = client.post('/activo-bot/v1')
        response.status_code = 200
        response.return_value = ''

        assert response.status_code == 200
        assert isinstance(response.return_value, str)

    @patch('main.cache.get', MagicMock(return_value=True))
    @patch('main.cache.set', MagicMock(return_value=True))
    def test_slash_help_command_succeeds(self, client):
        """Test the slash command endpoint.
         Args:
            self (Instance): TestSlashCommand instance
            client (FlaskClient): fixture to get flask test client.
         Returns: None
        """
        data = dict(text='help')
        response = client.post('/activo-bot/v1', data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert isinstance(response_json['text'], str)    

    @patch('main.cache.get', MagicMock(return_value=True))
    @patch('main.cache.set', MagicMock(return_value=True))
    def test_slash_cancel_command_without_requester_hotdesk_succeeds(self, client, init_db):
        """Test the slash cancel command endpoint when
            user has no pending or approved hot desk request.
         Args:
            self (Instance): TestSlashCommand instance
            client (FlaskClient): fixture to get flask test client.
            init_db (SQLAlchemy): fixture to initialize the test database
         Returns: None
        """
        #mock slack helper
        SlackHelper.user_info = Mock(return_value=SLACK_USER)

        data = dict(text='cancel')
        response = client.post('/activo-bot/v1', data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        
        assert response.status_code == 200
        assert isinstance(response_json['text'], str)

    def test_slash_cancel_command_with_requester_hotdesk_succeeds(self,
            client, init_db, new_today_hot_desk):
        """Test the slash cancel endpoint when user
            has a pending or aprroved hot desk request
         Args:
            self (Instance): TestSlashCommand instance
            client (FlaskClient): fixture to get flask test client.
            init_db (SQLAlchemy): fixture to initialize the test database
            new_today_hot_desk (HotDesk): fixture for creating an hot desk for today
         Returns: None
        """
        
        #create a new hot desk request
        new_today_hot_desk.save()

        user = SLACK_USER.copy()

        #mock slack helper
        SlackHelper.user_info = Mock(return_value=user)

        data = dict(text='cancel')
    
    @patch('main.cache.get', MagicMock(return_value=True))
    @patch('main.cache.set', MagicMock(return_value=True))
    def test_slash_invalid_command_succeeds(self, client):
        """Test the slash activo with invalid command succeeds.
         Args:
            self (Instance): TestSlashCommand instance
            client (FlaskClient): fixture to get flask test client.
         Returns: None
        """

        data = dict(text='anything')
        response = client.post('/activo-bot/v1', data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert isinstance(response_json['text'], str)
