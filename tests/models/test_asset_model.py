import pytest
from api.models import Asset, AssetCategory
from api.utilities.enums import AssigneeType
from api.models import User, AssetCategory


class TestAssetModel:
    def test_new_asset(self, new_asset_category, init_db, new_user):
        new_user = new_user.save()
        asset = Asset(
            tag='AND/345/EWR',
            assignee_id=new_user.token_id,
            assignee_type='user',
            created_by=new_user.token_id)
        new_asset_category.assets.append(asset)
        new_asset_category.save()
        assert asset == asset.save()

    def test_assignee_type_has_enum_store_succeed(self, new_asset_category,
                                                  init_db, new_space_two):
        new_space_two.save()
        asset = Asset(
            tag='AND/346/EWR',
            assignee_id=new_space_two.id,
            assignee_type='space')
        new_asset_category.assets.append(asset)
        new_asset_category.save()
        asset.save()
        assert asset.assignee_type.value == AssigneeType.store.value
        assert asset.tag == 'AND/346/EWR'

    def test_count(self):
        assert Asset.count() >= 1

    def test_query(self):
        asset_query = Asset.query_()
        assert asset_query.count() >= 1
        assert isinstance(asset_query.all(), list)

    def test_search_asset_succeeds(self):
        """Should retrieve assets that match provided string
        """
        asset_query = Asset.query_()
        query_result = asset_query.search('AND/34').all()
        assert len(query_result) >= 1
        assert query_result[0].tag == 'AND/346/EWR'

    def test_get(self, new_asset_category, new_user):
        new_user = new_user.save()
        status = 'assigned'
        asset = Asset(
            tag='AND/345/EWH',
            assignee_id=new_user.token_id,
            assignee_type='user',
            status=status,
            created_by=new_user.token_id)
        new_asset_category.assets.append(asset)
        new_asset_category.save()
        asset.save()
        new_asset = Asset.get(asset.id)
        assert new_asset == asset
        assert new_asset.status == status

    def test_get_for_non_admin_users(self, new_asset_category, test_user, mock_request_six_obj_decoded_token, request_ctx):
        new_user = test_user.save()
        status = 'assigned'
        asset = Asset(
            tag='AND/519/INK',
            assignee_id=new_user.token_id,
            assignee_type='user',
            status=status,
            created_by=new_user.token_id)
        new_asset_category.assets.append(asset)
        new_asset_category.save()
        asset.save()
        new_asset = Asset.get(asset.id)
        assert new_asset is None

    def test_delete(self, new_asset_category, request_ctx,
                    mock_request_two_obj_decoded_token,
                    new_user):
        new_asset_category.assets[0].delete()

    def test_inserting_record_without_assignee_raises_exception(
            self, init_db, new_asset_category, new_user):
        """Test that an exception is raised when no assignee is found

        Args:
            init_db (fixture): Initialize test database
            new_asset_category (fixture): Generate a new asset category
        """
        new_asset_category.save()
        asset_details = {
            'tag': 'AND/HAM/044',
            'asset_category_id': new_asset_category.id
        }
        with pytest.raises(Exception) as error:
            asset = Asset(**asset_details)
            asset.save()
            assert error.value.message == 'Assignee object not found'
