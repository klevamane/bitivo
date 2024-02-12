"""Module for testing permission schema"""
import pytest

from api.schemas.permission import PermissionSchema
from tests.mocks.permission import VALID_PERMISSION_DATA


class TestPermissionSchema:
    """
    Test permission schema
    """

    def test_permission_schema_with_valid_data_succeeds(self, init_db):
        """
        Should pass when valid permission type is supplied
        """
        permission_schema = PermissionSchema()
        permission_data = permission_schema.load_object_into_schema(
            VALID_PERMISSION_DATA)

        assert permission_data['type'] == VALID_PERMISSION_DATA['type'].title()
