import pytest
from api.schemas.comment import CommentSchema
from api.middlewares.base_validator import ValidationError
from api.utilities.messages.error_messages import serialization_errors


class TestCommentSchema:
    """
    Test comment schema
    """

    def test_comment_schema_with_valid_data_passes(self, new_comment):
        """Should pass when valid comment data is supplied
         Args:
            new_comment (object): Fixture for a comment
        """
        data = {
            'authorId': new_comment.author_id,
            'parentId': new_comment.parent_id,
            'body': new_comment.body
        }
        schema = CommentSchema()
        serialized_data = schema.load_object_into_schema(data)
        assert serialized_data['body'] == data['body']
        assert serialized_data['parent_id'] == data['parentId']
        assert serialized_data['author_id'] == data['authorId']

    def test_comment_schema_with_invalid_data_fails(self):
        """Should fail with invalid comment data"""
        data = {}
        schema = CommentSchema()
        with pytest.raises(ValidationError) as error:
            schema.load_object_into_schema(data)
        assert error.value.error['status'] == 'error'
