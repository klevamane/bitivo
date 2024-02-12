# Standard imports
import json

# Local imports
from main import dramatiq
from config import AppConfig

# Schema
from api.schemas.hot_desk import HotDeskRequestSchema

# Enums
from api.utilities.enums import HotDeskRequestStatusEnum

# Models
from api.models import User, HotDeskRequest, HotDeskResponse

# Base class
from .slack_bot_notification_handler import NotificationHandler

# Utilities
from ..utilities.constants import SHEET_HOT_DESK
from bot.utilities.helpers.spreadsheet_helper import update_spread_sheet_data
from ..utilities.user_hot_desk import cancel_hot_desk_by_id
from ..utilities.helpers.bot_helpers import (update_approval_response_on_cancel,
                                             check_if_user_email_is_in_google_sheet,
                                             get_requester_and_assignee,
                                             get_ineligible_user_email)
from ..utilities.user_hot_desk import get_pending_or_approved_hot_desk
from ..utilities.slack.slack_helper import SlackHelper
from ..utilities.google_sheets.google_sheets_helper import GoogleSheetHelper
from ..utilities.bugsnag import post_bugsnag_exception


slack_helper = SlackHelper()


class BotTasks(NotificationHandler):
    """Class that handles slack bot tasks"""
    @staticmethod
    @dramatiq.actor
    def request_hot_desk(result):
        """Method that persist hot desk requests into the database
        Args:
            result (dict): dictionary containing action details.
        """
        user_info = slack_helper.user_info(result['user']['id'])
        assignee_email = AppConfig.HOT_DESK_ASSIGNEE
        ref_no = result['actions'][0]['value']
        hot_desk_request_schema = HotDeskRequestSchema()
        try:
            requester_email = user_info['profile']['email']
            ineligible_user = get_ineligible_user_email(requester_email)
            requester, assignee = get_requester_and_assignee(
                requester_email, assignee_email)

            if requester and not ineligible_user:
                token_id = assignee.token_id
                data = json.dumps({
                    "requester_id": requester.token_id,
                    "assignee_id": token_id,
                    'hot_desk_ref_no': ref_no,
                    'status': 'pending'
                })
                hot_desk_request_data = hot_desk_request_schema.load_json_into_schema(
                    data)
                hot_desk_request = HotDeskRequest(**hot_desk_request_data)
                hot_desk_request.save()
                return hot_desk_request_schema.dump(hot_desk_request).data
        except Exception as e:
            post_bugsnag_exception(e, f'Could not request hot desk')


    @staticmethod
    @dramatiq.actor
    def reject_hotdesk_request(action_dict, hot_desk_ref_no):
        """Method that rejects hot desk requests
        Args:
            result (dict): dictionary containing action details.

        """
        from ..views.bot_actions import ActionResource
        action_resource = ActionResource()

        try:
            return action_resource.handle_hotdesk_request(action_dict, hot_desk_ref_no)
        except Exception as e:
            post_bugsnag_exception(e, 'Could not reject hot desk')

    @staticmethod
    @dramatiq.actor
    def update_spreadsheet(result, hot_desk_ref_no):
        """Method that updates the spreadsheet
        Args:
            result (dict): dictionary containing action details.
            hot_desk_ref_no (str): hot desk number

        """
        from ..views.bot_actions import ActionResource
        from ..views.slack_bot import initialize_bot

        try:
            action_resource = ActionResource()

            requester_id = HotDeskRequest.query.filter_by(
                hot_desk_ref_no=hot_desk_ref_no).order_by(
                    HotDeskRequest.created_at.desc()).first().requester_id
            requester_name = User.get(requester_id).name

            BotTasks.check_and_update_sheet(hot_desk_ref_no, requester_name)

            action_resource.handle_hotdesk_request(result, hot_desk_ref_no)
            initialize_bot.send()
        except Exception as error:
            post_bugsnag_exception(error, 'Could not approve hot desk')

    @staticmethod
    def check_and_update_sheet(hot_desk_ref_no, updated_to):
        """Method to check the sheet and call the update google sheet method
        Args:
            hot_desk_ref_no: the hot desk ref number
            updated_to(str): What we want to update to
        """
        try:
            sheet_data, sheet = GoogleSheetHelper().open_sheet()
            if sheet:
                bay_column = sheet.col_values(2)[1:]

                for index, (record, column) in enumerate(
                        zip(sheet_data, bay_column[:])):

                    update_spread_sheet_data(index, record, sheet, hot_desk_ref_no, updated_to)
        except Exception as error:
            post_bugsnag_exception(
                error, f'Could not update spreadsheet with ref no - {hot_desk_ref_no}')

    @staticmethod
    @dramatiq.actor
    def cancel_hot_desk(email, reason=''):
        """ Method that remove user from the sheet
            and cancel hot desk from database
        Args:
            email (dict): the dict of the hot desk data
            reason (str): the reason for cancelling the hot desk
        """
        try:
            hot_desk = get_pending_or_approved_hot_desk(email)
            hot_desk_ref_no = hot_desk['hotDeskRefNo']
            updated_to = SHEET_HOT_DESK

            # remove the requester from the hot desk zone
            if hot_desk['status'] == 'approved':
                BotTasks.check_and_update_sheet(hot_desk_ref_no, updated_to)

            hot_desk_id = hot_desk['id']

            # change the status to cancelled in the db
            cancel_hot_desk_by_id(hot_desk_id, reason)

            update_approval_response_on_cancel(hot_desk)
        except Exception as error:
            post_bugsnag_exception(error, f'Could not delete your hot desk')

    @staticmethod
    @dramatiq.actor
    def update_google_sheet(hot_desk_ref_no, updated_to):
        """Method to update the google sheet method
        Args:
            hot_desk_ref_no: the hot desk ref number
            updated_to(str): What we want to update to
        """
        BotTasks.check_and_update_sheet(hot_desk_ref_no, updated_to)
