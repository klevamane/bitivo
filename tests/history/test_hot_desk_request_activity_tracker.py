# Third party libraries
from flask import json

# models
from api.models.hot_desk import HotDeskRequest
from api.models import History
# Utilities
from bot.tasks.slack_bot import BotTasks

# Constants
from api.utilities.constants import HOT_DESK_HISTORY_MESSAGES

# enum
from api.utilities.enums import HotDeskRequestStatusEnum

from unittest.mock import MagicMock, patch
from main import cache

# Mocks
from tests.mocks.hot_desk import VALID_HOT_DESK_COMPLAINT

# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestHotDeskRequestActivityTracker:
    """Tests for hot desk requests activity tracker
    """

    def test_create_hot_desk_request_activity_tracker_succeed(
            self, init_db, mock_slack_api_call_2, new_user_two,
            new_hot_desk_request):
        """Tests that hisstory of a hot desk request is saved in the 'history' table
        Args:
            init_db (SQLAlchemy): fixture to initialize the test database
            mock_slack_api_call_2 (Fixture) Fixture for monkey patching slack client api call
            new_user_two (Fixture): fixture for creating an assignee
            new_hot_desk_request (Fixture): fixture for creating a pending hotdesk rquest
        """
        hot_desk_request_id = new_hot_desk_request.save().id
        history = History.query_().filter_by(
            resource_id=hot_desk_request_id).all()
        assert history[0].resource_id == hot_desk_request_id
        assert history[0].action == HotDeskRequestStatusEnum.pending.value
        assert history[0].actor_id == new_hot_desk_request.assignee_id
        assert history[0].activity == HOT_DESK_HISTORY_MESSAGES['pending_approval'] + \
            new_user_two.name
        assert history[1].action == 'created'
        assert history[1].activity == HOT_DESK_HISTORY_MESSAGES[
            'request_created']
        assert history[1].actor_id == new_hot_desk_request.requester_id

    @patch('main.cache.get', MagicMock(return_value=False))
    def test_reject_hot_desk_request_track_history_succeed(
            self, init_db, mock_slack_api_call, test_hot_desk_request):
        """Tests that history of a hot desk request when rejected
            is saved in the 'history' table
        Args:
            self(instance): Instance of TestSlackHelper
            mock_slack_api_call(Fixture): Fixture for monkey patching slack client api call
            test_hot_desk_request (Fixture): fixture for creating a pending hotdesk rquest
        Return
            None
        """

        test_hot_desk_request.status = HotDeskRequestStatusEnum.pending
        test_hot_desk_request.save()

        actions = [{'value': HotDeskRequestStatusEnum.rejected.value}]
        submission = dict(reason='You are not eligible')
        slack_result = dict(actions=actions, submission=submission)
        response = BotTasks.reject_hotdesk_request(
            slack_result, test_hot_desk_request.hot_desk_ref_no)
        response_json = json.loads(json.dumps(response))
        hot_desk_request_id = response_json["id"]

        history = History.query_().filter_by(
            resource_id=hot_desk_request_id).first()

        assert history.resource_id == hot_desk_request_id
        assert history.action == HotDeskRequestStatusEnum.rejected.value
        assert history.actor_id == test_hot_desk_request.assignee_id
        assert history.activity == 'Request rejected, Reason: You are not eligible'

    def test_hot_desk_request_track_history_when_asignee_changes_succeed(
            self, init_db, mock_slack_api_call, approved_hot_desk_request,
            new_user_three):
        """Tests that history of a hot desk request when asignee changes
            is saved in the 'history' table
        Args:
            self(instance): Instance of TestSlackHelper
            mock_slack_api_call(Fixture): Fixture for monkey patching slack client api call
            approved_hot_desk_request (Fixture): fixture for creating hotdesk rquest
        Return
            None
        """
        approved_hot_desk_request.status = HotDeskRequestStatusEnum.pending
        approved_hot_desk_request.save()
        new_user_three.save()
        hot_desk = HotDeskRequest.query_().filter_by(
            id=approved_hot_desk_request.id).first()
        hot_desk.update_(assignee_id=new_user_three.token_id)
        history = History.query_().filter_by(resource_id=hot_desk.id).first()
        assert history.resource_id == hot_desk.id
        assert history.action == HotDeskRequestStatusEnum.pending.value
        assert history.actor_id == new_user_three.token_id
        assert history.activity == HOT_DESK_HISTORY_MESSAGES['pending_approval'] + \
            new_user_three.name

    def test_hot_desk_complaint_tracker_succeed(
            self, client, init_db, auth_header, new_hot_desk_request):
        """Tests that history of a hot desk request when a requester complains
        is saved in the 'history' table
        Args:
            self(instance): Instance of TestSlackHelper
            client(Fixture): Flask test client
            auth_header(dict): fixture to get token
            new_hot_desk_request (Fixture): fixture for creating a pending hotdesk request
        Return
            None
        """
        hot_desk_request_id = new_hot_desk_request.save().id
        data = json.dumps(VALID_HOT_DESK_COMPLAINT)
        client.patch(
            f'{API_BASE_URL_V1}/hot-desks/{hot_desk_request_id}',
            headers=auth_header,
            data=data)
        activity = f'Complaint: {VALID_HOT_DESK_COMPLAINT["complaint"]}'
        history = History.query_().filter_by(
            resource_id=hot_desk_request_id).first()
        assert history.resource_id == hot_desk_request_id
        assert history.action == 'complaint'
        assert history.actor_id == new_hot_desk_request.requester_id
        assert history.activity == activity
