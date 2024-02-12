# Thirdparty imports
import pytest

# Models
from api.models import MaintenanceCategory

# Validators
from api.middlewares.base_validator import ValidationError


class TestMaintenanceCategoryModel:
    def test_create_new_maintenance_category_succeeds(
            self, new_maintenance_category):
        """Should create a new maintenance category
        
        Args:
            new_maintenance_category (object): Fixture to create a maintenance category
        """
        new_maintenance_category.save()
        retrieved_value = MaintenanceCategory.get(new_maintenance_category.id)
        assert retrieved_value.id == new_maintenance_category.id

    def test_update_maintenance_category_succeeds(
            self, new_maintenance_category, request_ctx,
            mock_request_two_obj_decoded_token):
        """Should update a maintenance category

        Args:
            new_maintenance_category (object): Fixture to create a maintenance category
        """
        new_maintenance_category.save()
        new_maintenance_category.update_(title="Updated")
        assert new_maintenance_category.title == "Updated"

    def test_get_maintenance_category_succeeds(self, new_maintenance_category):
        """Should retrieve a maintenance category

        Args:
            new_maintenance_category (object): Fixture to create a maintenance category
        """
        new_maintenance_category.save()
        assert MaintenanceCategory.get(
            new_maintenance_category.id) == new_maintenance_category

    def test_get_child_relationships(self, new_maintenance_category,
                                     new_work_order):
        """Should get child relationships of the model
        
        Args:
            new_maintenance_category (obj): Fixture to create a maintenance category
            new_work_order (obj): Fixture to create a work order

        """
        new_work_order.save()
        (child_work_orders_base_query,
         ) = new_maintenance_category.get_child_relationships()
        child_work_orders = child_work_orders_base_query.all()
        assert len(child_work_orders) > 0
        assert child_work_orders[0].id == new_work_order.id

    def test_delete_maintenance_category_with_child_relationships_fails(
            self, new_work_order, new_maintenance_category):
        """Test that deleting an maintenance category with a child raises error
        
        Args:
            new_work_order (obj): Fixture to create a work order
            new_maintenance_category (obj): Fixture to create a maintenance category
        """
        new_work_order.save()
        with pytest.raises(ValidationError):
            new_maintenance_category.delete()

    def test_query_maintenance_category_succeeds(self):
        """Should get a list of maintenance categories"""
        new_maintenance_category_query = MaintenanceCategory.query_()
        assert isinstance(new_maintenance_category_query.all(), list)

    def test_maintenance_category_model_string_representation_succeeds(
            self, new_maintenance_category):
        """Should retrieve the maintenance category string representation
        
        Args:
            new_maintenance_category (object): Fixture to create a maintenance category
        """
        assert repr(
            new_maintenance_category
        ) == f'<MaintenanceCategory {new_maintenance_category.title}>'
