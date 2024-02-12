"""Tests for Asset warranty model"""

from api.models import AssetWarranty

from api.utilities.enums import AssetWarrantyStatusEnum


class TestAssetWarrantyModel:
    """Test Asset warranty Model"""

    def test_asset_warranty_create_succeeds(self, init_db, new_asset_warranty):
        """Should create a new Asset warranty

        Args:
            init_db (object): Fixture to initialize the test database operations.
            new_Asset warranty (object): Fixture to create a new Asset warranty
        """
        new_asset_warranty.save()
        retrieved_value = AssetWarranty.get(new_asset_warranty.id)
        assert retrieved_value
        assert retrieved_value.id == new_asset_warranty.id

    def test_asset_warranty_model_string_representation(
            self, new_asset_warranty):
        """ Should compute the string representation of an asset warranty

        Args:
            new_asset_warranty (object): Fixture to create a new asset warranty
        """

        assert repr(new_asset_warranty
                    ) == f'<AssetWarranty {new_asset_warranty.status}>'

    def test_get_child_relationships_(self, init_db, new_asset_warranty):
        """Get resources relating to the asset warranty model

        Args:
            new_asset_warranty(object): Fixture to create asset warranty
        """

        assert new_asset_warranty.get_child_relationships() is None

    def test_update(self, new_asset_warranty, new_user, request_ctx,
                    mock_request_two_obj_decoded_token):
        """Should update asset warranty

        Args:
            new_asset_warranty (object): Fixture to create a new asset warranty
        """
        new_user.save()
        new_asset_warranty.save()
        new_asset_warranty.update_(start_date='2019-08-12')
        new_asset_warranty.update_(end_date='2020-08-12')
        assert AssetWarranty.get(new_asset_warranty.id).start_date.strftime(
            "%Y-%m-%d") == '2019-08-12'
        assert AssetWarranty.get(new_asset_warranty.id).end_date.strftime(
            "%Y-%m-%d") == '2020-08-12'

    def test_get(self, new_asset_warranty):
        """Should retrieve a asset warranty

        Args:
            asset_warranty (object): Fixture to create a new asset warranty
        """
        assert AssetWarranty.get(new_asset_warranty.id) == new_asset_warranty

    def test_query(self, new_asset_warranty):
        """Should get a list of available asset warranties

        Args:
            new_asset_warranty (object): Fixture to create a new asset warranty
        """
        new_asset_warranty_query = new_asset_warranty.query_()
        assert isinstance(new_asset_warranty_query.all(), list)

    def test_delete(self, asset_warranty_for_delete, new_user, request_ctx,
                    mock_request_two_obj_decoded_token):
        """Should delete an asset warranty

        Args:
            new_asset_warranty (object): Fixture to create a new asset warranty
            request_ctx (object): asset warranty client context
            mock_request_obj_decoded_token (object): Mock decoded_token from asset warranty client context
        """
        new_user.save()
        new_asset_warranty = asset_warranty_for_delete.save()
        new_asset_warranty.delete()
