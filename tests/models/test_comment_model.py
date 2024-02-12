from api.models import Comment
from unittest.mock import MagicMock, Mock, patch


class TestCommentModel:
    """
    Test comment model
    """

    def test_new_comment(self, init_db, new_comment):
        """Should create and return a comment
         Args:
            init_db (fixture): Fixture to initialize the test database operations.
            new_comment (object): Fixture to create a new comment
        """
        comment = new_comment
        assert comment == new_comment.save()

    def test_count(self):
        """Should return the count of available comments
        """
        assert Comment.count() == 1

    def test_query(self):
        """Should return the count of available comments through the query_
        """
        assert Comment.query_().count() == 1

    def test_update(self, new_comment, new_user, request_ctx,
                    mock_request_two_obj_decoded_token):
        """
        Should update a comment
         Args:
            new_comment (object): Fixture to update a comment
        """
        from faker import Faker
        fake = Faker()
        body = fake.sentence()
        new_comment.update_(body=body)
        assert new_comment.body == body

    def test_comment_model_string_representation(self, new_comment):
        """
        Should compute the official string representation of comment
         Args:
            new_comment (object): Fixture to create a new comment
        """
        assert repr(new_comment) == f'<Comment {new_comment.body}>'

    def test_delete(self, new_comment, request_ctx,
                    mock_request_two_obj_decoded_token):
        """Should remove a comment when deleted
         Args:
            request_ctx (object): request client context
            mock_request_two_obj_decoded_token (object): Mock decoded_token from request object
            new_comment (object): Fixture to create a new comment
        """
        new_comment.delete()
        assert Comment.get(new_comment.id) is None
