"""
Module of tests for slack helper
"""
from bot.utilities.slack.slack_helper import SlackHelper
from tests.mocks.slack_bot import (SLACK_BOT_TOKEN, ATTACHMENT, MSG)
from slackclient import SlackClient

class TestSlackHelper:
    """Tests for slack helper class"""

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


    def test_post_message_to_channel_succeeds(self, init_db, mock_slack_api_call):
        """ Tests post message to channel method
        Args:
            self(instance): Instance of TestSlackHelper
            mock_slack_api_call(Fixture): Fixture for monkey patching slack client api call
        Return
            None
        """
        slack_helper = SlackHelper()
        message_to_channel = slack_helper.post_message_to_channel('', ATTACHMENT, '', '')
        assert message_to_channel.get('MSG') == MSG
        assert isinstance(message_to_channel, dict)


    def test_get_user_by_email_succeeds(self, init_db,  mock_slack_api_call, new_user):
        """ Tests get user by email method
        Args:
            self(instance): Instance of TestSlackHelper
            mock_slack_api_call(Fixture): Fixture for monkey patching slack client api call
        Return
            None
        """
        slack_helper = SlackHelper()
        get_user = slack_helper.get_user_by_email(new_user.email)
        assert get_user['profile']['name'] == new_user.name
        assert get_user['profile']['email'] == new_user.email
        assert isinstance(get_user, dict)

    
    def test_update_message_succeeds(self, init_db,  mock_slack_api_call):
        """ Tests update message in a channel method
        Args:
            self(instance): Instance of TestSlackHelper
            mock_slack_api_call(Fixture): Fixture for monkey patching slack client api call
        Return
            None
        """
        slack_helper = SlackHelper()
        update_message = slack_helper.update_message_in_channel('', '', '', '')
        assert update_message.get('MSG') == MSG
        assert isinstance(update_message, dict)
        

    def test_get_user_info_succeeds(self, init_db,  mock_slack_api_call):
        """ Tests deleting request that does not exist fails
        Args:
            self(instance): Instance of TestSlackHelper
            mock_slack_api_call(Fixture): Fixture for monkey patching slack client api call
        Return
            None
        """
        slack_helper = SlackHelper()
        slack_user_id = 'sampleId'
        user_info = slack_helper.user_info(slack_user_id)
        assert user_info.get('profile')['id'] == slack_user_id
        assert isinstance(user_info, dict)

    def test_update_message_to_user_succeeds(self, init_db,  mock_slack_api_call):
        """ Tests update message in a channel method
        Args:
            self(instance): Instance of TestSlackHelper
            mock_slack_api_call(Fixture): Fixture for monkey patching slack client api call
        Return
            None
        """
        slack_helper = SlackHelper()
        update_message = slack_helper.update_message_to_user('', '', '')
        assert update_message.get('MSG') == MSG
        assert isinstance(update_message, dict)
        