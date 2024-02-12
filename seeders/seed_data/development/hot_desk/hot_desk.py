"""Development/Testing environment hot desk request seed data module"""
import datetime

# Models
from api.models import HotDeskRequest, User
from api.utilities.enums import HotDeskRequestStatusEnum

#Helpers
from api.utilities.helpers import calendar

def hot_desk_data():
    """ Creates a dict for a hot desk request
        Returns:
            list: A list of request dictionaries
    """

    # Users
    user_one, user_two, user_three, user_four, user_five, user_six,user_seven,\
    user_eight, user_nine, user_ten,user_eleven,user_twelve,user_thirteen = \
    User.query_().limit(13).all()

    return [{
            "requester_id": user_one.token_id,
            "status": HotDeskRequestStatusEnum.pending,
            "hot_desk_ref_no": "1G 65",
            "assignee_id": user_five.token_id,
            "reason": ""
    },
            {
                "status": HotDeskRequestStatusEnum.pending,
                "hot_desk_ref_no": "1G 45",
                "assignee_id": user_five.token_id,
                "reason": "",
                "requester_id": user_two.token_id
            },
            {
                "requester_id": user_three.token_id,
                "hot_desk_ref_no": "1F 55",
                "assignee_id": user_five.token_id,
                "reason": "",
                "created_at":calendar.get_start_of_week(datetime.datetime.utcnow()),
                "status": HotDeskRequestStatusEnum.approved,
            },
            {
                "requester_id": user_four.token_id,
                "status": HotDeskRequestStatusEnum.approved,
                "assignee_id": user_five.token_id,
                "reason": "",
                "created_at":calendar.get_start_of_week(datetime.datetime.utcnow()),
                "hot_desk_ref_no": "1N 123"
            },
            {
                "status": HotDeskRequestStatusEnum.pending,
                "requester_id": user_six.token_id,
                "hot_desk_ref_no": "1N 120",
                "reason": "",
                "created_at":calendar.get_start_of_month(datetime.datetime.utcnow()),
                "assignee_id": user_five.token_id
            },
            {
                "status": HotDeskRequestStatusEnum.pending,
                "hot_desk_ref_no": "1N 121",
                "requester_id": user_seven.token_id,
                "assignee_id": user_five.token_id,
                "created_at":calendar.get_start_of_quarter(datetime.datetime.utcnow()),
                "reason": ""
            },
            {
                "created_at":calendar.get_start_of_quarter(datetime.datetime.utcnow()),
                "status": HotDeskRequestStatusEnum.pending,
                "hot_desk_ref_no": "1N 124",
                "assignee_id": user_five.token_id,
                "reason": "",
                "requester_id": user_eight.token_id,
            },
            {
                "hot_desk_ref_no": "1N 126",
                "assignee_id": user_five.token_id,
                "requester_id": user_nine.token_id,
                "status": HotDeskRequestStatusEnum.rejected,
                "reason": "",
                "created_at":calendar.get_start_of_year(datetime.datetime.utcnow())
            },
            {
                "requester_id": user_ten.token_id,
                "assignee_id": user_five.token_id,
                "reason": "",
                "status": HotDeskRequestStatusEnum.rejected,
                "hot_desk_ref_no": "1N 119",
            },
            {
                "assignee_id": user_five.token_id,
                "reason": "",
                "status": HotDeskRequestStatusEnum.rejected,
                "requester_id": user_eleven.token_id,
                "hot_desk_ref_no": "1N 127",
                "created_at":calendar.get_start_of_year(datetime.datetime.utcnow())
            },
            {
                "status": HotDeskRequestStatusEnum.approved,
                "assignee_id": user_five.token_id,
                "reason": "",
                "requester_id": user_twelve.token_id,
                "created_at":calendar.get_start_of_month(datetime.datetime.utcnow()),
                "hot_desk_ref_no": "1N 128",
            },
            {
                "hot_desk_ref_no": "1N 122",
                "assignee_id": user_five.token_id,
                "reason": "",
                "requester_id": user_thirteen.token_id,
                "status": HotDeskRequestStatusEnum.pending,
                "created_at":calendar.get_start_of_month(datetime.datetime.utcnow())

            }]
