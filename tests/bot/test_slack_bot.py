"""
Module of tests for slack helper
"""
from unittest.mock import MagicMock, patch, Mock
from slackclient import SlackClient


# Utilities
from bot.utilities.slack.slack_helper import SlackHelper
from bot.utilities.constants import (
    ASSIGNED_HOTDESK_MSG, PERMANENT_SEAT_MSG)

from bot.tasks.slack_bot import BotTasks
from bot.views.bot_action_handlers import BotActionHandlers
from bot.utilities.helpers.bot_helpers import check_if_user_email_is_in_google_sheet

from tests.mocks.slack_bot import (SLACK_BOT_TOKEN, MSG)

# App config
from config import AppConfig

# Local import
from api.models import User
from api.models.hot_desk import HotDeskRequest
from api.utilities.enums import HotDeskRequestStatusEnum


class TestSlackBot:
    """Tests for slack bot file implementation"""

    def test_slackhelper_init_method(self):
        """ Tests slack client is initialized
        Args:
            self(instance): Instance of TestSlackHelper
        Return
            None
        """
        slack_helper = SlackHelper()
        slack_helper.slack_token = SLACK_BOT_TOKEN
        slack_helper.slack_client = SlackClient(slack_helper.slack_token)
        assert slack_helper.slack_token == SLACK_BOT_TOKEN
        assert slack_helper.slack_client.token == SLACK_BOT_TOKEN

    @patch('main.cache.get', Mock(return_value=['ran@email.com']))
    def test_request_hot_desk_with_valid_data_succeeds(
            self, init_db, mock_slack_api_call, new_user, new_user_two):
        """ Tests get user by email method
        Args:
            self(instance): Instance of TestSlackHelper
            mock_slack_api_call(Fixture): Fixture for monkey patching slack client api call
            new_user(Fixture): Fixture for creating the requester
            new_user_two(Fixture): Fixture for creating the assignee
        Return
            None
        """
        assignee_email = AppConfig.HOT_DESK_ASSIGNEE
        new_user_two.email = assignee_email
        new_user_two.save()
        user_dict = dict(id='sampleId')
        actions = [{'value': '5F 24'}]
        response = BotTasks.request_hot_desk(
            dict(user=user_dict, actions=actions))
        assert response['hotDeskRefNo'] == actions[0]['value']
        assert response['requester']['email'] == new_user.email
        assert response['reason'] is None
        assert response['status'] == HotDeskRequestStatusEnum.pending.value

    @patch('main.cache.get', MagicMock(return_value=False))
    def test_reject_hotdesk_request_with_valid_data_succeeds(
            self, init_db, mock_slack_api_call, new_hot_desk_request):
        """ Tests get user by email method
        Args:
            self(instance): Instance of TestSlackHelper
            mock_slack_api_call(Fixture): Fixture for monkey patching slack client api call
            new_hot_desk_request(Fixture): Fixture for creating new hot desk
        Return
            None
        """

        new_hot_desk_request.status = HotDeskRequestStatusEnum.pending
        new_hot_desk_request.save()
        requester_id = new_hot_desk_request.requester_id

        actions = [{'value': HotDeskRequestStatusEnum.rejected.value}]
        submission = dict(reason='Nothing is difficult to achieve')
        slack_result = dict(actions=actions, submission=submission)
        response = BotTasks.reject_hotdesk_request(
            slack_result, new_hot_desk_request.hot_desk_ref_no)
        assert response['hotDeskRefNo'] == new_hot_desk_request.hot_desk_ref_no
        assert response['requester']['tokenId'] == requester_id
        assert response['reason'] == submission['reason']
        assert response['status'] == HotDeskRequestStatusEnum.rejected.value

    def test_update_slack_ops_team_succeeds(self, init_db, mock_slack_api_call, new_user, test_hot_desk_request, new_user_two):
        """ Tests update slack ops team method
        Args:
            self(instance): Instance of TestSlackHelper
            mock_slack_api_call(Fixture): Fixture for monkey patching slack client api call
            new_user(Fixture): Fixture for creating a user
            test_hot_desk_request(object): hot desk request object
            new_user_two(Fixture): Fixture for creating the requester
        Return
            None
        """
        update = BotTasks.update_slack_ops_team(
            '', '', new_user.email, new_user_two, test_hot_desk_request.hot_desk_ref_no)
        assert update.get('MSG') == MSG
        assert update.get('user')['profile']['email'] == new_user.email
        assert isinstance(update, dict)

    def test_notify_requester_with_valid_data_succeeds(
            self, init_db, mock_slack_api_call, approved_hot_desk_request,
            new_user):
        """ Tests notify_requester method
        Args:
            init_db (object): Initialize the test database
            mock_slack_api_call(Fixture): Fixture for monkey patching slack client api call
            new_user(object): new user object
            approved_hot_desk_request(object): new hot desk request object
        Return
            None
        """
        approved_hot_desk_request.status = HotDeskRequestStatusEnum.pending
        approved_hot_desk_request.requester_id = new_user.token_id
        approved_hot_desk_request.save()
        requester_email = User.query_().filter_by(
            token_id=approved_hot_desk_request.requester_id).first().email
        response = BotTasks.notify_requester(
            hotdesk=approved_hot_desk_request.hot_desk_ref_no,
            requester_id=approved_hot_desk_request.requester_id)

        assert response['MSG']
        assert response['user']['profile'][
            'email'] == requester_email

    @patch('main.cache.get', MagicMock(return_value=['testemail@andela.com']))
    def test_request_subsequent_hotdesk_request_after_approval_on_same_day_fail(
            self, init_db, mock_slack_api_call, new_user,
            approved_hot_desk_request):
        """ Tests requesting for a hotdesk on the same day after one has been approved
        Args:
            self(instance): Instance of TestSlackHelper
            mock_slack_api_call(Fixture): Fixture for monkey patching slack client api call
            new_user_two(Fixture): Fixture for creating a user instance
            approved_hot_desk_request(Fixture): Fixture for creating an approved hotdesk request
        Return
            None
        """
        BotTasks.notify_hot_desk_ineligible_requester.send = Mock(
            side_effect=BotTasks.notify_hot_desk_ineligible_requester)
        BotTasks.request_hot_desk.send = Mock(
            side_effect=BotTasks.request_hot_desk)
        approved_hot_desk_request.save()
        hot_desk = HotDeskRequest.query_().filter_by(
            id=approved_hot_desk_request.id).first()
        hot_desk.update_(status=HotDeskRequestStatusEnum.rejected)
        hot_desk = HotDeskRequest.query_().filter_by(requester_id=new_user.token_id,
                                                     status=HotDeskRequestStatusEnum.pending).first()
        hot_desk.update_(status=HotDeskRequestStatusEnum.approved)
        request = {"result": {
            "user": {"id": new_user.token_id, 'name': new_user.name}}}

        response = BotActionHandlers.request_hot_desk_handler(**request)
        assert response['text'] == ASSIGNED_HOTDESK_MSG.format(
            hot_desk.hot_desk_ref_no)

    @patch('main.cache.get', MagicMock(return_value=['testemail2@andela.com']))
    @patch('main.cache.set', MagicMock(return_value=['testemail2@andela.com']))
    @patch('bot.utilities.slack.slack_helper.SlackHelper.post_message_to_user',
           MagicMock(return_value=PERMANENT_SEAT_MSG))
    def test_request_hotdesk_user_with_allocated_seat_fail(
            self, init_db, new_user):
        """ Tests requesting for a hotdesk by a user with reserved seat
        Args:
            self(instance): Instance of TestSlackHelper
            mock_slack_api_call(Fixture): Fixture for monkey patching slack client api call
            new_user(Fixture): Fixture for creating a user instance
        Return
            None
        """
        response = BotTasks.notify_hot_desk_ineligible_requester(
            new_user.email, new_user.name)
        assert response == PERMANENT_SEAT_MSG

    @patch('main.cache.get', MagicMock(return_value=['TESTEMAIL@andela.COM']))
    def test_check_if_user_email_is_in_google_sheet_succeeds(
            self, init_db, new_user):
        """ Tests getting users from google sheet whose email consists of
            uppercase and lowercase letters
        Args:
            self(instance): Instance of TestSlackHelper
            init_db (object): Initialize the test database
            new_user(Fixture): Fixture for creating a user instance
        Return
            None
        """

        user = check_if_user_email_is_in_google_sheet(new_user.email)

        assert user[0][0] == new_user.email
