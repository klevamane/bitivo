"""Module to test HotDeskResponse model"""

# Third party libraries
from sqlalchemy import exc
import pytest

# Local import
from api.models import HotDeskResponse, HotDeskRequest


class TestHotDeskResponseModel:
    """Tests for HotDeskResponse model"""

    def test_create_new_hot_desk_response_succeeds(self, init_db,
                                                   new_hot_desk_response):
        """Should create a new hot desk response

        Args:
            new_hot_desk_response (object): Fixture to create a new hot desk response
        """
        assert new_hot_desk_response == new_hot_desk_response.save()

    def test_hot_desk_response_status_update_succeeds(
            self, init_db, new_hot_desk_response, new_user):
        """Should update hot desk response

        Args:
            new_hot_desk_response (object): Fixture to create a hot desk response
        """

        new_hot_desk_response.save
        new_hot_desk_response.update_(status='approved')
        assert new_hot_desk_response.status.value == "approved"

    def test_get_a_hot_desk_succeeds(self, init_db, new_hot_desk_response):
        """Should retrieve a hot desk

        Args:
            new_hot_desk_response (object): Fixture to create a new hot desk response
        """
        new_hot_desk_response.save()
        assert HotDeskResponse.get(
            new_hot_desk_response.id) == new_hot_desk_response

    def test_get_child_relationships_(self, init_db, new_hot_desk_response):
        """Get resources relating to the HotDeskResponse model

        Args:
            new_hot_desk_response (object): Fixture to create a hot desk response
        """

        assert new_hot_desk_response.get_child_relationships() is None

    def test_delete_a_hot_desk_succeeds(self, init_db, new_hot_desk_response,
                                        request_ctx,
                                        mock_request_obj_decoded_token):
        """Should delete a hot desk

        Args:
            new_hot_desk_request (object): Fixture to create a new hot desk
        """
        new_hot_desk_response.delete()
        assert HotDeskResponse.get(new_hot_desk_response.id) is None

    def test_hot_desk_order_model_string_representation(
            self, init_db, new_hot_desk_response):
        """Should compute the string representation

        Args:
            new_hot_desk_response (object): Fixture to create a new hot desk
        """

        assert repr(
            new_hot_desk_response
        ) == f'<HotDeskResponse {new_hot_desk_response.hot_desk_request_id} {new_hot_desk_response.status} {new_hot_desk_response.assignee_id}>'

    def test_new_hot_desk_response_created_when_assignee_id_changes(
            self, init_db, test_hot_desk_request, new_user_two, request_ctx,
            mock_request_two_obj_decoded_token):
        """ Should add a new hot desk response if assigne_id for hot desk request changes
        Args:
            test_hot_desk_request(object): Fixture to create a new hot desk request
            new_user_two(object): Fixture to create a new user
        """
        new_user_two.save()
        test_hot_desk_request.save()
        hot_desk_request = HotDeskRequest.query_().filter_by(
            id=test_hot_desk_request.id).first()
        hot_desk_request.update_(assignee_id=new_user_two.token_id)
        hot_desk_response = HotDeskResponse.query_().filter_by(
            assignee_id=new_user_two.token_id,
            hot_desk_request_id=test_hot_desk_request.id).first()
        assert test_hot_desk_request.assignee_id == hot_desk_response.assignee_id
