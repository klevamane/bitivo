# third party library
import pytest

# schema
from api.schemas.asset_warranty import AssetWarrantySchema

# middleware
from api.middlewares.base_validator import ValidationError

# mock
from tests.mocks.asset_warranty import INVALID_ASSET_WARRANTY


class TestAssetWarrantySchema:
    """ Test Asset Warranty Schema """

    def test_asset_warranty_schema_with_valid_data_succeeds(
            self, new_asset_warranty):
        """
        Test Asset Warranty schema with valid data
        new_asset_warranty(object): fixture to create a new asset warranty

        """

        new_asset_warranty = new_asset_warranty.save()
        new_asset_warranty_data = AssetWarrantySchema().dump(new_asset_warranty).data
        assert new_asset_warranty.id == new_asset_warranty_data['id']
        assert new_asset_warranty.status.value == new_asset_warranty_data['status']

    def test_asset_warranty_schema_with_invalid_data_fails(self):
        """
        Test asset warranty schema with invalid data

        """
        with pytest.raises(ValidationError):
            AssetWarrantySchema().load_object_into_schema(INVALID_ASSET_WARRANTY)
