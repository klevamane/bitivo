# Services
from api.services.request import close_expired_request

# Models
from api.models.request import RequestStatusEnum, Request
from api.models.database import db


class TestCloseExpiredRequest:
    def test_closes_an_expired_request_succeeds(self, init_db,
                                                new_expired_request):
        """Should close one expired request

        Args:
            init_db (fixture): Fixture to initialize the test database operations.
            new_expired_request (Request): Instance of an expired Request

        """
        new_expired_request.save()
        close_expired_request()

        assert new_expired_request.closed_by_system == True
        assert new_expired_request.status == RequestStatusEnum.closed
        assert new_expired_request.closed_at

    def test_closes_all_expired_requests_in_the_app_succeeds(
            self, init_db, new_expired_requests):
        """Should close all requests that have expired

        Args:
            init_db (fixture): Fixture to initialize the test database operations.
            new_expired_requests (list): List containing expired Requests

        """
        db.session.add_all(new_expired_requests)
        db.session.commit()
        close_expired_request()
        for request in new_expired_requests:
            assert request.status == RequestStatusEnum.closed
            assert request.closed_at
