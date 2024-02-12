
# model
from api.models import HotDeskRequest, User

# schema
from api.schemas.hot_desk import HotDeskRequestSchema

# standard library
from datetime import datetime as dt

# utility
from api.utilities.helpers.calendar import get_start_or_end_of_day
from api.utilities.messages.success_messages import SUCCESS_MESSAGES

from api.utilities.helpers.env_resource_adapter import adapt_resource_to_env
from ..utilities.constants import SHEET_HOT_DESK


def get_pending_or_approved_hot_desk(user_email):
    """ Gets the requester's pending or approved hot desk data
    for today from the database
    Args:
        user_email (str): email of the requester
    Returns:
        dict: Approved or pending hot desk data
    """
    hot_desk_request_schema = HotDeskRequestSchema()
    today = dt.utcnow().date()

    start_date = get_start_or_end_of_day(today)
    end_date = get_start_or_end_of_day(today, end=True)

    user = User.get_by_email(user_email)
    if user:
        requester_id = user.token_id

        hot_desk = HotDeskRequest.query.filter(HotDeskRequest.deleted == False,
            HotDeskRequest.requester_id == requester_id,
            ((HotDeskRequest.status == 'approved') | (HotDeskRequest.status == 'pending'))) \
            .filter(HotDeskRequest.created_at.between(start_date, end_date)).first()

        return hot_desk_request_schema.dump(hot_desk).data


def cancel_hot_desk_by_id(hot_desk_id, reason=''):
    """ updates the hot desk status to cancelled
    Args:
        hot_desk_id (str): id of the hot desk to be cancelled
        reason(str): reason for cancelling the hot desk
    """

    hot_desk_request_schema = HotDeskRequestSchema()
    hot_desk = HotDeskRequest.get(hot_desk_id)
    if hot_desk:

        # circular import
        from bot.tasks.slack_bot import BotTasks
        status = 'cancelled'
        updated_to = SHEET_HOT_DESK
        hot_desk_data = hot_desk_request_schema.load_object_into_schema(
            dict(status=status, reason=reason), partial=True)
        hot_desk.update_(**hot_desk_data)
        adapt_resource_to_env(BotTasks.update_google_sheet.send(
            hot_desk.hot_desk_ref_no, updated_to))

        return SUCCESS_MESSAGES['deleted'].format('Hot desk')
