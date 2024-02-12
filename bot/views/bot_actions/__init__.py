"""Module to handle Bot Action Resource"""

import json
from datetime import datetime as dt, time

from flask import request, jsonify
from flask_restplus import Resource

from main import activo_bot, cache

from bot.views.bot_action_handlers import BotActionHandlers
from bot.utilities.slack.slack_helper import get_slack_floors
from bot.utilities.helpers.bot_helpers import back_navigation_helper
from bot.utilities.constants import HOT_DESK_MSG
from ...utilities.dialog_bot_validation.bot_fields_validators import cancel_hot_desk_dialog_validator
from .available_actions import AvailableActions
from .cache_actions import CacheActions
from .cancel_actions import CancelActions
from .response_actions import ResponseActions


@activo_bot.route('/bot-actions')
class ActionResource(Resource, AvailableActions, CacheActions, CancelActions,
                     ResponseActions, BotActionHandlers):
    """Resource for the action endpoint"""

    def post(self):
        """View method which handles all user actions
        Returns: str
        """
        result = json.loads(request.form.get('payload'))
        if self.is_not_business_hours(result):
            response = self.rejection_response(result['user']['name'])
            response.status_code = 200
            return response
        response = jsonify(self.select_action_name(result))
        response.status_code = 200
        return response

    def select_action_name(self, result, action_dict={}):
        """Method which handles all user actions
        Args:
            result (dict): dictionary containing action details.
        Returns: dict
        """
        channel_id, user_id, username = result['channel']['id'], result[
            'user']['id'], result['user']['name']
        self.channel_id = channel_id
        self.user_id = user_id
        self.username = username

        message_type_mapper = {
            'interactive_message': self.process_interactive_message,
            'dialog_submission': self.process_dialog_message
        }

        func = message_type_mapper.get(result['type'])

        if func:
            return func(result, action_dict)

    def process_dialog_message(self, *args):
        """Method that saves dialog submission action payload into action_dict
        Args:

            result(list): dialog submission action payload
            action_dict(dict): a combination of interactive action payload and dialog submission action payload
        Returns:
            dict
        """

        result, action_dict = args
        action_dict = cache.get('result')
        action_dict.update(result)

        if result['callback_id'] == 'reject':
            ActionResource.reject_hotdesk_handler(action_dict)
        elif result['callback_id'] == 'cancel hot desk':
            errors = cancel_hot_desk_dialog_validator(
                action_dict['submission']['cancelled_reason'])
            if errors:
                return errors
            ActionResource.cancel_hot_desk_handler(action_dict)

        return {}

    def process_interactive_message(self, *args):
        """Method that handles interactive message actions
        Args:
            *args:
                result(list): payload returned when user clicks interactive button
                action_dict(dict): a combination of interactive action payload and dialog submission action payload
        Returns:
            None
        """

        result, action_dict = args

        slack_floors = get_slack_floors()

        choice_name = result['actions'][0]['name'].lower()

        if choice_name in ('reject', 'cancel hot desk'):
            cache.set('result', result)

        self.check_availability_of_cached_data(slack_floors)

        output1 = self.get_empty_floor_and_seat_response(
            choice_name, slack_floors)

        output2 = self.get_single_floor_seats_allocation(
            choice_name, slack_floors)

        output3 = self.get_multiple_floors_seats_allocation(
            choice_name, slack_floors)

        output = output1 or output2 or output3

        if not output and choice_name:
            output = ActionResource.map_slack_actions(choice_name, result)
        back_navigation_helper(
            output, choice_name)  # push the current menu into the cache
        # which will then be the previous menu when back is clicked at the next menu

        return output

    @staticmethod
    def is_not_business_hours(result):
        """ Method which checks if request time is outside business hours
        Args:
            result(dict): payload returned when user clicks interactive button
        Returns: True or False
        """
        center_to_utc_business_end_mapper = {
            'Ghana': time(18),
            'Lagos': time(17),
            'Kigali': time(16),
            'Nairobi': time(15),
            'Kampala': time(15)
        }
        centers = center_to_utc_business_end_mapper.keys()
        if result['callback_id'] == 'some_id' and result['actions'][0][
                'name'] in centers:
            center = result['actions'][0]['name']
            business_end = center_to_utc_business_end_mapper[center]
            request_time = dt.utcnow().time()
            business_start = time(business_end.hour - 10)
            return not business_start <= request_time < business_end

    @staticmethod
    def rejection_response(requester_name):
        """ Method which creates the rejection response for requests outside
        business hours.
        Args:
            result(dict): payload returned when user clicks interactive button
        Returns: rejection jsonified response
        """
        return jsonify(
            {'text': HOT_DESK_MSG['not_work_hours'].format(requester_name)})
