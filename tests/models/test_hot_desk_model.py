"""Module to test HotDeskRequest model"""

# Third party libraries
from sqlalchemy import exc
import pytest

# Local import
from api.models import HotDeskRequest


class TestHotDeskRequestModel:
    """Tests for HotDeskRequest model"""

    def test_create_new_hot_desk_request_succeeds(self, init_db,
                                                  new_hot_desk_request):
        """Should create a new hot desk

        Args:
            new_hot_desk_request (object): Fixture to create a new hot desk
        """
        assert new_hot_desk_request == new_hot_desk_request.save()

    def test_update_hot_desk_succeeds(self, init_db, new_hot_desk_request,
                                      new_user):
        """Should update hot desk

        Args:
            new_hot_desk_request (object): Fixture to create a hot desk
        """

        value = new_user.email
        new_hot_desk_request.save()
        hot_desk = HotDeskRequest.query_().filter_by(
            id=new_hot_desk_request.id).first()
        hot_desk.update_(email=value, hot_desk_ref_no="3M 66")
        hot_desk_request = HotDeskRequest.get(new_hot_desk_request.id)
        assert hot_desk_request.email == value
        assert hot_desk_request.hot_desk_ref_no == "3M 66"

    def test_create_new_hot_desk__with_complaint_succeeds(
            self, init_db, new_hot_desk_request_with_complaint):
        """Should update hot desk

        Args:
            new_hot_desk_request_with_complaint (object): Fixture to create a hot desk with a complaint
            with the complaint column populated
        """
        assert new_hot_desk_request_with_complaint == \
            new_hot_desk_request_with_complaint.save()

    def test_get_a_hot_desk_succeeds(self, init_db, new_hot_desk_request):
        """Should retrieve a hot desk

        Args:
            new_hot_desk_request (object): Fixture to create a new hot desk
        """
        new_hot_desk_request.save()
        assert HotDeskRequest.get(
            new_hot_desk_request.id) == new_hot_desk_request

    def test_query_all_hot_desks_succeeds(self, init_db, new_hot_desk_request):
        """Should get a list of hot desks

        Args:
            new_hot_desk_request (object): Fixture to create a new hot desks
        """

        new_hot_desk_request_query = new_hot_desk_request.query_()
        assert isinstance(new_hot_desk_request_query.all(), list)

    def test_get_child_relationships_(self, init_db, new_hot_desk_request):
        """Get resources relating to the HotDeskRequest model

        Args:
            new_hot_desk_request (object): Fixture to create a hot desk
        """

        assert new_hot_desk_request.get_child_relationships() is None

    def test_delete_a_hot_desk_succeeds(self, init_db, new_hot_desk_request,
                                        request_ctx,
                                        mock_request_obj_decoded_token):
        """Should delete a hot desk

        Args:
            new_hot_desk_request (object): Fixture to create a new hot desk
        """
        new_hot_desk_request.delete()
        assert HotDeskRequest.get(new_hot_desk_request.id) is None

    def test_hot_desk_order_model_string_representation(
            self, init_db, new_hot_desk_request):
        """Should compute the string representation

        Args:
            new_hot_desk_request (object): Fixture to create a new hot desk
        """

        assert repr(
            new_hot_desk_request
        ) == f'<HotDeskRequest {new_hot_desk_request.requester_id} {new_hot_desk_request.hot_desk_ref_no} {new_hot_desk_request.assignee_id}>'

    def test_search_hot_desk_succeeds(self, new_hot_desk_request):
        """Should retrieve a hot_desk_request that matches provided string

        Args:
            new_hot_desk_request (object): Fixture to create a new hot_desk_request
        """
        hot_desk_request_query = new_hot_desk_request.query_()
        query_result = hot_desk_request_query.search('feel').all()
        assert len(query_result) >= 1
        assert query_result[0].complaint == 'not feeling too well'

    def test_instance_with_invalid_assignee_id_fails(
            self, init_db, hot_desk_with_invalid_assignee_id):
        """Should not create new hot desk

        IntegrityError is expected to be raised

        Args:
            hot_desk_with_invalid_assignee_id(object):
                                                    Fixture for hot desk with wrong assignee_id

        """

        with pytest.raises(exc.IntegrityError):
            hot_desk_with_invalid_assignee_id.save()

    def test_instance_with_invalid_requester_id_fails(
            self, init_db, hot_desk_with_invalid_requster_id):
        """Should not create new hot desk

        IntegrityError is expected to be raised

        Args:
            hot_desk_with_invalid_requster_id(object):
                                                Fixture for hot desk with wrong requester_id

        """

        with pytest.raises(exc.IntegrityError):
            hot_desk_with_invalid_requster_id.save()

    def test_instance_with_missing_fields_fails(self, init_db,
                                                hot_desk_with_missing_fields):
        """Should not create new hot desk

        IntegrityError is expected to be raised

        Args:
            hot_desk_with_missing_fields(object):
                                                Fixture for hot desk with missing field

        """

        with pytest.raises(exc.IntegrityError):
            hot_desk_with_missing_fields.save()
