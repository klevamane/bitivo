"""Module for delete request endpoints."""

# Third party libraries
from flask import json

# constant
from api.utilities.constants import CHARSET

# Messages
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import (
    serialization_errors,
    database_errors,
)

# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestDeleteRequestEndpoint:
    """Class for request endpoints."""

    def test_delete_request_succeeds(self, client, auth_header, new_request):
        """ Tests delete request succeeds

        Args:
            client (obj): Fixture to get flask test client.
            auth_header (dict): Fixture to get token.
            request (obj): Fixture to create a new request.
        Return
            None
        """

        request = new_request.save()
        response = client.delete(
            f"{API_BASE_URL_V1}/requests/{request.id}", headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert response_json["message"] == SUCCESS_MESSAGES["deleted"].format(
            "Request")

    def test_delete_request_with_non_existing_request_id_fails(
            self, client, auth_header):
        """ Tests deleting request that does not exist fails

        Args:
            client (obj): Fixture to get flask test client.
            auth_header (dict): Fixture to get token.
        Return
            None
        """

        response = client.delete(
            f"{API_BASE_URL_V1}/requests/fake-id", headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json["status"] == "error"
        assert response_json["message"] == database_errors[
            "non_existing"].format("Request")

    def test_delete_with_already_deleted_request_fails(
            self, client, auth_header, new_request):
        """ Tests delete already deleted request fails

        Args:
            client (obj): Fixture to get flask test client.
            auth_header (dict): Fixture to get token.
            new_delete_request (obj): Fixture to create a new delete request.
        Return
            None

        """

        request = new_request.save()
        response = client.delete(
            f"{API_BASE_URL_V1}/requests/{request.id}", headers=auth_header)

        response = client.delete(
            f"{API_BASE_URL_V1}/requests/{request.id}", headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            "not_found"].format("Request")

    def test_delete_request_with_invalid_requester_id_fails(
            self, init_db, client, auth_header, open_request):
        """ Tests delete for invalid requester id fails

        Args:
            client (obj): Fixture to get flask test client.
            auth_header (dict): Fixture to get token.
            init_db (func): Initialises the database.
            open_request (obj): Fixture to create a new request.

        """

        request = open_request.save()
        response = client.delete(
            f"{API_BASE_URL_V1}/requests/{request.id}", headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 403
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'cannot_delete'].format('Request')

    def test_delete_in_progress_status_in_request_fails(
            self, init_db, client, auth_header, in_progress_request):
        """ Tests delete in-progress status in request fails

        Args:
            client (obj): Fixture to get flask test client.
            auth_header (dict): Fixture to get token.
            init_db (func): Initialises the database.
            in_progress_request (obj): Fixture to create a new request.

        """

        request = in_progress_request.save()
        response = client.delete(
            f"{API_BASE_URL_V1}/requests/{request.id}", headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 403
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'processed status'].format('Request')

    def test_delete_completed_status_in_request_fails(
            self, init_db, client, auth_header, completed_request):
        """ Tests delete in-progress status in request fails

        Args:
            client (obj): Fixture to get flask test client.
            auth_header (dict): Fixture to get token.
            init_db (func): Initialises the database.
            completed_request (obj): Fixture to create a new request.

        """

        request = completed_request.save()
        response = client.delete(
            f"{API_BASE_URL_V1}/requests/{request.id}", headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 403
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'processed status'].format('Request')

    def test_delete_closed_status_in_request_fails(
            self, init_db, client, auth_header, closed_request):
        """ Tests delete in-progress status in request fails

        Args:
            client (obj): Fixture to get flask test client.
            auth_header (dict): Fixture to get token.
            init_db (func): Initialises the database.
            closed_request (obj): Fixture to create a new request.

        """

        request = closed_request.save()
        response = client.delete(
            f"{API_BASE_URL_V1}/requests/{request.id}", headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 403
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'processed status'].format('Request')
