""" Tests for request model """

from api.models import Request
from api.models.request import request_summary
# Mocks
from tests.mocks.requests import SUMMARY_REQUEST


class TestRequestModel:
    """ Test Request model"""

    def test_new_request(self, init_db, new_request):
        """Should create a new request

        Args:
            init_db (object): Fixture to initialize the test database operations.
            new_request (object): Fixture to create a new request
        """
        assert new_request == new_request.save()

    def test_update(self, new_request, request_ctx,
                    mock_request_two_obj_decoded_token):
        """Should update request

        Args:
            new_request (object): Fixture to create a new request
        """
        new_request.update_(subject='its my ipad screen that cracked')
        assert Request.get(
            new_request.id).subject == 'its my ipad screen that cracked'

    def test_get(self, new_request):
        """Should retrieve a request

        Args:
            new_request (object): Fixture to create a new request
        """
        assert Request.get(new_request.id) == new_request

    def test_query(self, new_request):
        """Should get a list of available requests

        Args:
            new_request (object): Fixture to create a new request
        """
        request_query = new_request.query_()
        assert isinstance(request_query.all(), list)

    def test_delete(self, new_request, request_ctx,
                    mock_request_two_obj_decoded_token):
        """Should delete a request

        Args:
            new_request (object): Fixture to create a new request
            request_ctx (object): request client context
            mock_request_obj_decoded_token (object): Mock decoded_token from request client context
        """
        new_request.delete()
        assert Request.get(new_request.id) is None

    def test_request_model_string_representation(self, new_request):
        """ Should compute the string representation of a request

        Args:
            new_request (object): Fixture to create a new request
        """

        assert repr(new_request) == f'<Request {new_request.subject}>'

    def test_total_request(self):
        """should compute the total summary request

        """

        assert request_summary() == SUMMARY_REQUEST['requestSummary']
