"""Module for work order schema tests"""

# Third parties
import pytest

# Middlewares
from api.utilities.helpers.schemas import validate_repeat_days

# Schemas
from api.schemas.frequency_schema import CustomOccurrence, CustomOccurrenceSchema
from api.utilities.enums import CustomFrequencyEnum

# Test mocks
from tests.mocks.work_order import VALID_CUSTOMOCCURRENCE_DETAILS, INVALID_REPEAT_DAYS, VALID_REPEAT_DAYS, DAYS


class TestCustomOccurrenceSchema:
    """Test CustomOccurrence schema """

    def test_custom_occurrence_deserialization_succeeds(self):
        """Tests for data during deserialization"""

        custom_occurrence_schema = CustomOccurrenceSchema()
        custom_occurrence_data = dict(
            custom_occurrence_schema.load(VALID_CUSTOMOCCURRENCE_DETAILS).data)

        assert custom_occurrence_data[
            'repeat_days'] == VALID_CUSTOMOCCURRENCE_DETAILS['repeat_days']
        assert custom_occurrence_data[
            'repeat_units'] == VALID_CUSTOMOCCURRENCE_DETAILS['repeat_units']
        assert custom_occurrence_data[
            'ends'] == VALID_CUSTOMOCCURRENCE_DETAILS['ends']
        assert custom_occurrence_data['ends'][
            'after'] == VALID_CUSTOMOCCURRENCE_DETAILS['ends']['after']

    def test_validate_repeat_days(self):
        """Test for validate repeat days in work order schema."""

        with pytest.raises(Exception) as e:
            for key in INVALID_REPEAT_DAYS:
                assert key not in DAYS and validate_repeat_days(
                    INVALID_REPEAT_DAYS)
        assert validate_repeat_days(VALID_REPEAT_DAYS) is None
