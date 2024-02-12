import json
from unittest.mock import Mock, patch
from datetime import datetime

from config import AppConfig
from tests.mocks.hot_desk import SLACK_INTERACTIVE_PAYLOAD
from bot.utilities.constants import HOT_DESK_MSG
from bot.views.bot_actions import ActionResource

BOT_BASE_URL_V1 = AppConfig.BOT_BASE_URL_V1


class TestOutsideBusinessHoursRequests:
    """Tests requests outside work hours"""

    @patch('bot.views.bot_actions.dt')
    def test_hotdesk_request_at_7_am_fails(self, mock_dt, client):
        """ Tests hotdesks requests at 8 am local time fail
        Args:
            self(Instance): TestOutsideBusinessHoursRequests instance
            mock_dt: datetime.datetime Mock object
        Returns:
            None
        """
        mock_dt.utcnow = Mock(return_value=datetime(2019, 6, 10, 6))
        payload = json.dumps(SLACK_INTERACTIVE_PAYLOAD)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        requester_name = SLACK_INTERACTIVE_PAYLOAD['user']['name']
        response = client.post(
            f'{BOT_BASE_URL_V1}/bot-actions',
            data={'payload': payload},
            headers=headers)
        assert response.status_code == 200
        assert json.loads(response.data).get(
            'text') == HOT_DESK_MSG['not_work_hours'].format(requester_name)

    @patch('bot.views.bot_actions.dt')
    def test_is_not_business_hours_7_59_am_succeeds(self, mock_dt):
        """ Tests function is_not_business_hours returns true at 7:59
        Args:
            self(Instance): TestOutsideBusinessHoursRequests instance
            mock_dt: datetime.datetime Mock object
        Returns:
            None
        """
        mock_dt.utcnow = Mock(return_value=datetime(2019, 6, 10, 6, 59))
        result = ActionResource.is_not_business_hours(
            SLACK_INTERACTIVE_PAYLOAD)
        assert result

    @patch('bot.views.bot_actions.dt')
    def test_is_not_business_hours_6_pm_succeeds(self, mock_dt):
        """ Tests function is_not_business_hours returns true at 6:00 pm
        Args:
            self(Instance): TestOutsideBusinessHoursRequests instance
            mock_dt: datetime.datetime Mock object
        Returns:
            None
        """
        mock_dt.utcnow = Mock(return_value=datetime(2019, 6, 10, 17))
        result = ActionResource.is_not_business_hours(
            SLACK_INTERACTIVE_PAYLOAD)
        assert result

    @patch('bot.views.bot_actions.dt')
    def test_is_not_business_hours_8_am_fails(self, mock_dt):
        """ Tests function is_not_business_hours returns false at 8
        Args:
            self(Instance): TestOutsideBusinessHoursRequests instance
            mock_dt: datetime.datetime Mock object
        Returns:
            None
        """
        mock_dt.utcnow = Mock(return_value=datetime(2019, 6, 10, 7))
        result = ActionResource.is_not_business_hours(
            SLACK_INTERACTIVE_PAYLOAD)
        assert not result
