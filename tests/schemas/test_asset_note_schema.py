# third party library
import pytest

# schema
from api.schemas.asset_note import AssetNoteSchema

# middleware
from api.middlewares.base_validator import ValidationError

# mock
from tests.mocks.asset_note import INVALID_ASSET_NOTE


class TestAssetNoteSchema:
    """ Test Asset Note Schema """

    def test_asset_note_schema_with_valid_data_succeeds(
            self, new_asset_note):
        """
        Test Asset Note schema with valid data
        new_asset_note(object): fixture to create a new asset note """
        new_asset_note = new_asset_note.save()
        new_asset_note_data = AssetNoteSchema().dump(new_asset_note).data

        assert new_asset_note.id == new_asset_note_data['id']
        assert new_asset_note.title == new_asset_note_data['title']
        assert new_asset_note.body == new_asset_note_data['body']

    def test_asset_note_schema_with_invalid_data_fails(self):
        """
        Test asset note schema with invalid data

        """
        with pytest.raises(ValidationError):
            AssetNoteSchema().load_object_into_schema(INVALID_ASSET_NOTE)
