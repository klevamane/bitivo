import pytest
from unittest.mock import MagicMock

from api.schemas.work_order import WorkOrderSchema
from api.utilities.validators.maintenance_category_validators import validate_titles_exists

from api.utilities.helpers.maintenance_category import add_work_orders
from api.models.maintenance_category import MaintenanceCategory, WorkOrder

from api.utilities.constants import EXCLUDED_FIELDS
from api.models.database import db
from tests.mocks.maintenance_category import VAlID_WORK_ORDER_DATA


class TestMaintenanceCategoryValidations:
    """Test validate work order titles function"""

    def test_saving_dublicate_work_order_title_fails(
            self, new_maintenance_category, new_user):
        """Test if dublicate titles for work order fails"""

        maintenance_category = new_maintenance_category.save()
        new_user.save()
        VAlID_WORK_ORDER_DATA[0]['assigneeId'] = new_user.token_id
        work_order_schema = WorkOrderSchema(exclude=EXCLUDED_FIELDS)
        work_order = work_order_schema.load_object_into_schema(
            VAlID_WORK_ORDER_DATA[0], partial=True)
        add_work_orders([work_order], maintenance_category)
        db.session.commit()

        assert validate_titles_exists(MaintenanceCategory,
                                      VAlID_WORK_ORDER_DATA[0],
                                      maintenance_category.id) is True
