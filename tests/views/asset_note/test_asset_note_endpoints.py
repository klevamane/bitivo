"""module of tests for asset note endpoints
"""
# Third-party libraries
from flask import json

# Constants
from api.utilities.constants import CHARSET

# Models
from api.models import AssetNote

# Messages
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import (serialization_errors,
                                                   filter_errors, jwt_errors, database_errors)

# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestAssetNoteEndpoints:

    def test_delete_assete_note_succeeds(self, client, auth_header, init_db,
                                         new_asset_note):
        """ Tests delete asset note succeeds

            Args:
                client (object): Fixture to get flask test client.
                auth_header (dict): Fixture to get token.
                init_db (func): Initialises the database.
                new_comment (object): Fixture to create a new asset note.

            """

        asset_note = new_asset_note.save()
        response = client.delete(
            f'{API_BASE_URL_V1}/notes/{asset_note.id}', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['deleted'].format(
            'Asset note')

    def test_delete_asset_note_with_non_existing_id_fails(
            self, client, auth_header, init_db):
        """ Tests delete comment fails

        Args:
            client (object): Fixture to get flask test client.
            auth_header (dict): Fixture to get token.
            init_db (object): Used to create the database structure using the models.

        """

        response = client.delete(
            f'{API_BASE_URL_V1}/notes/fkndhinknef4nj', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == database_errors[
            'non_existing'].format('Asset note')
