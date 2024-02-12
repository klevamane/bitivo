# Third party
from flask_restplus import Resource
from flask import request
from datetime import datetime as dt

# Local imports
from bot.utilities.helpers.bot_helpers import store_centers
from main import activo_bot, cache, dramatiq
from api.models import HotDeskRequest

# Utilities
from api.utilities.helpers.env_resource_adapter import adapt_resource_to_env

from api.utilities.helpers.calendar import get_start_or_end_of_day
from ..attachments.buttons.common.centers import add_cancel_button
from ..attachments.buttons.common.menu import get_floors_list
from ..utilities.slack.slack_helper import SlackHelper
from ..utilities.constants import ACTIVO_BOT_ICON, TIMEOUT, HELP_MESSAGE, INVALID_COMMAND
from ..utilities.google_sheets.google_sheets_helper import GoogleSheetHelper
from ..utilities.user_hot_desk import get_pending_or_approved_hot_desk
from ..utilities.constants import HOT_DESK_MSG
from ..attachments.buttons.common.yes_or_no import yes_or_no_button
from ..utilities.greeting import greeting


# Models
from api.models import Center

# Schema
from api.schemas.center import CenterSchema

slack_helper = SlackHelper()


def google_sheet_data():
    """
    get all hotdesks from google sheet

    Returns:
        list: list of all hotdesks
    """
    google_sheets_helper = GoogleSheetHelper()
    hot_desk_list = google_sheets_helper.retrieve_all_hot_desk()
    return hot_desk_list


def get_non_requested_hotdesks(hot_desk_list):
    """
    get the hotdesks that have not been requested

    Args:
        hot_desk_list (list): list of all the hotdesk

    Returns:
        list: list of hotdesks that have not been requested
    """
    today = dt.today()
    start_date = get_start_or_end_of_day(today, end=False)
    end_date = get_start_or_end_of_day(today, end=True)

    pending_seats_today = HotDeskRequest.query.\
        filter(HotDeskRequest.created_at.between(
            start_date, end_date)).filter_by(status='pending')

    pending_hot_desk_refs = [
        each.hot_desk_ref_no for each in pending_seats_today
    ]

    hot_desk_list_ = []
    for each in hot_desk_list:
        pp = next(iter(each.items()))
        hot_desk_list_ = pp[1]
        key = pp[0]
        hot_desk_list_ = [x.strip(' ') for x in hot_desk_list_]
        non_requested_desks = [
            obj for obj in hot_desk_list_ if obj not in pending_hot_desk_refs
        ]
        each[key] = non_requested_desks
    return hot_desk_list


@dramatiq.actor
def initialize_bot(refresh=True):
    """Caches hot desk data from google sheet"""
    cache_hot_desk_list = cache.get('slack_hot_desk_list')
    cache_floors = cache.get('floors')
    requester_name = cache.get('name')

    if not cache_floors or not cache_hot_desk_list or refresh:
        hot_desk_floors, hot_desk_list, floors = get_floors_list(
            google_sheet_data())

        hot_desk_list = get_non_requested_hotdesks(hot_desk_list)

        hot_desk_floors_with_cancel = hot_desk_floors[:]

        google_sheets_helper = GoogleSheetHelper()
        seat_location = google_sheets_helper.get_requester_seat_location(
            requester_name)
        hot_desk_users_list = google_sheets_helper.retrieve_all_hotdesk_eligible_users()
        cache.set('hot_desk_users_list', hot_desk_users_list, timeout=50)
        cache.set('permanent_seat', seat_location, timeout=50)
        cache.set('slack_hot_desk_floors', hot_desk_floors, timeout=50)
        cache.set(
            'slack_hot_desk_floors_with_cancel',
            hot_desk_floors_with_cancel,
            timeout=50)
        cache.set('slack_hot_desk_list', hot_desk_list, timeout=50)
        cache.set('floors', floors, timeout=50)
        return dict(message='Init Bot: fetched data from spreadsheet')

    hot_desk_list = get_non_requested_hotdesks(cache_hot_desk_list)
    cache.set('slack_hot_desk_list', hot_desk_list, timeout=50)

    return dict(
        message='Init Bot: maintaining current persisted spreadsheet data')


@activo_bot.route('')
class SlackBotResource(Resource):
    """Resource for the /activo command"""

    def post(self):
        """View method which  handles /activo command
        Returns: str
        """

        decision_mapper = {'': self.get_menus,
                           'help': self.get_help, 'cancel': self.cancel_hot_desk}

        text = request.form.get('text', '')
        username = request.form.get('user_name', '')
        name = (" ".join(username.split("."))).title()
        cache.set('name', name, timeout=50)
        user_id = request.form.get('user_id')
        channel_id = request.form.get('channel_id')
        decision = decision_mapper.get(text)
        response = (decision(username, user_id, channel_id)
                    if decision else self.get_help(username,
                                                   user_id, channel_id, title=INVALID_COMMAND.format(text)))

        # only store the centers message if after removing all
        store_centers(response) if text == '' else None

        return response, 200

    def get_center_buttons(self):
        """Method which handles interactions with bot responses
        Returns: (dict)
        """
        try:
            centers = Center.query_().all()[::-1]
            center_schema = CenterSchema(many=True, only=("id", "name"))

            center_buttons = add_cancel_button(
                center_schema.dump(centers).data)
            return center_buttons
        except ConnectionError:
            return {'text': TIMEOUT}

    def get_menus(self, username, user_id, channel_id):
        """Method which handles all buttons display
        Returns: str
        """
        # Send a cronjob to initialize bot
        # initialize_bot_data = adapt_resource_to_env(initialize_bot.delay)
        initialize_bot_data = adapt_resource_to_env(initialize_bot.send)
        initialize_bot_data(False)
        message = '{} *@{}*\nWelcome to Activo!\nI am your hot desk assistant\
            \nPlease select your Andela center:'
        text = message.format(greeting(), username)

        data = {
            'text': text,
            'attachments': self.get_center_buttons(),
            'response_type': 'ephemeral',
            'channel': channel_id,
            'user': user_id,
            'as_user': False,
            'icon_url': ACTIVO_BOT_ICON
        }

        return data

    def get_help(self, username, user_id, channel_id, title=HELP_MESSAGE):
        """Method which handles help information on the bot
        Args:
            self (instance): Instance of the SlackBotResource
            username (str): slack username for current user
            user_id (str): slack user id for current user
            channel_id (str): slack channel id for current channel
        """
        return {
            'text':
            f' Hi *@{username}*, {title}'
            '\n `/activo`: Enables you interact with bot functionalities by requesting for an hot desk'
            '\n `/activo cancel`: Enables you to cancel your pending or approved hot desk'
            '\n `/activo help`: Detailed information on how to use the bot'
        }

    def cancel_hot_desk(self, username, user_id, channel_id):
        """Method which handles the cancel call function to check
        if a user has a pending or approved hot desk

        Args:
            self (instance): Instance of the SlackBotResource
            username (str): slack username for current user
            user_id (str): slack user id for current user
            channel_id (str): slack channel id for current channel

        Returns: yes or no button or text
        """
        # Send a cronjob to initialize bot
        initialize_bot_data = adapt_resource_to_env(initialize_bot.send)
        initialize_bot_data(False)

        # requester info
        requester = slack_helper.user_info(user_id)
        requester_email = requester['profile']['email']

        # get the user hotdesk data
        user_hotdesk = get_pending_or_approved_hot_desk(requester_email)

        if user_hotdesk:
            yes_name = 'cancel hot desk'
            data = {
                'text':  HOT_DESK_MSG['confirm_delete_hot_desk'].format(username),
                'attachments': yes_or_no_button(yes_name, yes_value=requester_email)
            }
            return data
        else:
            return {'text':  HOT_DESK_MSG['no_hot_desk'].format(username)}
