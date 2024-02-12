# Third parties
import pytest
from unittest.mock import Mock

# Middlewares
from api.middlewares.base_validator import ValidationError

# Schemas
from api.schemas.request_type import RequestTypeSchema

# Test mocks
from tests.mocks.request_type import INVALID_REQUEST_TYPE_DATA, VALID_REQUEST_TYPE_DATA

from api.utilities.constants import REQUEST_TYPE_TIME_MAX_VALUES
from api.utilities.messages.error_messages import serialization_errors
from flask import request

error_phrase = ' or '.join(REQUEST_TYPE_TIME_MAX_VALUES.keys())


class TestRequestTypeSchema:
    """ Test RequestType model """

    def test_request_type_schema_dump_succeeds(self, init_db,
                                               new_request_type):
        """Tests if the schema dumps a request type successfully

        Args:
            init_db(SQLAlchemy): Fixture to initialize the test database actions
            new_request_type (object): Fixture to create a new request type
        """

        request_type = new_request_type.save()
        data = RequestTypeSchema().dump(request_type).data
        assert request_type.title == data['title']
