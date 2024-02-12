"""Module fo testing asset category models"""
import pytest

from api.models import Asset, Attribute, AssetCategory
from api.middlewares.base_validator import ValidationError


class TestAssetCategoryModel:
    """Test class for the asset category model class"""

    def test_new_asset_category(self, new_asset_category, init_db):
        """Test that a new asset category gets created"""

        assert new_asset_category == new_asset_category.save()

    def test_update_(self, new_asset_category, request_ctx,
                     mock_request_two_obj_decoded_token):
        """Test that a new asset category gets updated"""

        new_asset_category.update_(name='USB Dongles')

        assert new_asset_category.name == 'USB Dongles'
        assert new_asset_category.description is None

    def test_get(self, new_asset_category):
        """Test that a new asset category gets fetched"""

        asset_category = AssetCategory.get(new_asset_category.id)

        assert asset_category == new_asset_category
        assert asset_category.description is None
        assert asset_category.parent_id is None

    def test_assets(self, new_asset_category, new_user):
        """Test that a new asset gets added to a category"""

        new_user.save()
        asset = Asset(
            tag='AND/345/EWR',
            assignee_id=new_user.token_id,
            assignee_type='user')

        new_asset_category.assets.append(asset)
        asset.save()
        new_asset_category.save()
        assert new_asset_category.assets[0] == asset

    def test_attributes(self, new_asset_category):
        """Test that a new asset category gets associated with an attribute"""

        attribute = Attribute(
            _key='warranty',
            label='warranty',
            is_required=False,
            input_control='text-area',
            choices='choice')

        new_asset_category.attributes.append(attribute)
        attribute.save()
        new_asset_category.save()
        assert new_asset_category.attributes[0] == attribute

    def test_count(self, new_asset_category):
        """Test that a new asset category counts can be retrieved"""

        assert new_asset_category.count() == 1

    def test_query(self, new_asset_category):
        """Test that a query on an asset category returns a list"""

        category_query = new_asset_category.query_()
        assert category_query.count() == 1
        assert isinstance(category_query.all(), list)

    def test_search_asset_category_succeeds(self, new_asset_category):
        """Should retrieve an asset category that matches provided string

        Args:
            new_asset_category (object): Fixture to create a new asset category
        """
        category_query = new_asset_category.query_()
        query_result = category_query.search('dongle').all()
        assert len(query_result) >= 1
        assert query_result[0].name == 'USB Dongles'

    def test_delete_asset_category_with_child_relationships(
            self, new_asset_category):
        """Test that deleting an asset category with a child raises error"""

        with pytest.raises(ValidationError):
            new_asset_category.delete()

    def test_asset_category_model_string_representation(
            self, new_asset_category):
        """ Should compute the string representation of an asset category

        Args:
            new_asset_category (object): Fixture to create a new asset category
        """
        assert repr(
            new_asset_category) == f'<AssetCategory {new_asset_category.name}>'

    def test_adding_subcategory(self, new_asset_category,
                                new_test_asset_category):
        """Test that a new subcategory is successfully created

        Args:
            new_asset_category (object): Fixture to create a new asset category
            new_test_asset_category (object): Fixture to create another asset category
        """

        new_test_asset_category.description = 'laptops for engineers'
        new_test_asset_category.parent_id = new_asset_category.id
        new_test_asset_category.save()

        parent_category = AssetCategory.get(new_asset_category.id)
        child_category = AssetCategory.get(new_test_asset_category.id)

        assert child_category.description == 'laptops for engineers'
        assert child_category.parent_id == new_asset_category.id
        assert parent_category.children[0] == child_category

    def test_child_count(self, new_asset_category, new_test_asset_category):
        """Test that the method child_count gets the number of subcategories

        Args:
            new_asset_category (object): Fixture to create a new asset category
            new_test_asset_category (object): Fixture to create another asset category
        """
        new_test_asset_category.parent_id = new_asset_category.id
        new_test_asset_category.save()

        assert new_asset_category.child_count() is 1

    def test_child_count_when_child_is_deleted(self, new_asset_category,
                                               new_test_asset_category):
        """Test that the method child_count gets 0 subcategories if children are
        marked deleted

        Args:
            new_asset_category (object): Fixture to create a new asset category
            new_test_asset_category (object): Fixture to create another asset category
        """
        new_test_asset_category.parent_id = new_asset_category.id
        new_test_asset_category.deleted = True
        new_asset_category.save()
        assert new_asset_category.child_count() is 0
