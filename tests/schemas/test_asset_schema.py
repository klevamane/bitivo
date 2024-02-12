"""Module for testing history schema"""
# library
import pytest

# schema
from api.schemas.asset import AssetSchema

# validators
from api.middlewares.base_validator import ValidationError


class TestAssetSchema:
    """Test asset schema
    """

    def test_asset_schema_with_valid_data_passes(
            self, init_db, new_space, new_center, new_asset_category):
        """Should pass when valid history data is supplied

        Args:
            init_db (Fixture): initialize db
            new_space (object): fixture used to create new space 
            new_center (object): fixture used to create new center 
            new_asset_category (object): fixture used to create new asset category
        """
        new_asset_category.save()
        new_center.save()
        new_space.save()
        data = {
            'tag': 'AND/34005/EWRD',
            'customAttributes': {},
            'assetCategoryId': new_asset_category.id,
            'centerId': new_center.id,
            'status': 'inventory',
            'assigneeId': new_space.id,
            'assigneeType': 'space'
        }
        asset_schema = AssetSchema()
        asset_data = asset_schema.load_object_into_schema(data)
        assert asset_data['tag'] == data['tag']

    def test_asset_schema_with_invalid_data_fails(self, init_db):
        """Should fail with invalid history data

        Args:
            init_db (Fixture): initialize db
        """
        data = {'tag': 'AND/345/EWRD'}
        asset_schema = AssetSchema()
        with pytest.raises(ValidationError):
            asset_schema.load_object_into_schema(data)
