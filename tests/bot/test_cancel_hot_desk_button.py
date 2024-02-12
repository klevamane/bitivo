"""
Module to tests for cancel hot desk button
"""

# Third party library
from unittest.mock import Mock

# utilities
from bot.utilities.slack.slack_helper import SlackHelper

# views
from bot.views.slack_bot import SlackBotResource
from bot.views.bot_action_handlers.cancel_handlers import CancelHandlers


class TestCancelHotDeskButton:
    """Tests for slack bot cancel hot desk"""

    def test_cancel_hot_desk_button(self, init_db, new_user,
                                    new_today_hot_desk, mock_slack_api_call):
        """ Tests cancel hotdesk button when a user clicks cancel button
        Args:
            self(instance): Instance of test_cancel_hot_desk_button
            init_db (SQLAlchemy): fixture to initialize the test database
            new_today_hot_desk (HotDesk): fixture for creating an hot desk
            new_user(User): Fixture for creating the requester
            mock_slack_api_call: Fixture for monkey patching slack client api call
        """

        slack_helper = SlackHelper()
        slack_helper.post_message_to_user = Mock(return_value=True)

        # create an hotdesk
        hot_desk = new_today_hot_desk.save()

        #mock background task
        slack_resource = SlackBotResource()
        slack_resource.cancel_hot_desk = Mock(return_value=True)

        result = {
            "actions": [{
                "name": 'cancel request'
            }],
            "user": {
                "name": new_user.name,
                "id": "sampleID"
            },
            'channel': {
                "id": 'HI3DJ7HDK'
            }
        }

        response = CancelHandlers.cancel_hot_desk_button_handler(
            result=result)

        assert response[
           'text'] == 'Hey *@{}*, Are you sure you want to *cancel* your hotdesk'.format(new_user.name)
        assert response['attachments'][0]['actions'][0][
            'name'] == 'cancel hot desk'
        assert response['attachments'][0]['actions'][0]['type'] == 'button'
