"""Module for testing history schema"""
# library
import pytest

# schema
from api.schemas.history import HistorySchema

# validators
from api.middlewares.base_validator import ValidationError


class TestHistorySchema:
    """Test history schema
    """

    def test_history_schema_with_valid_data_passes(self, init_db):
        """Should pass when valid history data is supplied

        Args:
            init_db (Fixture): initialize db
        """
        data = {
            "resource_id": "-LPUuJEW8lBVV_R1CsQw",
            "resource_type": "Asset",
            "actor_id": "-LSFE343",
            "action": "Add",
            "activity": "Added to Activo"
        }
        history_schema = HistorySchema()
        history_data = history_schema.load_object_into_schema(data)
        assert history_data['resource_id'] == data['resource_id']

    def test_history_schema_with_invalid_data_fails(self, init_db):
        """Should fail with invalid history data

        Args:
            init_db (Fixture): initialize db
        """
        data = {"resource_type": 54321}
        history_schema = HistorySchema()
        with pytest.raises(ValidationError):
            history_schema.load_object_into_schema(data)
