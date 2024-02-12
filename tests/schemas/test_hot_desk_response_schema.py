# Third parties
import pytest

# Middlewares
from api.middlewares.base_validator import ValidationError

# Schemas
from api.schemas.hot_desk_response import HotDeskResponseSchema

# Test mocks
from ..mocks.hot_desk_response import VALID_HOT_DESK_RESPONSE_DATA, INVALID_HOT_DESK_RESPONSE_DATA


class TestHotDeskResponseSchema:
    """Test HotDeskResponse schema """

    def test_hot_desk_response_schema_with_invalid_data_fails(self, init_db):
        """Tests for invalid data supplied

        Args:
            init_db(SQLAlchemy): Fixture to initialize the test database actions
        """

        with pytest.raises(ValidationError):
            HotDeskResponseSchema().load_object_into_schema(
                INVALID_HOT_DESK_RESPONSE_DATA)

    def test_hot_desk_response_schema_serialization_succeeds(
            self, init_db, new_hot_desk_response):
        """Tests validation data supplied to the schema

         Args:
            new_hot_desk_request (object): Fixture to create a new hot desk
        """
        hot_desk_response = new_hot_desk_response.save()
        hot_desk_response_data = HotDeskResponseSchema().dump(
            hot_desk_response).data

        assert hot_desk_response.id == hot_desk_response_data['id']
        assert hot_desk_response.status.value == hot_desk_response_data[
            'status']

    def test_hot_desk_response_deserialization_succeeds(
            self, new_user, new_hot_desk_request):
        """Tests for data during deserialization"""
        new_hot_desk_request.save()
        VALID_HOT_DESK_RESPONSE_DATA[
            'assigneeId'] = new_hot_desk_request.assignee_id
        VALID_HOT_DESK_RESPONSE_DATA[
            'hotDeskRequestId'] = new_hot_desk_request.id

        hot_desk_response_schema = HotDeskResponseSchema()
        hot_desk_response_data = dict(
            hot_desk_response_schema.load(VALID_HOT_DESK_RESPONSE_DATA).data)

        assert hot_desk_response_data[
            "assignee_id"] == VALID_HOT_DESK_RESPONSE_DATA['assigneeId']
        assert hot_desk_response_data[
            "hot_desk_request_id"] == VALID_HOT_DESK_RESPONSE_DATA[
                'hotDeskRequestId']
