"""Module to test WorkOrder model"""

# Third party libraries
from sqlalchemy import exc
import pytest

# Local import
from api.models import WorkOrder


class TestWorkOrderModel:
    """Tests for WorkOrder model"""

    def test_create_new_work_order_succeeds(self, new_work_order):
        """Should create a new work order

        Args:
            new_work_order (object): Fixture to create a new work orderder
        """

        assert new_work_order == new_work_order.save()

    def test_update_work_order_succeeds(self, new_work_order, request_ctx,
                                        mock_request_two_obj_decoded_token):
        """Should update work order

        Args:
            new_work_order (object): Fixture to create a new work order
        """
        new_work_order.save()
        value = 'Engine Oil'
        new_work_order.update_(title=value)
        assert WorkOrder.get(new_work_order.id).title == value

    def test_get_a_work_order_succeeds(self, new_work_order):
        """Should retrieve a work order

        Args:
            new_work_order (object): Fixture to create a new work order
        """
        assert WorkOrder.get(new_work_order.id) == new_work_order

    def test_query_all_work_order_succeeds(self, new_work_order):
        """Should get a list of work orders

        Args:
            new_work_order (object): Fixture to create a new work order
        """
        work_order_query = new_work_order.query_()
        assert isinstance(work_order_query.all(), list)

    def test_search_users_succeeds(self, new_work_order):
        """Should retrieve a user that matches provided string

        Args:
            new_work_order (object): Fixture to create a work order
        """
        work_order_query = new_work_order.query_()
        query_result = work_order_query.search('car').all()
        assert len(query_result) >= 1
        assert query_result[0].description == 'change the fuel of the car'

    def test_get_child_relationships_(self, new_work_order):
        """Get resources relating to the model

        Args:
            new_work_order (object): Fixture to create a new work order
        """

        assert new_work_order.get_child_relationships() is None

    def test_delete_a_work_order_succeeds(self, new_work_order, request_ctx,
                                          mock_request_two_obj_decoded_token):
        """Should delete a work order

        Args:
            new_work_order (object): Fixture to create a new work order
        """
        new_work_order.delete()
        assert WorkOrder.get(new_work_order.id) is None

    def test_work_order_model_string_representation(self, new_work_order):
        """Should compute the string representation

        Args:
            new_work_order (object): Fixture to create a new work order
        """

        assert repr(new_work_order) == f'<WorkOrder {new_work_order.title}>'

    def test_instance_with_invalid_assignee_id_fails(
            self, work_order_with_invalid_assignee_id):
        """Should not create new work order

        IntegrityError is expected to be raised

        Args:
            work_order_with_invalid_assignee_id(object):
                                                    Fixture for work order with wrong assignee_id

        """

        with pytest.raises(exc.IntegrityError):
            work_order_with_invalid_assignee_id.save()

    def test_instance_with_invalid_maintenance_category_id_fails(
            self, work_order_with_invalid_maintenance_category_id):
        """Should not create new work order

        IntegrityError is expected to be raised

        Args:
            work_order_with_invalid_assignee_id(object):
                                                    Fixture for work order with wrong assignee_id

        """

        with pytest.raises(exc.IntegrityError):
            work_order_with_invalid_maintenance_category_id.save()

    def test_instance_with_missing_fields_fails(
            self, work_order_with_missing_fields):
        """Should not create new work order

        IntegrityError is expected to be raised

        Args:
            work_order_with_invalid_assignee_id(object):
                                                    Fixture for work order with wrong assignee_id

        """

        with pytest.raises(exc.IntegrityError):
            work_order_with_missing_fields.save()
