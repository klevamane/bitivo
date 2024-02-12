
#pytest
from unittest.mock import MagicMock, patch, Mock

# redis cache
from main import cache

# mock
from tests.mocks.slack_bot import SLACK_USER, ACTIONS, APPROVAL_RESPONSE_WITH_ID, APPROVAL_RESPONSE

#local imports
from bot.utilities.slack.slack_helper import SlackHelper
from bot.utilities.user_hot_desk import get_pending_or_approved_hot_desk
from bot.utilities.helpers.bot_helpers import (update_approval_response_on_cancel, 
    store_approval_response, remove_approval_response, process_dialog_error_data)
from bot.utilities.dialog_serialization_errors import BOT_DIALOG_ERROR

class TestBotHelper:

    @patch('main.cache.get', MagicMock(return_value=False))
    @patch('main.cache.set', MagicMock(return_value=True))
    def test_store_approval_response(self):

        """ tests the method that stores the approve response
        """
        user_id = SLACK_USER['profile']['email']
        response = APPROVAL_RESPONSE
        cache.set = Mock()
        store_approval_response(user_id, response)
        assert cache.set.called

    @patch(
        'bot.utilities.helpers.bot_helpers.remove_approval_response',
        MagicMock(return_value=True)
        )
    @patch('main.cache.get', MagicMock(return_value=APPROVAL_RESPONSE_WITH_ID))
    @patch('main.cache.set', MagicMock(return_value=True))
    @patch('bot.utilities.slack.slack_helper.SlackHelper.update_message_to_user')
    def test_update_approval_response_on_cancel(self, ACTIONS, init_db, new_user, new_today_hot_desk):
        """ tests the method that update the assignee message when
            a user cancel hot desk
            Args:
                ACTIONS: mock to assert that the update_message_to_user was called
                init_db (SQLAlchemy): fixture to initialize the test database
                new_today_hot_desk (HotDesk): fixture for creating an hot desk
                new_user(User): Fixture for creating the requester
        """
        new_today_hot_desk.save()
        email = new_user.email
        hot_desk = get_pending_or_approved_hot_desk(email)
        user_id = SLACK_USER['profile']['email']
        hot_desk['id'] = user_id
        update_approval_response_on_cancel(hot_desk)

        assert ACTIONS.called

    @patch('main.cache.get', MagicMock(return_value=APPROVAL_RESPONSE_WITH_ID))
    @patch('main.cache.set', MagicMock(return_value=True))
    def test_remove_approval_response(self):
        """ tests the method that delete an approval response from the
        approval message cache
        """
        cache.set = Mock()
        user_id = SLACK_USER['profile']['email']
        remove_approval_response(user_id)
        assert cache.set.called

    def test_process_dialog_error_data_succeeds(self):
        """
        test the method that combines all the errors that would be displayed on slack
        """
        error_data = {
            'other_cancelled_reason': BOT_DIALOG_ERROR['not_empty'],
            'other_reject_reason': BOT_DIALOG_ERROR['not_empty']
        }

        all_errors = process_dialog_error_data(error_data)
        assert 'errors' in all_errors
        assert all_errors['errors'][0]['name'] == 'other_cancelled_reason'
        assert all_errors['errors'][0]['error'] == BOT_DIALOG_ERROR['not_empty']
        assert all_errors['errors'][1]['name'] == 'other_reject_reason'
        assert all_errors['errors'][1]['error'] == BOT_DIALOG_ERROR['not_empty']
