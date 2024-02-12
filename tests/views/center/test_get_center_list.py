"Module for asset category endpoint test"

from flask import json  # pylint: disable=E0401

from api.utilities.constants import CHARSET
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import jwt_errors
from tests.mocks.center import NEW_CENTER

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1  # pylint: disable=C0103


class TestCenterEndpoints:  # pylint: disable=R0904
    """"
    Centers endpoints test
    """

    def test_get_centers_empty_list(  # pylint: disable=R0201,C0103
            self,
            client,
            init_db,  # pylint: disable=W0613
            auth_header_two):
        """
        Should return an empty list if no centers were found
        """
        response = client.get(f'{BASE_URL}/centers', headers=auth_header_two)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"

        assert response_json["data"]
        assert response_json["message"] == SUCCESS_MESSAGES["fetched"].format(
            "Centers")

    def test_get_centers_fails_without_permissions(
            self, client, init_db, auth_header, request_ctx,
            mock_request_two_obj_decoded_token, new_user, default_role):
        default_role.save()
        new_user.save()
        new_user.update_(role_id=default_role.id)
        response = client.get(f'{BASE_URL}/centers', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200

    def test_get_centers_response_data(  # pylint: disable=R0201,C0103
            self,
            client,
            new_custom_center,
            init_db,  # pylint: disable=W0613
            auth_header_two, new_user,
            new_role):
        """A method that tests centers list response data"""
        new_role.save()
        new_user.save()
        new_user.update_(role_id=new_role.id)
        new_center = new_custom_center(NEW_CENTER)
        new_center.save()
        response = client.get(f'{BASE_URL}/centers', headers=auth_header_two)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert isinstance(response_json["data"], list)
        assert len(response_json["data"]) is not 0
        assert response_json["data"][0]["name"] == new_center.name
        assert isinstance(response_json["data"][0]["image"], object)
        assert response_json["data"][0]["image"]["url"] == new_center.image[
            'url']
        assert response_json["data"][0]["staffCount"] == 0
        assert response_json["message"] == SUCCESS_MESSAGES["fetched"].format(
            "Centers")

    def test_get_centers_unauthorized(  # pylint: disable=R0201,C0103
            self,
            client,
            init_db  # pylint: disable=W0613
    ):
        """
        Should return jwt error when no token was provided in request
        """
        response = client.get(f'{BASE_URL}/centers')

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json["status"] == "error"
        assert "data" not in response_json
        assert response_json["message"] == jwt_errors['NO_TOKEN_MSG']

    def test_get_filtered_centers(  # pylint: disable=R0201,C0103
            self,
            client,
            new_custom_center,
            init_db,  # pylint: disable=W0613
            auth_header_two):
        """A method that tests get_centers with query"""
        new_center = new_custom_center(NEW_CENTER)
        new_center.save()
        response = client.get(
            f'{BASE_URL}/centers?where=name,like,andela', headers=auth_header_two)
        empty_response = client.get(
            f'{BASE_URL}/centers?where=name,like,shdfjhsjd',
            headers=auth_header_two)

        response_json = json.loads(response.data.decode(CHARSET))
        empty_response_json = json.loads(empty_response.data.decode(CHARSET))

        assert response_json["data"][0]["name"] == new_center.name
        assert response_json["data"][0]["image"]["url"] == new_center.image[
            'url']

        assert not empty_response_json["data"]
        assert empty_response.status_code == 200
        assert empty_response_json["status"] == "success"
        assert empty_response_json["message"] == SUCCESS_MESSAGES[
            "fetched"].format("Centers")

    def test_get_deleted_centers_with_params(  # pylint: disable=R0201,C0103
            self,
            client,
            test_center,
            init_db,  # pylint: disable=W0613
            auth_header_two,
            new_user):
        """A method that tests getting deleted centers"""
        test_center.save()
        new_user.save()
        res = client.delete(
            f'{BASE_URL}/centers/{test_center.id}', headers=auth_header_two)
        response = client.get(
            f'{BASE_URL}/centers?include=deleted', headers=auth_header_two)
        response_json = json.loads(response.data.decode(CHARSET))
        res_json = json.loads(res.data.decode(CHARSET))

        assert res.status_code == 200
        assert res_json['status'] == 'success'
        assert res_json['message'] == SUCCESS_MESSAGES[
            'center_deleted'].format(test_center.name)

        assert response.status_code == 200

        assert response_json["status"] == "success"
        assert isinstance(response_json["data"], list)
        assert len(response_json["data"]) > 0
        assert response_json["data"][0]["name"] == test_center.name

        # assert that deleted field in included in returned data
        assert response_json["data"][0]["deleted"] is True
        assert isinstance(response_json["data"][0]["image"], object)
        assert response_json["data"][0]["image"]["url"] == test_center.image[
            'url']
        assert response_json["data"][0]["staffCount"] == 0
        assert response_json["message"] == SUCCESS_MESSAGES["fetched"].format(
            "Centers")

    def test_get_deleted_users_in_a_center_with_params(  # pylint: disable=R0201,C0103
            self,
            client,
            test_center_with_deleted_users,
            init_db,  # pylint: disable=W0613
            auth_header_two):
        """A method that tests getting deleted users in a center"""

        test_center_with_deleted_users.save()

        response = client.get(
            f'{BASE_URL}/centers/{test_center_with_deleted_users.id}/people?include=deleted',
            headers=auth_header_two)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200

        assert response_json["status"] == "success"
        assert isinstance(response_json["data"], list)
        assert len(response_json["data"]) > 0
        for user in response_json["data"]:
            # assert that deleted field in included in returned data
            # assert that email in returned users
            assert user['deleted'] is True
            assert isinstance(user["email"], str)
            assert isinstance(user["imageUrl"], str)
            assert isinstance(user["tokenId"], str)

        assert response_json["message"] \
            == SUCCESS_MESSAGES["get_center_people"].format(test_center_with_deleted_users.name)
