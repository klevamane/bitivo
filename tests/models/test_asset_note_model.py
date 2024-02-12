"""Module fo testing asset note models"""

from api.models import AssetNote


class TestAssetNoteModel:
    """ Test class for asset note model class """

    def test_delete(self, asset_note_for_delete, request_ctx,
                    mock_request_two_obj_decoded_token, new_user):
        """Should delete a request

        Args:
            new_request (object): Fixture to create a new request
            request_ctx (object): request client context
            mock_request_obj_decoded_token (object): Mock decoded_token from request client context
        """
        new_user.save()
        new_note = asset_note_for_delete.save()
        new_note.delete()

    def test_new_request(self, init_db, new_asset_note):
        """Should create a new request

        Args:
            init_db (object): Fixture to initialize the test database operations.
            new_request (object): Fixture to create a new request
        """
        assert new_asset_note == new_asset_note.save()

    def test_update(self, new_asset_note):
        """Should update request

        Args:
            new_request (object): Fixture to create a new request
        """
        # new_asset_note.save()
        new_asset_note.update_(title='its my ipad screen that cracked')
        assert AssetNote.get(
            new_asset_note.id).title == 'its my ipad screen that cracked'

    def test_get(self, new_asset_note):
        """Should retrieve a request

        Args:
            new_request (object): Fixture to create a new request
        """
        assert AssetNote.get(new_asset_note.id) == new_asset_note

    def test_query(self, new_asset_note):
        """Should get a list of available requests

        Args:
            new_request (object): Fixture to create a new request
        """
        asset_note_query = new_asset_note.query_()
        assert isinstance(asset_note_query.all(), list)

    def test_request_model_string_representation(self, new_asset_note):
        """ Should compute the string representation of a request

        Args:
            new_request (object): Fixture to create a new request
        """

        assert repr(new_asset_note) == f'<AssetNote {new_asset_note.title}>'
