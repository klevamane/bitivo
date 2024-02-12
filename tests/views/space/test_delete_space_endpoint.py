"""
    Module for delete space endpoint tests
"""
from flask import json

from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import (database_errors, jwt_errors,
                                                   serialization_errors)
from api.utilities.constants import CHARSET

# app config
from config import AppConfig

API_V1_BASE_URL = AppConfig.API_BASE_URL_V1


class TestDeleteSpaceEndPoint:
    """
    Tests for the deletespace endpoint
    """

    def test_delete_space_succeeds_for_space_with_no_children(
            self, init_db, client, auth_header, new_center, custom_space_type,
            custom_space, new_user):  # pylint: disable=R0913
        """
        Tests delete space succeeds when a space has no children

        Parameters:
            client (object): Fixture to get flask test client
            auth_header (dict): Fixture to get token
            init_db (object): Used to create the database structure using the models
            new_center (object): Fixture to create a new center
            custom_space_type (object): Fixture to create and save a custom space_type
            custom_space (object): Fixture to create and save a new space
        """
        new_user.save()
        new_center.save()

        space_type = custom_space_type({'type': 'floor', 'color': 'yellow'})

        #create a new Space without children
        parent_space = custom_space({
            'name': "First",
            'center_id': new_center.id,
            'space_type_id': space_type.id,
            'created_by': new_user.token_id
        })
        response = client.delete(
            f'{API_V1_BASE_URL}/spaces/{parent_space.id}', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES["deleted"].format(
            "Space")

    def test_delete_space_fails_for_space_with_children(
            self, init_db, client, auth_header, new_center, custom_space_type,
            custom_space):  # pylint: disable=R0913
        """
        Test delete space fails when a space has children

        Parameters:
            client (object): Fixture to get flask test client
            auth_header (dict): Fixture to get token
            init_db (object): Used to create the database structure using the models
            new_center (object): Fixture to create a new center
            custom_space_type (object): Fixture to create and save a custom space_type
            custom_space (object): Fixture to create and save a new space
        """
        new_center.save()

        space_types_data = [('Building', 'Red'), ('Wing', 'Blue')]

        space_types = [
            custom_space_type({
                'type': data[0],
                'color': data[1]
            }) for data in space_types_data
        ]

        #create a new Space without children
        parent_space = custom_space({
            'name': "Second",
            'center_id': new_center.id,
            'space_type_id': space_types[0].id
        })

        #create a child for the parent space
        custom_space({
            'name': "Second",
            'center_id': new_center.id,
            'space_type_id': space_types[1].id,
            'parent_id': parent_space.id
        })

        response = client.delete(
            f'{API_V1_BASE_URL}/spaces/{parent_space.id}', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 403
        assert response_json['status'] == 'error'
        assert response_json['message'] == database_errors[
            "model_delete_children"].format("Space", "child space(s)")

    def test_delete_space_fails_for_no_token_supplied(self, client):
        """
        Test delete space fails when no token is supplied

        Parameters:
            client (object): fixture to get flask test client
        """

        response = client.delete(
            f'{API_V1_BASE_URL}/spaces/-LL9ab1iJLjgPNqHQ0Ha')

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']
        assert response_json['status'] == 'error'

    def test_delete_space_fails_for_invalid_space_id(self, client,
                                                     auth_header):
        """
        Test delete space fails when the space id contains invalid
        characters such as #@8

        Parameters:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
        """

        response = client.delete(
            f'{API_V1_BASE_URL}/spaces/!#ffsfgs8L', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['message'] == serialization_errors['invalid_id']
        assert response_json['status'] == 'error'

    def test_delete_space_fails_for_non_existing_space(self, client,
                                                       auth_header):
        """
        Test delete space fails when deleting a space not existing
        in the Database

        Parameters:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
        """

        response = client.delete(
            f'{API_V1_BASE_URL}/spaces/L3dfgr123L', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['message'] == database_errors[
            'non_existing'].format("Space")
        assert response_json['status'] == 'error'

    def test_delete_space_fails_for_already_deleted_space(
            self, client, auth_header, new_center, custom_space_type,
            custom_space, new_user):
        """
        Test delete space fails when deleting a space already deleted
        from the Database

        Parameters:
            client (object): Fixture to get flask test client
            auth_header (dict): Fixture to get token
            new_center (object): Fixture to create a new center
            custom_space_type (object): Fixture to create and save a custom space_type
            custom_space (object): Fixture to create and save a new space
        """
        new_user.save()
        space_type = custom_space_type({'type': 'block', 'color': 'pink'})

        #create a new Space without children
        parent_space = custom_space({
            'name': "Tenth",
            'center_id': new_center.id,
            'space_type_id': space_type.id,
            'created_by': new_user.token_id
        })

        #delete the space
        client.delete(
            f'{API_V1_BASE_URL}/spaces/{parent_space.id}', headers=auth_header)

        #delete the same space
        response = client.delete(
            f'{API_V1_BASE_URL}/spaces/{parent_space.id}', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['message'] == database_errors[
            'non_existing'].format("Space")
        assert response_json['status'] == 'error'
