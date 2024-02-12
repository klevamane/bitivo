"""
Module of tests for  requests activity tracker
"""
# system imports
import json

# models
from api.models import History

# Constant
from api.utilities.constants import CHARSET

# Mocks
from tests.mocks.requests import VALID_REQUEST_DATA

# messages
from api.utilities.messages.success_messages import HISTORY_MESSAGES
from api.utilities.constants import PERMISSION_TYPES

from config import AppConfig
V1_BASE_URL = AppConfig.API_BASE_URL_V1


class TestRequestActivityTracker:
    """Tests for requests activity tracker
    """

    def test_track_create_request_history_created_succeeds(
            self, client, init_db, auth_header, new_user,
            new_request_type_two):
        """Test history is generated when new request is created

         Args:
             client (FlaskClient): fixture to get flask test client
             init_db (SQLAlchemy): fixture to initialize the test database
             auth_header (dict): fixture to get token
             new_user (dict): fixture to create a new user
             new_request_type_two (dict): fixture to create a new request type
         """

        new_user.save()
        new_request_type_two.save()
        VALID_REQUEST_DATA['centerId'] = new_user.center_id
        VALID_REQUEST_DATA['requesterId'] = new_user.token_id
        VALID_REQUEST_DATA['requestTypeId'] = new_request_type_two.id
        data = json.dumps(VALID_REQUEST_DATA)

        response = client.post(
            f'{V1_BASE_URL}/requests', headers=auth_header, data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        response_data = response_json['data']
        history = History.query_().filter_by(
            resource_id=response_data['id']).first()

        assert history.resource_id == response_data['id']
        assert history.action == PERMISSION_TYPES['POST']
        assert history.activity == HISTORY_MESSAGES['added_resource']

    def test_request_update_status_history_created_succeeds(
            self, client, init_db, auth_header, new_request_requester_update,
            new_user, new_request_type_two):
        """History is created when a requester updates an open request with success

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request_requester_update: request with the current user as the requester
            new_user (dict): fixture to create a new user
            new_request_type_two (dict): fixture to create a new request type

        Returns:
             None
        """
        new_request_type_two.save()
        payload = {
            "subject": "new subject",
            "description": "new description",
            "requestTypeId": new_request_type_two.id
        }
        new_request_requester_update.requester_id = new_user.token_id
        new_request_requester_update.description = "description"
        new_request_requester_update.subject = "subject"
        new_request_requester_update.attachments = []
        new_request_requester_update.save()

        request_id = new_request_requester_update.id

        data = json.dumps(payload)
        response = client.patch(
            f'{V1_BASE_URL}/requests/{request_id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        response_data = response_json['data']
        history = History.query_().filter_by(
            resource_id=response_data['id']).first()

        assert history.resource_id == response_data['id']
        assert history.action == PERMISSION_TYPES['PATCH']

    def test_update_center_to_request_history_created_succeeds(
            self, client, init_db, auth_header, new_request_responder_update,
            new_request_user, new_user):
        """History is created when a responder updates a request assignee_id with success

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request_responder_update: request with the current user as the responder

        Returns:
             None
        """
        new_request_user.name = 'Mad Titan'
        new_request_user.center_id = new_request_responder_update.center_id
        new_request_user.save()

        payload = {"assigneeId": new_request_user.token_id}

        new_user.name = 'Thanos'
        new_request_responder_update.assignee_id = new_user.token_id
        new_request_responder_update.save()
        request_id = new_request_responder_update.id
        data = json.dumps(payload)
        response = client.patch(
            f'{V1_BASE_URL}/requests/{request_id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        response_data = response_json['data']
        history = History.query_().filter_by(
            resource_id=response_data['id']).first()

        assert history.resource_id == response_data['id']
        assert history.action == PERMISSION_TYPES['PATCH']
        assert history.activity == 'assignee changed from Mad Titan to Thanos'

    def test_delete_request_history_created_succeeds(self, client, auth_header,
                                                     new_request):
        """ Tests history created when delete request succeeds

        Args:
            client (obj): Fixture to get flask test client.
            auth_header (dict): Fixture to get token.
            request (obj): Fixture to create a new request.
        Return
            None
        """

        request = new_request.save()
        client.delete(
            f"{V1_BASE_URL}/requests/{request.id}", headers=auth_header)

        history = History.query_().filter_by(resource_id=request.id).first()

        assert history.resource_id == request.id
        assert history.action == PERMISSION_TYPES['DELETE']
        assert history.activity == HISTORY_MESSAGES['removed_resource']
