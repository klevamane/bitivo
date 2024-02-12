"""Module for hot desk schema tests"""

# Third parties
import pytest

# Middlewares
from api.middlewares.base_validator import ValidationError

# Schemas
from api.schemas.hot_desk import HotDeskRequestSchema
from api.utilities.validators.status_validator import validate_hot_desk_status

# Test mocks
from ..mocks.hot_desk import VALID_HOT_DESK_DATA, INVALID_HOT_DESK_DATA, VALID_STATUS_DATA, INVALID_HOT_DESK_REQUESTER_ID


class TestHotDeskRequestSchema:
    """Test HotDeskRequest schema """

    def test_hot_desk_schema_with_invalid_data_fails(self, init_db):
        """Tests for invalid data supplied

        Args:
            init_db(SQLAlchemy): Fixture to initialize the test database actions
        """

        with pytest.raises(ValidationError):
            HotDeskRequestSchema().load_object_into_schema(
                INVALID_HOT_DESK_DATA)

    def test_hot_desk_schema_serialization_succeeds(self, init_db,
                                                    new_hot_desk_request):
        """Tests validation data supplied to the schema

         Args:
            new_hot_desk_request (object): Fixture to create a new hot desk
        """
        hot_desk = new_hot_desk_request.save()
        hot_desk_data = HotDeskRequestSchema().dump(hot_desk).data

        assert hot_desk.requester_id == hot_desk_data['requester']['tokenId']
        assert hot_desk.hot_desk_ref_no == hot_desk_data['hotDeskRefNo']

    def test_hot_desk_deserialization_succeeds(self, new_user):
        """Tests for data during deserialization"""
        new_user.save()
        hot_desk_schema = HotDeskRequestSchema()
        VALID_HOT_DESK_DATA['requester_id'] = new_user.token_id
        hot_desk_data = dict(hot_desk_schema.load(VALID_HOT_DESK_DATA).data)

        assert hot_desk_data["requester_id"] == VALID_HOT_DESK_DATA[
            'requester_id']
        assert hot_desk_data["hot_desk_ref_no"] == VALID_HOT_DESK_DATA[
            'hot_desk_ref_no']

    def test_hot_desk_with_invalid_requester_id_fails(self, init_db):
        """Tests for invalid data supplied

        Args:
            init_db(SQLAlchemy): Fixture to initialize the test database actions
        """
        with pytest.raises(ValidationError):
            HotDeskRequestSchema().load_object_into_schema(
                INVALID_HOT_DESK_REQUESTER_ID)
