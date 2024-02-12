"""Module to test user model"""

from api.models import User


class TestUserModel:
    """Test user model"""

    def test_new_user(self, init_db, new_user):
        """Test for creating a new user"""
        assert new_user == new_user.save()

    def test_get(self, new_user):
        """Test for get method"""
        assert User.get(new_user.token_id) == new_user

    def test_update(self, new_user, request_ctx,
                    mock_request_two_obj_decoded_token):
        """Test for update method"""
        new_user.update_(name='Ayobami')
        assert new_user.name == 'Ayobami'

    def test_count(self, new_user):
        """Test for count of users"""
        assert new_user.count() == 1

    def test_query(self, new_user):
        """Test for query method"""
        user_query = new_user.query_()
        assert user_query.count() == 1
        assert isinstance(user_query.all(), list)
        assert user_query.filter_by(name='Ayobami').first() == new_user
        assert user_query.filter(new_user.name == 'Ayobami').count() == 1
        assert isinstance(
            user_query.filter(new_user.name == 'Ayobami').all(), list)

    def test_search_users_succeeds(self, new_user):
        """Should retrieve a user that matches provided string

        Args:
            new_user (object): Fixture to create a new user
        """
        user_query = new_user.query_()
        query_result = user_query.search('ayo').all()
        assert len(query_result) >= 1
        assert query_result[0].name == 'Ayobami'

    def test_delete(self, new_user, request_ctx,
                    mock_request_two_obj_decoded_token):
        """Test for delete method"""
        new_user.delete()

    def test_user_model_string_representation(self, new_user):
        """ Should compute the string representation of a user

        Args:
            new_user (object): Fixture to create a new user
        """
        assert repr(new_user) == f'<User {new_user.name}>'
