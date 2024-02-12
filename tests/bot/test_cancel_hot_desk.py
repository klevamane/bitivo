"""
Module to tests for cancel hot desk
"""

# Third party library
from unittest.mock import Mock, MagicMock, patch
from main import cache

# utilities
from bot.utilities.user_hot_desk import get_pending_or_approved_hot_desk
from bot.utilities.constants import HOT_DESK_MSG
from bot.utilities.slack.slack_helper import SlackHelper
from bot.utilities.user_hot_desk import cancel_hot_desk_by_id


# mock data
from ..mocks.slack_bot import SLACK_USER, APPROVAL_RESPONSE, ACTIONS

# button data
from bot.attachments.buttons.common.yes_or_no import yes_or_no_button

# views
from bot.tasks.slack_bot import BotTasks
from bot.views.bot_actions import ActionResource

from bot.utilities.helpers.bot_helpers import process_dialog_error_data
from bot.utilities.dialog_serialization_errors import BOT_DIALOG_ERROR


class TestCancelHotDesk:
    """Tests for slack bot cancel hot desk"""

    @patch('main.cache.set', MagicMock(return_value=True))
    @patch('bot.utilities.slack.slack_helper.SlackHelper.update_message_to_user', MagicMock(return_value=True))
    def test_cancel_hot_desk_with_valid_data_succeeds(self, init_db,
        new_user, new_today_hot_desk):
        """ Tests cancel hotdesk when user select yes to cancel an hotdesk
        Args:
            self(instance): Instance of TestCancelHotDesk
            init_db (SQLAlchemy): fixture to initialize the test database
            new_today_hot_desk (HotDesk): fixture for creating an hot desk
            new_user(User): Fixture for creating the requester
        """
        new_response = APPROVAL_RESPONSE.copy()

        slack_helper = SlackHelper()
        slack_helper.post_message_to_user = Mock(return_value=True)

        # mock background task and sheet update
        BotTasks.check_and_update_sheet = Mock(return_value=True)
        BotTasks.update_google_sheet.send = Mock(side_effect=BotTasks.update_google_sheet)
        BotTasks.cancel_hot_desk.send = Mock(
            side_effect=BotTasks.cancel_hot_desk)
        BotTasks.notify_user_after_hotdesk_cancellation.send = Mock(
            side_effect = BotTasks.notify_user_after_hotdesk_cancellation)

        # create an hotdesk
        hot_desk = new_today_hot_desk.save()
        approval_response = {hot_desk.id: new_response}
        cache.get = Mock(return_value=approval_response)
        yes_name = 'cancel hot desk'
        yes_value = new_user.email

        #get data from yes or no button attachment
        main_result = yes_or_no_button(yes_name, yes_value=yes_value)
        result = main_result[0]
        result['user'] = SLACK_USER
        result['submission'] = {'cancelled_reason': 'I changed my mind'}
        cancel_hot_desk_by_id(hot_desk.id, 'reason')
        BotTasks.cancel_hot_desk.send = Mock(side_effect=BotTasks.cancel_hot_desk)
        ActionResource.cancel_hot_desk_handler(result)

        assert BotTasks.check_and_update_sheet.called

    @patch('main.cache.set', MagicMock(return_value=True))
    def test_cancel_hot_desk_dialog_messages(self):
        """
        Test cancel hot desk dialog with others field selected
        """
        result = {
            'actions': [{'name': 'cancel hot desk'}],
            'callback_id': 'cancel hot desk',
            'submission': {'cancelled_reason': ' '}
        }
        action_dict = {}
        cancel_hot_desk = ActionResource.process_dialog_message('', result, action_dict)

        error_data = {
            'cancelled_reason': BOT_DIALOG_ERROR['not_empty']
        }

        assert cancel_hot_desk == process_dialog_error_data(error_data=error_data)

    @patch(
        'bot.views.bot_actions.ActionResource.cancel_hot_desk_handler',
        MagicMock(return_value=True)
    )

    @patch('main.cache.set', MagicMock(return_value=True))
    def test_cancel_hot_desk_dialog_without_others_messages(self):
        """
        Test cancel hot desk dialog fields
        """
        result = {
            'actions': [{'name': 'cancel hot desk'}],
            'callback_id': 'cancel hot desk',
            'submission': {'cancelled_reason': 'I want'}
        }
        action_dict = {}
        ActionResource.process_dialog_message('', result, action_dict)

        assert ActionResource.cancel_hot_desk_handler.called
