"""Module for hot dest status validator """

# System libraries
import unittest
import enum

# Third parties
import pytest

# Middlewares
from api.middlewares.base_validator import ValidationError

# Schemas
from api.utilities.validators.status_validator import validate_hot_desk_status, validate_status

# Test mocks
from ..mocks.hot_desk import VALID_STATUS_DATA

from api.utilities.enums import HotDeskRequestStatusEnum


class TestValidateHotDeskRequestStatus(unittest.TestCase):

    def test_hot_desk_status_validator(self, status=None):
        """Tests for the validate hot_desk_status_method"""

        status = HotDeskRequestStatusEnum.pending
        assert status.value in VALID_STATUS_DATA and validate_hot_desk_status(status) is None

        invalid_status_enum = enum.Enum('InvalidStatusEnum', {"status": "not pending"})
        status = invalid_status_enum.status
        import marshmallow
        with self.assertRaises(marshmallow.exceptions.ValidationError):
            assert status not  in VALID_STATUS_DATA and validate_hot_desk_status(status)

        status = "pending"
        with self.assertRaises(marshmallow.exceptions.ValidationError):
            assert status not  in ["approved", "denied"] and validate_status(status)



