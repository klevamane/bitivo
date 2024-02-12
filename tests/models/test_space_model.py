import pytest
from api.models import Space
from api.middlewares.base_validator import ValidationError


class TestSpaceModel:
    """
    Test space model
    """

    def test_space_will_save(self, init_db, new_space):
        """Test for creating a new space"""
        space1 = new_space
        assert space1 == new_space.save()
        assert space1.name == 'Epic Tower'

    def test_space_count_is_correct(self):
        """Test for count of space"""
        assert Space.count() == 1

    def test_query_method(self):
        """Test that a query on a space returns a list"""
        space_query = Space.query_()
        assert space_query.count() == 1
        assert isinstance(space_query.all(), list)

    def test_no_child_for_first_space(self):
        """Test that first space has no child"""
        space_query = Space.query_().first()
        assert space_query.children == []

    def test_space_will_delete_without_children(
            self, new_space, request_ctx, mock_request_two_obj_decoded_token,
            new_user):
        """Test that deleting a space without child is successful"""
        new_user.save()
        new_space.delete()
        assert Space.get(new_space.id) is None

    def test_parent_child_space_relationship(self, new_space, new_space2):
        """Test that a parent space gets associated with a child space"""
        new_space.save()
        assert len(tuple(new_space.children)) == 0
        new_space2.save()
        assert len(tuple(new_space.children)) == 1

    def test_space_will_update(self, new_space, request_ctx,
                               mock_request_two_obj_decoded_token, new_user):
        """Test for update method"""
        new_user.save()
        new_space.update_(name='Floor')
        new_space.update_(parent_id=None)
        assert new_space.name == 'Floor'
        assert new_space.parent_id == None

    def test_space_with_child_relationship_will_not_delete(
            self, new_space, request_ctx, new_space2,
            mock_request_obj_decoded_token):
        """Test that deleting a space with a child raises error"""
        new_space.save()
        new_space2.save()
        with pytest.raises(ValidationError):
            new_space.delete()

    def test_space_model_string_representation(self, new_space):
        """ Should compute the string representation of a space

        Args:
            new_space (object): Fixture to create a new space
        """
        assert repr(
            new_space) == f'<Space {new_space.name} {new_space.children}>'
