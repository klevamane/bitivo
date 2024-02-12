"""Tests for SSE publish on request update"""

import json
from unittest.mock import Mock
from config import AppConfig
from api.utilities.server_events import sse
from api.utilities.enums import RequestStatusEnum

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestSseUpdate:
    def test_sse_publish_on_inprogess_succeeds(self, init_db, client,
                                               new_request, auth_header,
                                               new_request_user,
                                               new_request_responder_update):
        """A responder updates a request status with success SSE is sent

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request_responder_update: request with the current user as the responder 
            new_request_user: Fixer to create a user who is to create a request
        Returns:
             None
        """
        new_request_user.save()
        data = json.dumps({
            "status": 'in progress',
        })
        new_request_responder_update.status = 'open'
        request_before_update = new_request_responder_update.save()
        request_id = request_before_update.id
        sse.publish = Mock()
        response = client.patch(
            f'{API_BASE_URL_V1}/requests/{request_id}',
            headers=auth_header,
            data=data)
        assert response.status_code == 200
        assert sse.publish.call_args[0][0].get("responderId")
        assert sse.publish.call_args[0][0].get("totalInProgressRequests") == 1
        del sse.publish

    def test_sse_publish_to_request_completed_succeeds(
        self, client, init_db, auth_header, new_request_responder_update,
            new_request_user):
        """A responder updates a request status with success SSE is sent

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request_responder_update: request with the current user as the responder
            new_request_user: Fixer to create a user who is to create a request
        Returns:
             None
        """
        new_request_user.save()
        data = json.dumps({
            "status": 'completed',
        })
        new_request_responder_update.status = 'in_progress'
        new_request_responder_update.save()
        self.request_id = new_request_responder_update.id
        sse.publish = Mock()
        response = client.patch(
            f'{API_BASE_URL_V1}/requests/{self.request_id}',
            headers=auth_header,
            data=data)
        assert response.status_code == 200
        assert sse.publish.call_args[0][0].get("responderId")
        assert sse.publish.call_args[0][0].get("totalCompletedRequests") == 1
        del sse.publish

    def test_sse_publish_to_request_closed_fails(
        self, client, init_db, auth_header, new_request_responder_update,
            new_request_user):
        """A responder updates a request to closed without success

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_request_responder_update: request with the current user as the responder
            new_request_user: Fixer to create a user who is to create a request
        Returns:
             None
        """
        new_request_user.save()
        data = json.dumps({
            "subject": "naruto",
            "description": "boruto",
            "status": RequestStatusEnum.closed.value
        })
        new_request_responder_update.status = RequestStatusEnum.in_progress
        new_request_responder_update.save()
        request_id = new_request_responder_update.id
        sse.publish = Mock()
        response = client.patch(
            f'{API_BASE_URL_V1}/requests/{request_id}',
            headers=auth_header,
            data=data)

        assert response.status_code == 400
        del sse.publish
