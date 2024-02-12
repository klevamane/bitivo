"""Module for Request related services"""

# Standard Library
from datetime import timedelta, datetime

# Models
from api.models import Request
from api.models.database import db

# Services
from . import celery_scheduler


@celery_scheduler.task(name='close_expired_request')
def close_expired_request():
    """Closes all the requests whose closure_time has expired
        Returns:
            None
    """
    requests = Request.query_().filter_by(status="completed").all()
    expired_requests = []

    for request in requests:
        closure_time = request.request_type.closure_time
        time_completed = request.completed_at
        closure_time_diff = timedelta(**closure_time)
        closure_time_has_expired = datetime.now() > \
                                   time_completed + closure_time_diff

        if closure_time_has_expired:
            expired_requests.append(request.id)

    expired_requests_query = Request.query.filter(
        Request.id.in_(expired_requests))

    expired_requests_query.update({
        Request.status: "closed",
        Request.closed_by_system: True,
        Request.closed_at: datetime.now()
    },
                                  synchronize_session='fetch')

    db.session.commit()
