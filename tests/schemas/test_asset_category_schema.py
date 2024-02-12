#Third Party
import pytest

# Middlewares
from api.middlewares.base_validator import ValidationError

# Schemas
from api.schemas.asset_category import AssetCategorySchema

# mock data
from tests.mocks.asset_category import (
    valid_asset_category_data_with_attr_keys,
    asset_category_data_missing_running_low,
    asset_category_data_missing_low_in_stock,
    asset_category_data_with_low_in_stock_greater_than_running_low,
    asset_category_with_description_more_than_1000)


class TestAssetCategorySchema:
    """Test AssetCategorySchema"""

    def test_asset_category_schema_with_valid_data_succeeds(self, init_db):
        """Tests that if valid data is supplied to the schema, validation passes

        Args:
            init_db(SQLAlchemy): fixture to initialize the test database

        """

        serialized_data = AssetCategorySchema().load_object_into_schema(
            valid_asset_category_data_with_attr_keys)
        assert serialized_data[
            'name'] == valid_asset_category_data_with_attr_keys['name']
        assert serialized_data[
            'running_low'] == valid_asset_category_data_with_attr_keys[
                'runningLow']
        assert serialized_data[
            'description'] == valid_asset_category_data_with_attr_keys[
                'description']

    def test_asset_category_schema_if_only_low_in_stock_value_supplied_fails(
            self, init_db):
        """Tests if only low_in_stock value is supplied, validation fails

        Args:
            init_db(SQLAlchemy): fixture to initialize the test database
        """

        with pytest.raises(ValidationError):
            AssetCategorySchema().load_object_into_schema(
                asset_category_data_missing_running_low)

    def test_asset_category_schema_if_only_running_low_value_supplied_fails(
            self, init_db):
        """Tests if only running_low value is supplied, validation fails

        Args:
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        with pytest.raises(ValidationError):
            AssetCategorySchema().load_object_into_schema(
                asset_category_data_missing_low_in_stock)

    def test_asset_category_schema_if_low_in_stock_value_is_greater_than_running_low_value_fails(
            self, init_db):
        """Tests if low_in_stock value is greater than running_low value, validation fails

        Args:
            init_db(SQLAlchemy): fixture to initialize the test database
        """

        with pytest.raises(ValidationError):
            AssetCategorySchema().load_object_into_schema(
                asset_category_data_with_low_in_stock_greater_than_running_low)

    def test_asset_category_schema_if_description_more_than_1000_fails(
            self, init_db):
        """Tests that a description longer than 1000 characters causes a
            validation error

        Args:
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        with pytest.raises(ValidationError):
            AssetCategorySchema().load_object_into_schema(
                asset_category_with_description_more_than_1000)

    def test_asset_category_schema_with_invalid_parent_id_fails(
            self, init_db, new_asset_category):
        """Tests if only low_in_stock value is supplied, validation fails

        Args:
            init_db(SQLAlchemy): fixture to initialize the test database
            new_asset_category: fixture to create a category
        """
        category_data = valid_asset_category_data_with_attr_keys
        category_data['parent_id'] = f'@{new_asset_category.id}'
        with pytest.raises(ValidationError):
            AssetCategorySchema().load_object_into_schema(
                category_data)
