import json
import os

from tests.mocks.hot_desk import SLACK_THE_WHOLE_DAY_PAYLOAD,\
    SLACK_FEW_HOURS_PAYLOAD, SLACK_BOOK_A_SEAT_PAYLOAD
from tests.mocks.center_buildings import center_with_many_buildings

from bot.attachments.buttons.common.campuses import lagos_buildings


BOT_BASE_URL_V1 = os.getenv('BOT_BASE_URL_V1')


class TestGetCenterBuildings:
    """Tests view center buildings implementation"""

    def test_bot_shows_center_buildings_option_if_center_has_more_than_one_building(self, client):
        """ Tests if the bot shows all center buildings if a center
            has more than one building
        Args:
            client (FlaskClient): fixture to get flask test client
        Returns:
            None
        """
        lagos_buildings[0]['actions'].insert(1, center_with_many_buildings)
        payload = json.dumps(SLACK_BOOK_A_SEAT_PAYLOAD)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = client.post(
            f'{BOT_BASE_URL_V1}/bot-actions',
            data={'payload': payload},
            headers=headers)
        lagos_buildings[0]['actions'].remove(center_with_many_buildings)
        buiding_buttons = json.loads(response.data)
        assert response.status_code == 200
        assert buiding_buttons['attachments'][0]['actions'][0]['name'] == 'et'
        assert buiding_buttons['attachments'][0]['actions'][1]['name'] == 'epict'
        assert json.loads(response.data).get(
            'text') == 'What building will you like to sit in?'

    def test_bot_shows_whole_day_option_and_a_few_hours_option_if_center_has_one_building(self, client):
        """ Tests if the bot shows the whole day button and a few hours button
            if a center has only one building
        Args:
            client (FlaskClient): fixture to get flask test client
        Returns:
            None
        """
        payload = json.dumps(SLACK_BOOK_A_SEAT_PAYLOAD)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = client.post(
            f'{BOT_BASE_URL_V1}/bot-actions',
            data={'payload': payload},
            headers=headers)
        whole_day_few_hours_btns = json.loads(response.data)
        assert response.status_code == 200
        assert whole_day_few_hours_btns['attachments'][0]['actions'][0]['name'] == 'The whole day'
        assert whole_day_few_hours_btns['attachments'][0]['actions'][1]['name'] == 'A few hours'
        assert json.loads(response.data).get(
            'text') == 'How long will you be in the office?'
