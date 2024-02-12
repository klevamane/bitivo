"""
Module of tests for  request types activity tracker
"""
# system imports
import json

# models
from api.models import History

# Constant
from api.utilities.constants import CHARSET

# Mocks
from tests.mocks.request_type import VALID_REQUEST_TYPE_DATA, VALID_REQUEST_TYPE_UPDATE_DATA

# messages
from api.utilities.messages.success_messages import HISTORY_MESSAGES
from api.utilities.constants import PERMISSION_TYPES

from config import AppConfig
V1_BASE_URL = AppConfig.API_BASE_URL_V1

class TestRequestTypesActivityTracker:
    """Tests for request types activity tracker
    """

    def test_create_request_type_history_created_succeed(  # pylint: disable=C0103
            self,
            client,
            init_db,  # pylint: disable=W0613
            auth_header,
            new_user):
        """
        Tests history created when request types is created.

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_user (dict): fixture to create a new user

        """
        new_user.save()
        VALID_REQUEST_TYPE_DATA['assigneeId'] = new_user.token_id
        VALID_REQUEST_TYPE_DATA['centerId'] = new_user.center_id
        data = json.dumps(VALID_REQUEST_TYPE_DATA)
        response = client.post(
            f'{V1_BASE_URL}/request-types', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data']
        history = History.query_().filter_by(
            resource_id=response_data['id']).first()

        assert history.resource_id == response_data['id']
        assert history.action == PERMISSION_TYPES['POST']
        assert history.activity == HISTORY_MESSAGES['added_resource']

    def test_update_request_type_history_created_succeeds(
            self, client, auth_header, new_request_type, new_user_two,
            new_center):
        """
        Tests history created when request type is updated

        Args:
            client (FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get token
            new_request_type2 (dict): fixture to create a new_request_type
        """
        new_center.save()
        new_user_two.center_id = new_center.id
        new_user_two.save()
        new_request_type.save()
        request_type_id = new_request_type.id
        valid_request_type_data = dict(**VALID_REQUEST_TYPE_UPDATE_DATA)
        valid_request_type_data['assigneeId'] = new_user_two.token_id
        valid_request_type_data['centerId'] = new_user_two.center_id
        valid_request_type_data['resolutionTime'] = {"minutes": 1}
        data = json.dumps(valid_request_type_data)
        response = client.patch(
            f'{V1_BASE_URL}/request-types/{request_type_id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        response_data = response_json['data']
        history = History.query_().filter_by(
            resource_id=response_data['id']).first()

        assert history.resource_id == response_data['id']
        assert history.action == PERMISSION_TYPES['PATCH']

    def test_update_request_type_assignee_history_created_succeeds(
            self, client, auth_header, duplicate_request_type, second_user):
        """history created when assignee id is updated

        Args:
            client (FlaskClient): fixture to get flask test client
            auth_header (dict): fixture to get token
            duplicate_request_type (dict): fixture to create a new_request_type
            second_user(dict): fixture to create another user

        """
        duplicate_request_type.resolution_time = {
            "days": 10,
            "hours": 4,
            "minutes": 1
        }
        duplicate_request_type.save()

        second_user.center_id = duplicate_request_type.center_id
        second_user.save()
        request_type_id = duplicate_request_type.id
        valid_request_type_data = dict(**VALID_REQUEST_TYPE_UPDATE_DATA)
        valid_request_type_data['assigneeId'] = second_user.token_id
        valid_request_type_data['centerId'] = duplicate_request_type.center_id
        valid_request_type_data['resolutionTime'] = {
            "days": 10,
            "hours": 4,
            "minutes": 1
        }
        data = json.dumps(valid_request_type_data)
        response = client.patch(
            f'{V1_BASE_URL}/request-types/{request_type_id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data']
        history = History.query_().filter_by(
            resource_id=response_data['id']).first()

        assert history.resource_id == response_data['id']
        assert history.action == PERMISSION_TYPES['PATCH']
        assert history.activity == 'assignee changed from Sunday to Mary'

    def test_delete_request_type_history_created_succeeds(
            self, client, auth_header, init_db, new_request_type):
        """
        Tests history created when request type is deleted

         Args:
            client (object): Fixture to get flask test client
            auth_header (dict): Fixture to get token
            init_db (object): Used to create the database structure using the models
            new_request_type (object): Fixture to create a new request type

        Returns:
            None
        """
        request_type = new_request_type.save()

        client.delete(
            f'{V1_BASE_URL}/request-types/{request_type.id}',
            headers=auth_header)
        history = History.query_().filter_by(
            resource_id=request_type.id).first()
        assert history.resource_id == request_type.id
        assert history.action == PERMISSION_TYPES['DELETE']
        assert history.activity == HISTORY_MESSAGES['removed_resource']
