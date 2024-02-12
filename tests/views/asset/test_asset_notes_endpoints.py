"""Module for testing asset notes resources."""
from flask import json

from api.utilities.constants import CHARSET
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import serialization_errors
from tests.mocks.asset_note import TEST_ASSET_NOTE

# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestAssetNoteEndpoints:
    """Class for testing asset notes resource"""

    def test_create_asset_note_succeeds(self, client, init_db, auth_header,
                                        new_asset, new_user):
        """
        Test creating asset note for specific asset succeeds
        """
        new_user.save()
        new_asset.created_by = new_user.token_id
        data = json.dumps(TEST_ASSET_NOTE)
        response = client.post(
            f'{API_BASE_URL_V1}/assets/{new_asset.id}/notes',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 201
        assert isinstance(response_json, dict)
        assert response_json["status"] == "success"
        assert response_json["message"] == SUCCESS_MESSAGES['created'].format(
            'Asset note')
        assert response_json["data"]["title"] == TEST_ASSET_NOTE['title']

    def test_create_asset_note_for_nonexistent_asset_fails(
            self, client, init_db, auth_header, new_space):
        """
        Test creating asset note for non-existent asset fails
        """

        data = json.dumps(TEST_ASSET_NOTE)
        response = client.post(
            f'{API_BASE_URL_V1}/assets/{new_space.id}/notes',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert isinstance(response_json, dict)
        assert response_json["status"] == "error"
        assert response_json["message"] == "An error occurred"
        assert response_json["errors"]["assetId"][0] == serialization_errors[
            'asset_not_found']

    def test_get_asset_notes_succeeds(self, client, init_db, auth_header,
                                      new_asset_note):
        """
        Test getting asset note for specific asset succeeds
        """
        new_asset_note.save()
        response = client.get(
            f'{API_BASE_URL_V1}/assets/{new_asset_note.asset_id}/notes',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert isinstance(response_json, dict)
        assert response_json["status"] == "success"
        assert response_json["message"] == SUCCESS_MESSAGES['fetched'].format(
            'Asset notes')
        assert response_json["data"][0]["title"] == new_asset_note.title

    def test_get_asset_notes_with_invalid_asset_id_fails(
            self, client, init_db, auth_header):
        """
        Test getting asset note for specific asset with invalid asset
        id fails
        """
        response = client.get(
            f'{API_BASE_URL_V1}/assets/-LjXY8QptIssfEtZl3Ty/notes',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json["status"] == "error"
        assert response_json['message'] == serialization_errors[
            'not_found'].format('Asset')
