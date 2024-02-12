""" Tests for request type model """
# Models
from api.models import RequestType

# Enums
from api.utilities.enums import RequestStatusEnum


class TestRequestTypeModel:
    """ Test RequestType model. """

    def test_new_request_type(self, init_db, new_request_type):
        """Should create a new request type.

        Args:
            init_db (object): Fixture to initialize the test database operations.
            new_request_type (object): Fixture to create a new request type.
        """
        assert new_request_type == new_request_type.save()

    def test_update(self, new_request_type, request_ctx,
                    mock_request_two_obj_decoded_token):
        """Should update request type.

        Args:
            new_request_type (object): Fixture to create a new request type
        """
        new_request_type.update_(title='new_title')
        assert RequestType.get(new_request_type.id).title == 'new_title'

    def test_get(self, new_request_type):
        """Should retrieve a request type

        Args:
            new_request_type (object): Fixture to create a new request type
        """
        assert RequestType.get(new_request_type.id) == new_request_type

    def test_query(self, new_request_type):
        """Should get a list of available request types

        Args:
            new_request_type (object): Fixture to create a new request type
        """
        request_type_query = new_request_type.query_()
        assert isinstance(request_type_query.all(), list)

    def test_delete(self, new_request_type, request_ctx,
                    mock_request_two_obj_decoded_token):
        """Should delete a request type

        Args:
            new_request_type (object): Fixture to create a new request type
            request_ctx (object): request client context
            mock_request_obj_decoded_token (object): Mock decoded_token from request client context
        """
        new_request_type.delete()
        assert RequestType.get(new_request_type.id) is None

    def test_request_type_model_string_representation(self, new_request_type):
        """ Should compute the string representation of a request type

        Args:
            new_request_type (object): Fixture to create a new request type
        """

        assert repr(
            new_request_type) == f'<RequestType {new_request_type.title}>'
