"""Module to handle bot available actions"""

from bot.attachments.buttons.common.campuses import lagos_buildings
from bot.attachments.buttons.common.duration_buttons import whole_day_few_hours_btns
from bot.attachments.buttons.common.book_and_find_someone import book_seat_find_someone_buttons
from bot.attachments.buttons.common.menu import get_hot_desk_list
from bot.utilities.constants import DEFAULT, TIMEOUT, GOOGLE_SHEET_NOT_FOUND, NOT_IMPLEMENTED_MSG
from bot.utilities.helpers.bot_helpers import render_previous_menus
from bot.utilities.slack.slack_helper import get_slack_hot_desk_floors_with_cancel, get_slack_hot_desk_list

hot_desk_data = []


class AvailableActions:
    """Handles all available actions for hot desk, floors, seats, etc"""

    @classmethod
    def get_buildings(cls, **kwargs):
        """Method to get building buttons

        Args:
            attachments (dict): dictionary containing buttons.
        Returns(dict): dictionary containing a text and attachments.
        """

        choice = kwargs.get('choice', '')
        center_mapper = {'book a seat': lagos_buildings}
        if len(lagos_buildings[0]['actions'][:-1]) > 1:
            return {
                'text': 'What building will you like to sit in?',
                'attachments': center_mapper.get(choice),
            }
        duration_mapper = {'book a seat': whole_day_few_hours_btns}
        return {
            'text': 'How long will you be in the office?',
            'attachments': duration_mapper.get(choice),
        }

    @classmethod
    def get_book_seat_find_someone_buttons(cls, **kwargs):
        """ Method to display book seat and find someone button.

            Args:
                attachments (list): list containing buttons.
            Returns (dict): dictionary containing a text and attachments
        """

        choice = kwargs.get('choice', '')
        button_mapper = {'lagos': book_seat_find_someone_buttons}

        return {
            'text': 'What will you like to do today?',
            'attachments': button_mapper.get(choice),
        }

    @classmethod
    def find_someone_action(cls, **kwargs):
        """ Method to display a message when user clicks find someone.

            Args:
                attachments (list): list containing buttons.
            Returns (dict): dictionary containing a text
        """
        return NOT_IMPLEMENTED_MSG

    @classmethod
    def a_few_hours_action(cls, **kwargs):
        """ Method to display a message when user clicks a few hours button.

            Args:
                attachments (list): list containing buttons.
            Returns (dict): dictionary containing a text
        """
        return NOT_IMPLEMENTED_MSG

    def get_available_hot_desks(self):
        """Method to get available Hot desks from the Space Allocation Sheet.

        Args:
            result (dict): dictionary containing action details.
        Returns(dict): dictionary containing available hot desks.
        """
        try:
            data = {
                'attachments': hot_desk_data,
                'response_type': 'ephemeral',
                'channel': self.channel_id,
                'user': self.user_id
            }
            return data

        except TimeoutError:
            return {'text': TIMEOUT}

    @classmethod
    def get_available_floors(cls, **kwargs):
        """Method that display available floors
        Args:
            result (dict): dictionary containing action details.
        Returns(dict): dictionary containing available floors.
        """
        try:
            result = kwargs['result']
            channel_id = result['channel']['id'],
            user_id = result['user']['id']

            data = {
                'attachments': get_slack_hot_desk_floors_with_cancel(),
                'response_type': 'ephemeral',
                'channel': channel_id,
                'user': user_id
            }
            if not data['attachments']:
                return {'text': GOOGLE_SHEET_NOT_FOUND}
            return data

        except TimeoutError:
            return {'text': TIMEOUT}

    def get_available_seats(self, attachements):
        """Method that get available seats in floors
        Args:
            attachments(list): list containing hot desk seats
        Returns(dict): dictionary containing available seats in floors."""
        try:

            data = {
                'attachments': attachements,
                'response_type': 'ephemeral',
                'channel': self.channel_id,
                'user': self.user_id
            }

            return data

        except TimeoutError:
            return {'text': TIMEOUT}

    @classmethod
    def map_slack_actions(cls, choice, result):
        """Method which maps user actions to methods
        Args:
            self: class instance
            choice (str): user action
            result (dict): dictionary containing action details
        Returns:
            function call
        """
        choice_mapper = {
            'book a seat': cls.get_buildings,
            'lagos': cls.get_book_seat_find_someone_buttons,
            'cancel': cls.cancel_hotdesk_request,
            'back': render_previous_menus,
            'the whole day': cls.get_available_floors,
            'hot desk': cls.request_hot_desk_handler,
            'cancel request': cls.cancel_hot_desk_button_handler,
            'reject': cls.dialog,
            'approve': cls.update_spreadsheet_handler,
            'cancel hot desk': cls.cancel_hot_desk_reason_options,
            'cancel reason options': cls.cancel_hot_desk_reason,
            'submit cancel hot desk reason': cls.submit_cancel_hot_desk_reason,
            'find someone': cls.find_someone_action,
            'a few hours': cls.a_few_hours_action}
        func = choice_mapper.get(choice)
        kwargs = dict(choice=choice, result=result)
        return func(**kwargs) if func else DEFAULT

    def get_single_floor_seats_allocation(self, choice_name, slack_floors):
        """Method that returns the seats for a single floor
        Args:
            choice_name(str): name of interactive button clicked
            slack_floors(list):
        Returns(list): list containing seats for a single floor
        """
        if slack_floors and choice_name == 'et' and len(slack_floors) == 1:
            return self.get_available_seats(
                get_hot_desk_list(
                    slack_floors[0],
                    get_slack_hot_desk_list(),
                    single_floor=True))

    def get_multiple_floors_seats_allocation(self, choice_name, slack_floors):
        """Method that returns the seats for multiple floors
        Args:
            choice_name(str): name of interactive button clicked
            slack_floors(list):
        Returns(list): list containing seats for mutiple floors
        """
        if slack_floors and len(
                choice_name
        ) > 2 and f'{choice_name[0]}{choice_name[1:].lower()}' in slack_floors:
            return self.get_available_seats(
                get_hot_desk_list(choice_name, get_slack_hot_desk_list()))

    def get_empty_floor_and_seat_response(self, choice_name, slack_floors):
        """Method that returns a message for no available seats
        Args:
            choice_name(str): name of interactive button clicked
            slack_floors(list):
        Returns:
            message(dict): message
        """
        if slack_floors is not None and choice_name == 'et' and len(
                slack_floors) == 0:
            return {
                'text':
                    'Sorry there are no available seats at the moment :disappointed:'
            }
