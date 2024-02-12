import pytest
from api.models import SpaceType
from api.middlewares.base_validator import ValidationError

class TestSpaceTypeModel:
    """
    Test space type model
    """
    def test_new_space_type(self, init_db, new_space_type):
        """Test for creating a new space type"""
        space_type = new_space_type
        assert space_type == new_space_type.save()

    def test_count(self):
        """Test for count of space types"""
        assert SpaceType.count() == 1

    def test_query(self):
        """Test for query method"""
        space_type_query = SpaceType.query_()
        assert space_type_query.count() == 1
        assert isinstance(space_type_query.all(), list)

    def test_update(self, new_space_type):
        """Test for update method"""
        new_space_type.update_(color='Black')
        assert new_space_type.color == 'Black'

    def test_delete(self, new_space_type, request_ctx,
                    mock_request_obj_decoded_token):
        """Test for delete method"""
        new_space_type.delete()
        assert SpaceType.get(new_space_type.id) is None

    def test_space_type_model_string_representation(self, new_space_type):
        """ Should compute the string representation of space type

        Args:
            new_space_type (object): Fixture to create a new space type
        """
        assert repr(new_space_type) == f'<SpaceType {new_space_type.type}>'
