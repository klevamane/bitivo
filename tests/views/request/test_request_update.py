"""Tests for request update using PATCH http verb"""

# Standard Library
import json

# Local Module
from api.utilities.messages.error_messages import serialization_errors
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.constants import CHARSET
from api.utilities.enums import RequestStatusEnum
from api.utilities.messages.error_messages import request_errors
from api.utilities.json_parse_objects import json_parse_objects

from tests.mocks.user import (USER_DATA_VALID, USER_EMAIL_ALREADY_EXISTS,
                              USER_DATA_NEW)

# app config
from config import AppConfig
api_v1_base_url = AppConfig.API_BASE_URL_V1


class TestRequestUpdate:
    request_payload = {
        "subject": "naruto",
        "description": "boruto",
        "status": 'completed'
    }
    request_payload_with_invalid_attachments = {
        "subject": "naruto",
        "description": "boruto",
        "attachments": "attachments",
        "status": 'in progress'
    }
    request_payload_inprogress = {
        "subject": "naruto",
        "description": "boruto",
        "status": 'in progress',
    }

    def error_assertion(self, response, error_type, error_key, *args):
        """ Assets for test errors

        Args:
            response: Http response
            error_type (dict): The type of error to be asserted for
            error_key (string): Maps the error key in the error type dictionary
            *args: Variable number of arguments

        Returns:
            None
        """
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == error_type[error_key].format(*args)

    def test_requester_updates_a_request_center_id_that_is_open_fails(
            self, client, init_db, auth_header, new_request_requester_update,
            new_user):
        """A requester updates an open request's center id without success

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request_requester_update: request with the current user as the requester

        Returns:
             None
        """
        center_id = new_request_requester_update.center_id
        payload = {
            "subject": "naruto",
            "description": "boruto",
            "center_id": center_id
        }
        new_request_requester_update.requester_id = new_user.token_id
        new_request_requester_update.save()

        request_id = new_request_requester_update.id
        initial_status = new_request_requester_update.status

        data = json.dumps(payload)
        response = client.patch(
            f'{api_v1_base_url}/requests/{request_id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 403
        assert response_json['message'] == serialization_errors['request_center_update'].format(
            'center Id')
        assert response_json['status'] == 'error'

    def test_requester_updates_a_request_request_type_with_another_center_id_fails(
            self, client, init_db, auth_header, new_request_requester_update,
            new_user, new_request_type_three):
        """A requester fails to update a request with a request type having a different center id

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request_requester_update: request with the current user as the requester

        Returns:
             None
        """

        new_request_type_three.save()
        payload = {
            "subject": "naruto",
            "description": "boruto",
            "request_type_id": new_request_type_three.id
        }
        new_request_requester_update.requester_id = new_user.token_id
        new_request_requester_update.save()
        request_id = new_request_requester_update.id

        data = json.dumps(payload)
        response = client.patch(
            f'{api_v1_base_url}/requests/{request_id}',
            headers=auth_header,
            data=data)
        self.error_assertion(response, request_errors,
                             'request_update_request_type_center_mismatch')

    def test_requester_updates_a_request_request_type_succeeds(
            self, client, init_db, auth_header, new_request_requester_update,
            new_user, new_request_type_three):
        """A requester successfully updates the request - request type id

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request_requester_update: request with the current user as the requester
            new_request_type_three: fixture to create a new request type

        Returns:
             None
        """
        new_request_type_three.center_id = new_user.center_id
        new_request_type_three.save()
        payload = {"request_type_id": new_request_type_three.id}
        new_request_requester_update.requester_id = new_user.token_id
        new_request_requester_update.save()
        request_id = new_request_requester_update.id
        request_type_assignee_id = new_request_type_three.assignee_id

        data = json.dumps(payload)
        response = client.patch(
            f'{api_v1_base_url}/requests/{request_id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['message'] == SUCCESS_MESSAGES['edited'].format(
            'Request')
        assert response_json['status'] == 'success'
        assert response_json['data']['responder'][
            'tokenId'] == request_type_assignee_id

    def test_requester_updates_the_requester_id_of_a_request_request_that_is_open_fails(
            self, client, init_db, auth_header, new_request_requester_update,
            new_user, new_request_type_three, new_user_two):
        """A requester fails updates an open request with a requester id field

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request_requester_update: request with the current user as the requester

        Returns:
             None
        """

        new_request_type_three.save()
        payload = {
            "subject": "naruto",
            "description": "boruto",
            "requester_id": new_user_two.token_id
        }
        new_request_requester_update.requester_id = new_user.token_id
        new_request_requester_update.save()
        request_id = new_request_requester_update.id

        data = json.dumps(payload)
        response = client.patch(
            f'{api_v1_base_url}/requests/{request_id}',
            headers=auth_header,
            data=data)
        self.error_assertion(response, request_errors,
                             'You cannot update inaccessible field',
                             'requester id')

    def test_requester_updates_a_request_that_is_open_with_assignee_id_fails(
            self, client, init_db, auth_header, new_request_requester_update,
            new_user):
        """A requester updates an open request's assignee without success

        A requester updates a request that has its status not set to open,
        The request body is updated, but the request status and assignee_id
        is ignored. Therefore the user is unable to update the request status
        and the assignee_id

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request_requester_update: request with the current user as the requester

        Returns:
             None
        """
        new_user.save()
        payload = {
            "subject": "naruto",
            "description": "boruto",
            "assignee_id": new_user.token_id
        }
        new_request_requester_update.save()
        request_id = new_request_requester_update.id
        initial_status = new_request_requester_update.status

        data = json.dumps(payload)
        response = client.patch(
            f'{api_v1_base_url}/requests/{request_id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 403
        assert response_json['message'] == serialization_errors['request_assignee_update'].format(
            'assignee')
        assert response_json['status'] == 'error'

    def test_requester_updates_a_request_that_is_open_with_status_and_assignee_id_fails(
            self, client, init_db, auth_header, new_request_requester_update,
            new_user):
        """A requester updates an open request's  status and assignee without success

        A requester updates a request that has its status not set to open,
        A validation error is raised with status code 403


        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request_requester_update: request with the current user as the requester

        Returns:
             None
        """
        new_user.save()
        payload = {
            "subject": "naruto",
            "description": "boruto",
            "status": "in progress",
            "assignee_id": new_user.token_id
        }
        new_request_requester_update.save()
        request_id = new_request_requester_update.id
        initial_status = new_request_requester_update.status

        data = json.dumps(payload)
        response = client.patch(
            f'{api_v1_base_url}/requests/{request_id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 403
        assert response_json['message'] == serialization_errors['requester_two_fields'].format(
            'status','assignee')
        assert response_json['status'] == 'error'

    def test_requester_updates_a_request_that_is_open_with_status_and_center_id_fails(
            self, client, init_db, auth_header, new_request_requester_update,
            new_user, new_center):
        """A requester updates an open request's status and center without success

        A requester updates a request that has its status not set to open,
        A validation error is raised with status code 403

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request_requester_update: request with the current user as the requester

        Returns:
             None
        """
        new_user.save()
        payload = {
            "subject": "naruto",
            "description": "boruto",
            "status": "in progress",
            "center_id": new_center.id
        }
        new_request_requester_update.save()
        request_id = new_request_requester_update.id
        initial_status = new_request_requester_update.status

        data = json.dumps(payload)
        response = client.patch(
            f'{api_v1_base_url}/requests/{request_id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 403
        assert response_json['message'] == serialization_errors['requester_two_fields'].format(
            'status','center Id')
        assert response_json['status'] == 'error'

    def test_requester_updates_a_request_that_is_open_with_assignee_and_center_id_fails(
            self, client, init_db, auth_header, new_request_requester_update,
            new_user, new_center):
        """A requester updates an open request's assignee and center without success

        A requester updates a request that has its status not set to open,
        A validation error is raised with status code 403


        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request_requester_update: request with the current user as the requester

        Returns:
             None
        """
        new_user.save()
        new_center.save()
        payload = {
            "subject": "naruto",
            "description": "boruto",
            "assignee_id": new_user.token_id,
            "center_id": new_center.id
        }
        new_request_requester_update.save()
        request_id = new_request_requester_update.id
        initial_status = new_request_requester_update.status

        data = json.dumps(payload)
        response = client.patch(
            f'{api_v1_base_url}/requests/{request_id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 403
        assert response_json['message'] == serialization_errors['requester_two_fields'].format(
            'assignee','center Id')
        assert response_json['status'] == 'error'

    def test_requester_updates_a_request_that_is_open_with_status_assignee_and_center_id_fails(
            self, client, init_db, auth_header, new_request_requester_update,
            new_user, new_center):
        """A requester updates an open request's status, assignee, and center without success

        A requester updates a request that has its status not set to open,
        A validation error is raised with status code 403

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request_requester_update: request with the current user as the requester
            new_center: fixture to create new center

        Returns:
             None
        """
        new_user.save()
        new_center.save()
        payload = {
            "subject": "naruto",
            "description": "boruto",
            "status": "in progress",
            "assignee_id": new_user.token_id,
            "center_id": new_center.id
        }
        new_request_requester_update.save()
        request_id = new_request_requester_update.id
        initial_status = new_request_requester_update.status

        data = json.dumps(payload)
        response = client.patch(
            f'{api_v1_base_url}/requests/{request_id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 403
        assert response_json['message'] == serialization_errors['requester_three_fields'].format(
            'status', 'assignee','center Id')
        assert response_json['status'] == 'error'


    def test_requester_updates_a_the_request_status_fails(
            self, client, init_db, auth_header, new_request_requester_update):
        """A requester updates a request status without success

        The request status upon update is ignored, therefore disabling
        the ability of a requester to be able to update a request status

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request_requester_update: request with the current user as the requester

        Returns:
             None
        """
        new_request_requester_update.save()
        request_id = new_request_requester_update.id
        initial_status = new_request_requester_update.status

        data = json.dumps(self.request_payload)
        response = client.patch(
            f'{api_v1_base_url}/requests/{request_id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 403
        assert response_json['message'] == serialization_errors['request_status_update'].format(
            'status')
        assert response_json['status'] == 'error'


    def test_a_requester_closes_a_request_that_is_not_completed_fails(
            self, init_db, client, auth_header, new_request_requester_update):

        new_request_requester_update.status = "in_progress"
        new_request_requester_update.save()
        request_id = new_request_requester_update.id

        data = json.dumps(self.request_payload)
        response = client.patch(
            f'{api_v1_base_url}/requests/{request_id}',
            headers=auth_header,
            data=data)

        self.error_assertion(response, request_errors, 'requester_no_update',
                             RequestStatusEnum.in_progress.value)

    def test_a_requester_closes_a_request_a_completed_succeeds(
            self, init_db, client, auth_header, new_request_requester_update):
        payload = {
            "subject": "naruto",
            "description": "boruto",
            "status": RequestStatusEnum.closed.value
        }
        new_request_requester_update.status = RequestStatusEnum.completed.value
        new_request_requester_update.save()
        request_id = new_request_requester_update.id

        data = json.dumps(payload)
        response = client.patch(
            f'{api_v1_base_url}/requests/{request_id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['message'] == SUCCESS_MESSAGES['edited'].format(
            'Request')
        assert response_json['data']['closedAt'] is not None
        assert response_json['data'][
            'status'] == RequestStatusEnum.closed.value

    def test_a_requester_updates_a_request_with_invalid_attachments_data(
            self, init_db, client, auth_header, new_request_requester_update):
        new_request_requester_update.status = RequestStatusEnum.completed.value
        new_request_requester_update.save()
        request_id = new_request_requester_update.id

        data = json.dumps(self.request_payload_with_invalid_attachments)
        response = client.patch(
            f'{api_v1_base_url}/requests/{request_id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_data_type']

    def test_a_responder_add_assignee_to_request_succeeds(
            self, client, init_db, auth_header, new_request_responder_update,
            new_request_user, new_user):
        """A responder updates a request assignee_id with success

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request_responder_update: request with the current user as the responder

        Returns:
             None
        """
        new_request_user.center_id = new_request_responder_update.center_id
        new_request_user.save()
        payload = {"assigneeId": new_request_user.token_id}

        new_request_responder_update.save()
        request_id = new_request_responder_update.id
        data = json.dumps(payload)
        response = client.patch(
            f'{api_v1_base_url}/requests/{request_id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['message'] == SUCCESS_MESSAGES['edited'].format(
            'Request')

        assert response_json['data']['status'] == RequestStatusEnum.open.value
        assert response_json['data']['attachments'] == json_parse_objects(
            new_request_responder_update.attachments, 'loads')

        assert response_json['data']['assignee'][
            'tokenId'] == new_request_user.token_id

    def test_a_responder_updates_a_request_status_succeeds(
            self, client, init_db, auth_header, new_request_responder_update,
            new_request_user):
        """A responder updates a request status with success

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request_responder_update: request with the current user as the responder

        Returns:
             None
        """
        new_request_user.save()
        payload_inprogress = {
            "status": "in progress",
        }

        new_request_responder_update.assignee_id = new_request_user.token_id
        new_request_responder_update.save()
        request_id = new_request_responder_update.id

        data = json.dumps(payload_inprogress)
        response = client.patch(
            f'{api_v1_base_url}/requests/{request_id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['message'] == SUCCESS_MESSAGES['edited'].format(
            'Request')
        assert response_json['data']['inProgressAt'] is not None
        assert response_json['data'][
            'status'] == RequestStatusEnum.in_progress.value

    def test_a_responder_updates_a_request_status_to_closed_fails(
            self, client, init_db, auth_header, new_request_responder_update):
        """A responder updates a request to closed without success

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request_responder_update: request with the current user as the responder

        Returns:
             None
        """

        payload = {
            "subject": "naruto",
            "description": "boruto",
            "status": RequestStatusEnum.closed.value
        }
        new_request_responder_update.status = RequestStatusEnum.in_progress
        new_request_responder_update.save()
        request_id = new_request_responder_update.id
        data = json.dumps(payload)
        response = client.patch(
            f'{api_v1_base_url}/requests/{request_id}',
            headers=auth_header,
            data=data)

        self.error_assertion(response, request_errors, 'cannot_close_request',
                             'Status')

    def test_a_responder_updates_a_completed_request_fails(
            self, client, init_db, auth_header, new_request_responder_update,
            new_user):
        """A responder fails in updating a request with a completed status

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request_responder_update: request with the current user as the responder

        Returns:
             None
                """
        payload = {
            "subject": "value",
            "description": "chain",
            "status": "in progress"
        }
        new_request_responder_update.status = RequestStatusEnum.completed.value
        new_request_responder_update.save()
        request_id = new_request_responder_update.id

        data = json.dumps(payload)
        response = client.patch(
            f'{api_v1_base_url}/requests/{request_id}',
            headers=auth_header,
            data=data)

        self.error_assertion(response, request_errors, 'cannot_update',
                             RequestStatusEnum.completed.value)

    def test_requester_updates_a_request_that_is_not_opened_fails(
            self, client, init_db, auth_header, new_request_requester_update,
            new_user_two, new_request_type):
        """A requester updates a request without success

        A requester updates a request that has its status not set to open

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request_requester_update: request with the current user as the requester

        Returns:
             None
        """
        new_request_requester_update.status = RequestStatusEnum.closed.value
        new_user_two.center_id = new_request_requester_update.center_id
        new_user_two.save()
        new_request_type.assignee_id = new_user_two.token_id
        new_request_type.save()
        new_request_requester_update.request_type_id = new_request_type.id
        new_request_requester_update.save()
        request_id = new_request_requester_update.id
        data = json.dumps(self.request_payload)
        response = client.patch(
            f'{api_v1_base_url}/requests/{request_id}',
            headers=auth_header,
            data=data)

        self.error_assertion(response, request_errors, 'requester_no_update',
                             new_request_requester_update.status.value)

    def test_a_responder_updates_a_request_body_in_progress_without_status_field_fails(
            self, client, init_db, auth_header, new_request_responder_update,
            new_request_type, new_user):
        """A responder updates a request with missing status without success

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request_responder_update: request with the current user as the responder

        Returns:
             None
        """
        payload = {"subject": "naruto", "description": "boruto"}
        new_request_type.assignee_id = new_user.token_id
        new_request_type.save()
        new_request_responder_update.request_type_id = new_request_type.id
        new_request_responder_update.status = "in_progress"
        new_request_responder_update.save()
        request_id = new_request_responder_update.id

        data = json.dumps(payload)
        response = client.patch(
            f'{api_v1_base_url}/requests/{request_id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))
        self.error_assertion(response, serialization_errors,
                             'missing_input_field', 'Status')

    def test_a_responder_changes_the_status_of_a_request_in_progress_to_open_fails(
            self, client, init_db, auth_header, new_request_responder_update):
        """A responder updates a request with missing status without success

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request_responder_update: request with the current user as the responder

        Returns:
             None
        """
        payload = {
            "subject": "naruto",
            "description": "boruto",
            "status": 'open'
        }
        new_request_responder_update.status = RequestStatusEnum.in_progress
        new_request_responder_update.save()
        status = new_request_responder_update.status
        request_id = new_request_responder_update.id

        data = json.dumps(payload)
        response = client.patch(
            f'{api_v1_base_url}/requests/{request_id}',
            headers=auth_header,
            data=data)

        self.error_assertion(response, request_errors, 'cannot_change',
                             status.value, RequestStatusEnum.open.value)

    def test_a_user_is_the_requester_and_responder_of_the_same_request_fails(
            self, client, init_db, auth_header, new_request):
        """A responder updates a request with missing status without success

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request: request with the current user as the requester and the
                responder

        Returns:
             None
        """
        payload = {
            "subject": "naruto",
            "description": "boruto",
            "status": RequestStatusEnum.open.value
        }

        new_request.save()
        request_id = new_request.id

        data = json.dumps(payload)
        response = client.patch(
            f'{api_v1_base_url}/requests/{request_id}',
            headers=auth_header,
            data=data)

        self.error_assertion(response, request_errors,
                             'cannot_be_requester_responder')

    def test_a_responder_add_assignee_that_does_not_exist_fails(
            self, client, init_db, auth_header, new_user,
            new_request_responder_update, new_request_user):
        """A responder fails updates a request assignee_id

        The responder fails to update a request assignee_id by using an
        assignee_id that does not exist

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user (dict): fixture to create a new user
            new_request_responder_update (dict): fixture to create a
            request with the current user as the responder

        Returns:
             None
        """
        new_user.save()
        new_request_user.save()

        request_payload2 = {"assigneeId": '-LU2NFHxjdft7uRWMH5Yn'}
        new_request_responder_update.save()
        request_id = new_request_responder_update.id
        data = json.dumps(request_payload2)
        response = client.patch(
            f'{api_v1_base_url}/requests/{request_id}',
            headers=auth_header,
            data=data)

        self.error_assertion(response, serialization_errors,
                             'generic_not_found', 'Assignee')

    def test_a_responder_add_assignee_that_does_not_belong_to_request_center_fails(
            self, client, init_db, auth_header, new_user,
            new_request_responder_update, test_center_with_users):
        """A responder fails updates a request assignee_id

        The responder fails to update a request assignee_id by using an
        assignee_id that does not exist

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user (dict): fixture to create a new user
            new_request_responder_update (dict): fixture to create a
            request with the current user as the responder

        Returns:
             None
        """

        test_center_with_users.save()
        new_user.save()

        request_payload2 = {"assigneeId": new_user.token_id}
        new_request_responder_update.center_id = test_center_with_users.id
        new_request_responder_update.save()
        request_id = new_request_responder_update.id
        data = json.dumps(request_payload2)
        response = client.patch(
            f'{api_v1_base_url}/requests/{request_id}',
            headers=auth_header,
            data=data)

        self.error_assertion(response, serialization_errors, 'user_not_found',
                             'Assignee')

    def test_a_responder_updates_a_request_to_completed_succeeds(
            self, client, init_db, auth_header, new_request_responder_update,
            new_request_user):
        """A responder updates a request status with success

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request_responder_update: request with the current user as the responder

        Returns:
             None
        """
        new_request_user.save()
        payload_inprogress = {
            "status": 'completed',
        }
        new_request_responder_update.status = 'in_progress'
        new_request_responder_update.save()
        request_id = new_request_responder_update.id

        data = json.dumps(payload_inprogress)
        response = client.patch(
            f'{api_v1_base_url}/requests/{request_id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['message'] == SUCCESS_MESSAGES['edited'].format(
            'Request')
        assert response_json['data']['completedAt'] is not None
        assert response_json['data'][
            'status'] == RequestStatusEnum.completed.value

    def test_a_responder_updates_a_request_to_in_progress_succeeds(
            self, client, init_db, auth_header, new_request_responder_update,
            new_request_user):
        """A responder updates a request status with success

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request_responder_update: request with the current user as the responder

        Returns:
             None
        """
        new_request_user.save()
        payload_inprogress = {
            "status": 'in progress',
        }
        new_request_responder_update.status = 'open'
        request_before_update = new_request_responder_update.save()
        request_id = request_before_update.id

        data = json.dumps(payload_inprogress)
        response = client.patch(
            f'{api_v1_base_url}/requests/{request_id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['message'] == SUCCESS_MESSAGES['edited'].format(
            'Request')
        assert response_json['data']['dueBy'] is not None
        assert response_json['data'][
            'status'] == RequestStatusEnum.in_progress.value
