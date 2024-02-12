"""Module for work order schema tests"""

# Third parties
import pytest

# Middlewares
from api.middlewares.base_validator import ValidationError
from api.utilities.helpers.schemas import validate_repeat_days
from api.utilities.messages.error_messages.serialization_error import error_dict

# Schemas
from api.schemas.work_order import WorkOrderSchema

# Test mocks
from tests.mocks.work_order import VALID_WORK_ORDER_DATA, INVALID_WORK_ORDER_DATA, INVALID_REPEAT_DAYS, VALID_REPEAT_DAYS, DAYS


class TestWorkOrderSchema:
    """Test WorkOrder schema """

    def test_work_order_schema_with_invalid_data_fails(self, init_db):
        """Tests for invalid data supplied

        Args:
            init_db(SQLAlchemy): Fixture to initialize the test database actions
        """

        with pytest.raises(ValidationError):
            WorkOrderSchema().load_object_into_schema(INVALID_WORK_ORDER_DATA)

    def test_work_order_schema_serialization_succeeds(self, new_work_order):
        """Tests validation data supplied to the schema

         Args:
            new_work_order (object): Fixture to create a new work_order
        """
        work_order = new_work_order.save()
        work_order_data = WorkOrderSchema().dump(work_order).data

        assert work_order.title == work_order_data['title']
        assert work_order.description == work_order_data['description']
        assert work_order.frequency.value == work_order_data['frequency']
        assert work_order.status.value == work_order_data['status']

    def test_work_order_deserialization_succeeds(self):
        """Tests for data during deserialization"""

        work_order_schema = WorkOrderSchema()

        work_order_data = dict(
            work_order_schema.load(VALID_WORK_ORDER_DATA).data)
        assert work_order_data["title"] == VALID_WORK_ORDER_DATA['title']
        assert work_order_data["description"] == VALID_WORK_ORDER_DATA[
            'description']
