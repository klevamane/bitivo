"""module of tests for spaces edit endpoints
"""
from flask import json

from api.utilities.constants import CHARSET
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import (serialization_errors,
                                                   jwt_errors)
from tests.mocks.space import create_space_data

# app config
from config import AppConfig

api_v1_base_url = AppConfig.API_BASE_URL_V1


class TestEditSpaces:
    """
    Test for edit spaces endpoint
    """

    def test_edit_spaces_should_be_successful_when_all_conditions_are_met(
            self, client, init_db, auth_header, update_space, new_user):
        """
        Should return a 200 success code when an update is successful
        """
        new_user.save()
        update_space.save()
        data = json.dumps({
            "id": update_space.id,
            "name": "Andela Guest House"
        })
        response = client.patch(
            f'{api_v1_base_url}/spaces/{update_space.id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert response_json["message"] == SUCCESS_MESSAGES['updated'].format(
            'Space')
        assert "spaceType" in response_json['data']
        assert response_json['data']['name'] == "Andela Guest House"
        assert response_json["data"]['id'] == update_space.id
        assert response_json["data"]['parentId'] == update_space.parent_id
        assert 'spaceType' in response_json['data']
        assert response_json["data"]['spaceType'][
            'id'] == update_space.space_type_id

    def test_edit_spaces_should_fail_when_wrong_space_type_is_used(
            self, client, init_db, auth_header, update_space, new_space_types,
            new_spaces):
        """
        Should return a 400 status code when the wrong
        spaceType from the parent is tried to be updated
        """
        update_space.save()
        centers = new_spaces['centers']
        spaces = new_spaces['spaces']
        space_types = new_space_types

        data = json.dumps(
            create_space_data(
                id=update_space.id,
                name="Dojo",
                centerId=centers[0].id,
                spaceTypeId=space_types[3].id,
                parentId=spaces[0].id))
        space = space_types[0].type.lower()
        response = client.patch(
            f'{api_v1_base_url}/spaces/{update_space.id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'cannot_have_parent_type'].format(space)

    def test_edit_spaces_should_fail_when_the_same_name_is_provided(
            self, client, init_db, auth_header, update_space, new_space_types,
            new_spaces):
        """
        Should return a 409 error code when the same name 
        and parent id is being tried to be updated
        """
        update_space.save()
        centers = new_spaces['centers']
        spaces = new_spaces['spaces']
        space_types = new_space_types

        data = json.dumps(
            create_space_data(
                id=update_space.id,
                name="Ground Floor",
                centerId=centers[0].id,
                spaceTypeId=space_types[1].id,
                parentId=spaces[0].id))
        response = client.patch(
            f'{api_v1_base_url}/spaces/{update_space.id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 409
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'exists'].format('Space')

    def test_edit_space_should_fail_when_wrong_ids_are_used(
            self, client, init_db, auth_header, update_space, new_space_types,
            new_spaces):
        """
        Should return a 404 error code when
        wrong parentId and spaceTypeId are used
        """
        update_space.save()
        centers = new_spaces['centers']
        spaces = new_spaces['spaces']
        space_types = new_space_types

        data1 = json.dumps(
            create_space_data(
                id=update_space.id,
                name="Epic Tower",
                centerId=centers[0].id,
                spaceTypeId=spaces[0].id,
                parentId=spaces[0].id))
        data2 = json.dumps(
            create_space_data(
                id=update_space.id,
                name="Epic Tower",
                centerId=centers[0].id,
                spaceTypeId=space_types[1].id,
                parentId=space_types[1].id))
        response = client.patch(
            f'{api_v1_base_url}/spaces/{update_space.id}',
            headers=auth_header,
            data=data1)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json["status"] == "error"
        assert response_json['message'] == serialization_errors[
            'not_found'].format('Space type')

        response = client.patch(
            f'{api_v1_base_url}/spaces/{update_space.id}',
            headers=auth_header,
            data=data2)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json["status"] == "error"
        assert response_json['message'] == serialization_errors[
            'not_found'].format('Parent space')

    def test_edit_space_should_fail_update_with_a_wrong_center(
            self, client, init_db, auth_header, update_space, new_space_types,
            new_spaces):
        """
        Should return a 400 error code when the
        wrong centerID is used when updating
        """
        update_space.save()
        centers = new_spaces['centers']
        spaces = new_spaces['spaces']
        space_types = new_space_types

        data = json.dumps(
            create_space_data(
                id=update_space.id,
                name="Epic Tower",
                centerId=centers[1].id,
                spaceTypeId=space_types[1].id,
                parentId=spaces[0].id))

        response = client.patch(
            f'{api_v1_base_url}/spaces/{update_space.id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'centers_not_match']

    def test_edit_space_should_fail_when_authorization_token_is_not_provided(
            self, client, init_db, update_space):
        """
        Should return a 401 error code when authorization token is not provided
        """
        update_space.save()
        response = client.patch(f'{api_v1_base_url}/spaces/{update_space.id}')
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_edit_should_fail_when_invalid_id_is_used(
            self, client, init_db, auth_header, update_space):
        """
        Should return a 400 error code when
        invalid id is used when trying to update
        """
        update_space.save()
        response = client.patch(
            f'{api_v1_base_url}/spaces/1234!#', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors['invalid_id']

    def test_edit_spaces_should_pass_when_the_same_name_and_id_is_provided(
            self, client, init_db, auth_header, update_space, new_space_types,
            new_spaces):
        """
        Should return a 200 success code when the same name and id
        is updated
        """
        update_space.save()
        centers = new_spaces['centers']
        spaces = new_spaces['spaces']
        space_types = new_space_types

        data = json.dumps(
            create_space_data(
                id=update_space.id,
                name="Andela",
                centerId=centers[0].id,
                spaceTypeId=space_types[1].id,
                parentId=spaces[0].id))
        client.patch(
            f'{api_v1_base_url}/spaces/{update_space.id}',
            headers=auth_header,
            data=data)
        response = client.patch(
            f'{api_v1_base_url}/spaces/{update_space.id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert response_json["message"] == SUCCESS_MESSAGES['updated'].format(
            'Space')
        assert response_json["data"]['name'] == "Andela"
        assert response_json["data"]['id'] == update_space.id
        assert response_json["data"]['parentId'] == spaces[0].id
        assert 'spaceType' in response_json['data']
        assert response_json["data"]['spaceType']['id'] == space_types[1].id
        assert response_json["data"]['spaceType']['type'] == space_types[
            1].type
        assert response_json["data"]['spaceType']['color'] == space_types[
            1].color

    def test_edit_spaces_should_pass_when_the_centerid_is_not_provided(
            self, client, init_db, auth_header, update_space, new_space_types,
            new_spaces):
        """
        Should return a 200 success code when the centerId
        is not provided in the request
        """
        update_space.save()
        spaces = new_spaces['spaces']
        space_types = new_space_types

        data = json.dumps({
            "id": update_space.id,
            "name": "The Dojo",
            "spaceTypeId": space_types[1].id,
            "parentId": spaces[0].id
        })
        response = client.patch(
            f'{api_v1_base_url}/spaces/{update_space.id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert response_json["message"] == SUCCESS_MESSAGES['updated'].format(
            'Space')
        assert response_json["data"]['name'] == "The Dojo"
        assert response_json["data"]['id'] == update_space.id
        assert response_json["data"]['parentId'] == spaces[0].id
        assert 'spaceType' in response_json['data']
        assert response_json["data"]['spaceType']['id'] == space_types[1].id
        assert response_json["data"]['spaceType']['type'] == space_types[
            1].type
        assert response_json["data"]['spaceType']['color'] == space_types[
            1].color

    def test_edit_spaces_should_fail_when_updating_parentid_but_spacetypeid_is_not_provided(
            self, client, init_db, auth_header, update_space, new_space_types,
            new_spaces):
        """
        Should return a 400 erro code when the spaceTypeId
        is not provided in the request
        """
        update_space.save()
        spaces = new_spaces['spaces']

        data = json.dumps({"id": update_space.id, "parentId": spaces[0].id})
        response = client.patch(
            f'{api_v1_base_url}/spaces/{update_space.id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'provide_space_and_spacetype_id']

    def test_edit_spaces_should_fail_when_updating_spacetype_but_the_parentid_is_not_provided(
            self,
            client,
            init_db,
            auth_header,
            update_space,
            new_space_types,
    ):
        """
        Should return a 400 error code when the parentId
        is not provided but spacetype is provided
        """
        update_space.save()
        space_types = new_space_types

        data = json.dumps({
            "id": update_space.id,
            "name": "Andela Uganda",
            "spaceTypeId": space_types[2].id,
        })
        response = client.patch(
            f'{api_v1_base_url}/spaces/{update_space.id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'must_have_parent_space']

    def test_edit_spaces_should_fail_when_updating_same_name_with_same_centers_and_different_id(
            self, client, init_db, auth_header, new_spaces):
        """
        Should return a 409 error code when the same name and center
        being tried to be updated but with different id
        """

        spaces = new_spaces['spaces'][5]
        another_space = new_spaces['spaces'][0]

        data = json.dumps({
            "id": another_space.id,
            "name": new_spaces['spaces'][5].name
        })
        response = client.patch(
            f'{api_v1_base_url}/spaces/{another_space.id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 409
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'exists'].format('Space')

    def test_edit_spaces_should_fail_when_updating_space_with_children(
            self, client, init_db, auth_header, new_space_types, new_spaces):
        """
        Should return a 400 error code when editing space
        with children
        """

        spaces = new_spaces['spaces'][0]
        space_types = new_space_types

        data = json.dumps({
            "id": spaces.id,
            "parentId": new_spaces['spaces'][1].id,
            "spaceTypeId": space_types[2].id,
        })

        response = client.patch(
            f'{api_v1_base_url}/spaces/{spaces.id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'can_not_edit_parent']
