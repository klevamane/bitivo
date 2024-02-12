"""
Module of tests for permission endpoints
"""

from flask import json

from api.models.permission import Permission
from api.utilities.constants import CHARSET
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import (serialization_errors,
                                                   jwt_errors)
from tests.mocks.permission import (
    VALID_PERMISSION_DATA, PERMISSION_DATA_WITH_INVALID_TYPE,
    PERMISSION_DATA_WITH_EMPTY_TYPE, PERMISSION_WITH_NO_TYPE)

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1


class TestPermissionPostEndpoints:
    """
    Test Permission resource POST endpoint
    """

    def test_create_permission_with_valid_data_succeeds(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            new_user):
        """
        Test successfully creating a permission
        """
        new_user.save()
        data = json.dumps(VALID_PERMISSION_DATA)
        response = client.post(
            f'{BASE_URL}/permissions', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 201
        assert response_json["status"] == "success"
        assert response_json["message"] == \
            SUCCESS_MESSAGES['created'].format('Permission')

    def test_create_permission_with_invalid_type_fails(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            new_user):
        """
        Test create permission when permission type is an invalid character
        like '-'
        """
        new_user.save()
        data = json.dumps(PERMISSION_DATA_WITH_INVALID_TYPE)
        response = client.post(
            f'{BASE_URL}/permissions', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["errors"]["type"][0] == \
            serialization_errors['string_characters']

    def test_create_permission_with_empty_type_fails(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header):
        """
        Test create permission when permission type is blank/empty
        """
        data = json.dumps(PERMISSION_DATA_WITH_EMPTY_TYPE)
        response = client.post(
            f'{BASE_URL}/permissions', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["errors"]["type"][0] == \
            serialization_errors['not_empty']

    def test_create_permissions_with_duplicate_type_fails(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header):
        """
        Test create duplicate permission
        """
        data = json.dumps(VALID_PERMISSION_DATA)
        response = client.post(
            f'{BASE_URL}/permissions', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 409
        assert response_json["status"] == "error"
        assert response_json["message"] == \
            serialization_errors["exists"].format("Permission")

    def test_create_permissions_with_no_type_field_fails(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header):
        """
        Test create permission when type is not provided in response body
        """
        data = json.dumps(PERMISSION_WITH_NO_TYPE)
        response = client.post(
            f'{BASE_URL}/permissions', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["errors"]["type"][0] == \
            serialization_errors['field_required']

    def test_create_permission_no_token_fails(self, client, init_db):
        """
        Test create duplicate permission
        """
        data = json.dumps(VALID_PERMISSION_DATA)
        response = client.post(f'{BASE_URL}/permissions', data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json["status"] == "error"
        assert response_json["message"] == jwt_errors["NO_TOKEN_MSG"]
