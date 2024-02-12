import pytest
from api.schemas.space_type import SpaceTypeSchema
from tests.mocks.space_type import (VALID_SPACE_TYPE_DATA,
                                    SPACE_TYPE_DATA_WITHOUT_TYPE,
                                    SPACE_TYPE_DATA_WITH_EMPTY_COLOR)
from api.utilities.messages.error_messages import serialization_errors

schema = SpaceTypeSchema()


class TestSpaceTypeShema:
    """
    Test space type schema
    """

    def test_space_type_schema_will_pass_with_valid_data(self, init_db):
        """
        Should pass when valid space type data is supplied
        """
        data = VALID_SPACE_TYPE_DATA
        serialized_data, errors = schema.load(data)

        assert serialized_data['type'] == data['type'].title()
        assert serialized_data['color'] == data['color']
        assert errors == {}

    def test_space_type_schema_will_raise_error_with_invalid_type(
            self, init_db):
        """
        Should raise an error when no type attribute is not supplied
        """
        data = SPACE_TYPE_DATA_WITHOUT_TYPE
        serialized_data, errors = schema.load(data)

        assert 'type' not in serialized_data
        assert serialized_data['color'] == data['color']
        assert errors == {'type': [serialization_errors['field_required']]}

    def test_space_type_schema_will_catch_error_with_invalid_color(
            self, init_db):
        """
        Should raise an error when no color attribute is not supplied
        """
        data = SPACE_TYPE_DATA_WITH_EMPTY_COLOR
        serialized_data, errors = schema.load(data)

        assert 'color' not in serialized_data
        assert serialized_data['type'] == data['type']
        assert errors == {'color': [serialization_errors['field_required']]}
