"""Module for testing updating an asset note """
from config import AppConfig
from flask import json


from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import serialization_errors, jwt_errors
from api.utilities.constants import CHARSET

from tests.mocks.asset_note import ASSET_NOTE_DATA

# app config
API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestUpdateAssetNote:
    """Class for testing the update asset note resource """

    def test_update_asset_note_succeeds(
            self, auth_header, client, new_asset_note):
        """
        Tests successfully updating an asset note
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            new_asset_repair_log: Fixture to create an asset repair
            log in the database
          Returns:
            None
        """
        new_asset_note.save()
        note_id = new_asset_note.id
        update_data = ASSET_NOTE_DATA
        data = json.dumps(update_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/notes/{note_id}', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert isinstance(response_json['data'], dict)
        assert response_json['status'] == 'success'
        assert response_json['data']['title'] == update_data['title']
        assert response_json['data']['body'] == update_data['body']
        assert response_json['message'] == SUCCESS_MESSAGES['updated'].format(
            'Asset note')

    def test_update_asset_note_no_token_fails(
            self, client, new_asset_note):
        """
        Tests updating an asset note without an authentication token
        Args:
            client (func): Flask test client
            new_asset_note: Fixture to create an asset repair
            log in the database
        Returns: None
        """
        new_asset_note.save()
        note_id = new_asset_note.id
        update_data = ASSET_NOTE_DATA
        data = json.dumps(update_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/notes/{note_id}', data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_update_asset_note_invalid_note_id_fails(
            self, auth_header, client, new_asset_note):
        """
        Tests updating an asset note with an invalid note id
        Args:
            client (func): Flask test client
            auth_header (func): Authentication token
            new_asset_note: Fixture to create an asset note
            log in the database
         Returns:
            None
        """
        new_asset_note.save()
        note_id = new_asset_note.id
        update_data = ASSET_NOTE_DATA
        data = json.dumps(update_data)
        response = client.patch(
            f'{API_BASE_URL_V1}/repair-logs/@{note_id}', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert isinstance(response_json, dict)
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors['invalid_id']
