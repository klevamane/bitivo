from unittest.mock import Mock, patch
from datetime import datetime
from bot.utilities.greeting import greeting


@patch('bot.utilities.greeting.datetime')
def test_get_morning_greeting_message_succeeds(mock_datetime):
    """ Tests get morning greeting message"""

    mock_datetime.now = Mock(return_value=datetime(2019, 6, 10, 6))
    greeting_msg = greeting()
    assert greeting_msg == 'Good morning'


@patch('bot.utilities.greeting.datetime')
def test_get_afternoon_greeting_message_succeeds(mock_datetime):
    """ Tests get afternoon greeting message"""

    mock_datetime.now = Mock(return_value=datetime(2019, 6, 10, 14))
    greeting_msg = greeting()
    assert greeting_msg == 'Good afternoon :sunny:'


@patch('bot.utilities.greeting.datetime')
def test_get_evening_greeting_message_succeeds(mock_datetime):
    """ Tests get evening greeting message"""

    mock_datetime.now = Mock(return_value=datetime(2019, 6, 10, 20))
    greeting_msg = greeting()
    assert greeting_msg == 'Good evening'
