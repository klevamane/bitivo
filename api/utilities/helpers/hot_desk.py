# model
from api.models import HotDeskRequest, User, HotDeskResponse

# utilities
from api.utilities.error import raises


def get_hotdesk_of_specific_user_by_requester_id(hot_desk_id,requester_id):
    """ Gets the requester's pending or approved hot desk data
    for today from the database
    Args:
        hot_desk_id (str): id of the hot desk request
        requester_id (str): token_id of the requester
    Returns:
        dict: Approved or pending hotdesk data
    """
    hotdesk_request = HotDeskRequest.get_or_404(hot_desk_id)
    if (requester_id == hotdesk_request.requester_id):
        return hotdesk_request

    raises('cant_cancel', 403,'hot desk')


def filter_hotdesk_response(*args):
    """ filter hostdesk response data based on the args supplied

     Args:
        status(str): The hot desk response status
        responder (str): token_id of the responder
        start_date (date): Start date. Defaults to 7 days difference from the end_date
        end_date (date): End date. Defaults to the current date

    Returns:
        dictionary: a dictionary of the hot-desk responder data that match the args supplied
        
    """

    status, responder, startdate, enddate = args
    return HotDeskResponse.query_().filter_by(status=status, is_escalated=False,
            assignee_id=responder).filter(HotDeskResponse.created_at.between(startdate, enddate)).all()
