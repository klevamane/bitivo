import pytest
from api.schemas.space import SpaceSchema
from tests.mocks.space import VALID_SPACE_DATA
from api.utilities.messages.error_messages import serialization_errors

schema = SpaceSchema()


class TestSpaceShema:
    """
    Test space schema
    """

    def test_space_shema_will_pass_with_valid_data(self, init_db):
        """
        Should pass when valid space data is supplied
        """
        data = VALID_SPACE_DATA
        serialized_data, errors = schema.load(data)

        assert serialized_data['name'] == data['name'].title()
