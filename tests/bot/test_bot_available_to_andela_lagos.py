"""Tests for bot related endpoints"""
import pytest
import json
from unittest import mock
from unittest.mock import MagicMock, patch

from config import AppConfig
from bot.utilities.constants import USER_NOT_FOUND
from bot.utilities.slack.slack_helper import SlackHelper
from bot.utilities.provision_user import provision_user
from bot.tasks.slack_bot import BotTasks
from bot.views.bot_action_handlers import BotActionHandlers

from tests.mocks.centers_button import center_buttons

from ..mocks.slack_bot import ACTIONS, SLACK_USER
from ..mocks.google_sheet import GoogleSheetHelper

BOT_BASE_URL_V1 = AppConfig.BOT_BASE_URL_V1


class TestSlackHelperMethods:
    """
    Test slack helper class
    """

    def test_posting_message_to_channel(self):
        """Test post request method returns 200.
        Args:
            self (Instance): TestSlackHelperMethods instance
        Returns: None
        """

        slack_helper = SlackHelper()

        slack_helper.slack_client.api_call = mock.Mock()
        msg = "Testing code "
        attachment = center_buttons
        slack_helper.post_message_to_channel(msg, attachment, 'user_id',
                                             'channel_id')

        action, kwargs = slack_helper.slack_client.api_call.call_args

        assert action[0] == "chat.postEphemeral"
        assert kwargs.get('text') == msg
        assert kwargs.get('username') == 'activo_test_bot'
        assert slack_helper.slack_client.api_call.called

    def test_launch_bot_endpoint_returns_200_status_code(self, client):
        """Test post request method returns 200.
        Args:
            self (Instance): TestSlackHelperMethods instance
            client (FlaskClient): fixture to get flask test client.
        Returns: None
        """

        client = mock.MagicMock()

        response = client.post(BOT_BASE_URL_V1)
        response.return_value = 200
        assert response.return_value == 200

    def test_user_actions(self, client):
        """Test the user actions endpoint.
        Args:
            self (Instance): TestSlackHelperMethods instance
            client (FlaskClient): fixture to get flask test client.
        Returns: None
        """
        client = mock.MagicMock()

        response = client.post(f'{BOT_BASE_URL_V1}/bot-actions')
        response.status_code = 200
        response.return_value = {}

        assert response.status_code == 200
        assert isinstance(response.return_value, dict)

    def test_request_hot_desk_fails(self, mock_slack_api_call,
                                    new_hot_desk_request, new_user):
        """
        Tests request hot desk fails
        Args:
            self (SQLAlchemy): instance of this class
            new_user (User): fixture for creating an assignee
            new_hot_desk_request (HotDesk): fixture that gets a center in the db
            mock_slack_api_call (obj) Fixture for monkey patching slack client api call
        """

        del SLACK_USER['id']
        AppConfig.HOT_DESK_ASSIGNEE = '5amv3l@andela.com'

        slack_helper = SlackHelper()
        slack_helper.user_info = mock_slack_api_call

        with pytest.raises(KeyError):
            response = BotTasks.request_hot_desk({
                'user': SLACK_USER,
                'actions': ACTIONS
            })

    @mock.patch(
        "api.views.hot_desk_analytics.GoogleSheetHelper",
        GoogleSheetHelper,
    )
    def test_update_spreadsheet_succeeds(self, new_hot_desk_request):
        """
        Tests update spread sheet succeeds
        Args:
            self (SQLAlchemy): instance of this class
            new_hot_desk_request (HotDesk): fixture that gets a center in the db
        """

        new_hot_desk_request.hot_desk_ref_no = '1M 120'
        hot_desk = new_hot_desk_request.save()
        BotActionHandlers.slack_dm = mock.Mock()

        hot_desk_ref_no = ACTIONS[0]['value']

        BotTasks.update_spreadsheet = mock.Mock(
            side_effect=BotTasks.update_spreadsheet(SLACK_USER,
                                                    hot_desk_ref_no))

    @patch('main.cache.get', MagicMock(return_value=['testemail@andela.com']))
    def test_invalid_user_request_for_desk(self, init_db,
                                           mock_slack_api_call_2):
        """Test that appropriate response is returned when invalid user makes a request
        Args:
            self(Instance):
        Returns: None
        """
        user_dict = dict(id='sampleId')
        actions = [{'value': '5F 24'}]
        slack_helper = SlackHelper()
        slack_helper.slack_client.api_call = mock.Mock()
        mock_get_patcher = mock.patch(
            'bot.utilities.provision_user.requests.get')
        mock_get = mock_get_patcher.start()
        mock_get.return_value.json.return_value = {'values': []}
        with mock.patch(
                'bot.utilities.slack.slack_helper.SlackHelper.post_message_to_user'
        ) as post_message_to_user_call:
            response = BotTasks.request_hot_desk(
                dict(user=user_dict, actions=actions))
            post_message_to_user_call.assert_called_once_with(
                USER_NOT_FOUND, None, 'sample@andela.com')
        mock_get_patcher.stop()
        assert response is None

    @patch('main.cache.get', MagicMock(return_value=['testemail@andela.com']))
    def test_user_is_provisioned_succeeds(self, init_db, mock_slack_api_call_2,
                                          new_user_two, test_center_with_users,
                                          default_role):
        """
        Tests that user not in the db requesting for a desk is added to the db
        Args:
            init_db (SQLAlchemy): fixture to initialize the test database
            mock_slack_api_call_2 (obj) Fixture for monkey patching slack client api call
            new_user_two (obj): fixture for creating an assignee
            test_center_with_users (obj): fixture that gets a center in the db
            default_role (obj): fixture that assigns a role to the user
        """

        assignee_email = AppConfig.HOT_DESK_ASSIGNEE
        new_user_two.email = assignee_email
        new_user_two.save()
        user_dict = dict(id='sampleId')
        actions = [{'value': '5F 24'}]
        mock_get_patcher = mock.patch(
            'bot.utilities.provision_user.requests.get')
        mock_get = mock_get_patcher.start()
        mock_get.return_value.raise_for_status.return_value = None
        mock_get.return_value.json.return_value = {
            'values': [{
                'id': "sampleId",
                'email': 'mabel@andela.com',
                'first_name': 'mabel',
                'last_name': 'prince',
                'picture': 'nice_pic',
            }]
        }
        response = BotTasks.request_hot_desk(
            dict(user=user_dict, actions=actions))
        mock_get_patcher.stop()
        assert response['requester']['email'] == 'mabel@andela.com'
        assert response['hotDeskRefNo'] == actions[0]['value']
