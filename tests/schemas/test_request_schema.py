# Third parties
import pytest

# Middlewares
from api.middlewares.base_validator import ValidationError

# Schemas
from api.schemas.request import RequestSchema

# Test mocks
from tests.mocks.requests import INVALID_REQUEST_DATA

# Messages
from api.utilities.messages.error_messages import serialization_errors


class TestRequestSchema:
    """ Test Request model """

    def test_request_schema_with_invalid_data_fails(self, init_db):
        """Tests validation fails if invalid data is supplied to the schema
         Args:
            init_db(SQLAlchemy): Fixture to initialize the test database actions
        """
        with pytest.raises(ValidationError) as e:
            RequestSchema().load_object_into_schema(INVALID_REQUEST_DATA)
        error = e.value.error
        assert error['errors']['centerId'][0] == serialization_errors[
            'invalid_id_field']
        assert error['errors']['requesterId'][0] == serialization_errors[
            'invalid_id_field']
        assert error['errors']['requestTypeId'][0] == serialization_errors[
            'invalid_id_field']
        assert error['message'] == 'An error occurred'
        assert error['status'] == 'error'

    def test_request_schema_with_valid_data_succeeds(self, init_db,
                                                     new_request):
        """Tests validation fails if invalid data is supplied to the schema
         Args:
            init_db(SQLAlchemy): Fixture to initialize the test database actions
            new_request (object): Fixture to create a new request
        """
        request = new_request.save()
        request_data = RequestSchema().dump(request).data

        assert request.subject == request_data['subject']
        assert request.serial_number == request_data['serialNumber']
        assert request.description == request_data['description']
