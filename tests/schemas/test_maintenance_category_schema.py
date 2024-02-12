"""Module to test the maintenance category schema"""

# Schemas
from api.schemas.maintenance_categories import MaintenanceCategorySchema

# Serializer messages
from api.utilities.messages.error_messages import serialization_errors

# Constants
from ..mocks.maintenance_category import MAINTENANCE_CATEGORY


class TestMaintenanceCategorySchema:
    def test_maintenance_category_schema_with_valid_data_succeeds(
            self, new_maintenance_category, new_work_order):
        """Should pass with valid model object 
        
        Args:
            new_maintenance_category (obj): Fixture to create a maintenance category
            new_work_order (obj): Fixture to create a work order
        """

        maintenance_category = new_maintenance_category.save()
        new_work_order.save()
        maintenance_category_data = MaintenanceCategorySchema().dump(
            maintenance_category).data
        assert maintenance_category_data['id'] == maintenance_category.id
        assert maintenance_category_data['title'] == maintenance_category.title
        assert type(maintenance_category_data['workOrderCount']) == int

    def test_maintenance_category_schema_with_invalid_asset_category_fails(
            self, new_maintenance_category, new_center, new_asset_category):
        """Should fail with invalid asset category 
        
        Args:
            new_maintenance_category (obj): Fixture to create a maintenance category
            new_center (obj): Fixture to create a center category
            new_asset_category (obj): Fixture to create an asset category
        """
        new_maintenance_category.save()
        new_center.save()
        NEW_MAINTENANCE_CATEGORY = MAINTENANCE_CATEGORY.copy()
        NEW_MAINTENANCE_CATEGORY['centerId'] = new_center.id
        maintenance_category_errors = MaintenanceCategorySchema().load(
            NEW_MAINTENANCE_CATEGORY).errors
        assert maintenance_category_errors['assetCategoryId'][
            0] == serialization_errors['category_not_found']

    def test_maintenance_category_schema_with_invalid_center_fails(
            self, new_maintenance_category, new_asset_category):
        """Should fail with an invalid center id 
        
        Args:
            new_maintenance_category (obj): Fixture to create a maintenance category
            new_asset_category (obj): Fixture to create an asset category
        """
        new_maintenance_category.save()
        new_asset_category.save()
        NEW_MAINTENANCE_CATEGORY = MAINTENANCE_CATEGORY.copy()
        NEW_MAINTENANCE_CATEGORY['assetCategoryId'] = new_asset_category.id
        maintenance_category_errors = MaintenanceCategorySchema().load(
            NEW_MAINTENANCE_CATEGORY).errors
        assert maintenance_category_errors['centerId'][
            0] == serialization_errors['not_found'].format('Center')

    def test_maintenance_category_schema_with_invalid_title_fails(
            self, new_maintenance_category, new_asset_category, new_center):
        """Should fail with no title in the body
        
        Args:
            new_maintenance_category (obj): Fixture to create a maintenance category
            new_asset_category (obj): Fixture to create an asset category
            new_center (obj): Fixture to create a center category
        """
        new_maintenance_category.save()
        new_asset_category.save()
        new_center.save()
        NEW_MAINTENANCE_CATEGORY = MAINTENANCE_CATEGORY.copy()
        NEW_MAINTENANCE_CATEGORY['title'] = ''
        NEW_MAINTENANCE_CATEGORY['centerId'] = new_center.id
        NEW_MAINTENANCE_CATEGORY['assetCategoryId'] = new_asset_category.id
        maintenance_category_errors = MaintenanceCategorySchema().load(
            NEW_MAINTENANCE_CATEGORY).errors
        assert maintenance_category_errors['title'][0] == serialization_errors[
            'not_empty']

    def test_maintenance_category_schema_with_no_data_fails(
            self, new_maintenance_category, new_asset_category, new_center):
        """Should fail with no data passed to the schema
        
        Args:
            new_maintenance_category (obj): Fixture to create a maintenance category
            new_asset_category (obj): Fixture to create an asset category
            new_center (obj): Fixture to create a center category
        """
        new_maintenance_category.save()
        new_asset_category.save()
        new_center.save()
        maintenance_category_errors = MaintenanceCategorySchema().load(
            {}).errors
        for key in maintenance_category_errors:
            assert maintenance_category_errors[key][0] == serialization_errors[
                'field_required']
