"""Module that holds request model class."""

from sqlalchemy import text

# Third Party Library
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Sequence
from sqlalchemy.event import listens_for

# Database
from .database import db

# Auditable Base Model
from .base.auditable_model import AuditableBaseModel

# Base query class
from .base.base_query import CustomBaseQuery
# Base Policy
from .base.base_policy import BasePolicy

# Utilities
from ..utilities.enums import RequestStatusEnum
from ..utilities.server_events import publish

# Standard Library
from datetime import datetime as dt, timedelta

from . import RequestType
from ..utilities.sql_queries import sql_queries

# Activity Tracker
from api.utilities.history.request_activity_tracker import RequestTracker
from api.utilities.history.tracker_listener import activity_tracker_listener


class RequestPolicy(BasePolicy):
    pass


class Request(AuditableBaseModel):
    """
    Model for requests
    """

    policies = {'patch': 'owner', 'delete': 'owner'}

    __tablename__ = 'requests'

    query_class = CustomBaseQuery

    serial_number = db.Column(db.Integer, Sequence('requests_id_seq'))
    subject = db.Column(db.String(60), nullable=False)
    request_type_id = db.Column(
        db.String, db.ForeignKey('request_types.id'), nullable=False)
    center_id = db.Column(
        db.String, db.ForeignKey('centers.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    attachments = db.Column(ARRAY(db.Text), nullable=True)
    requester_id = db.Column(
        db.String, db.ForeignKey('users.token_id'), nullable=False)
    responder_id = db.Column(
        db.String, db.ForeignKey('users.token_id'), nullable=True)
    assignee_id = db.Column(
        db.String, db.ForeignKey('users.token_id'), nullable=True)

    requester = db.relationship(
        'User',
        backref='requests',
        primaryjoin=
        "and_(Request.requester_id == User.token_id, User.deleted == False)")
    responder = db.relationship(
        'User',
        backref='request_responses',
        primaryjoin=
        "and_(Request.responder_id == User.token_id, User.deleted == False)")
    assignee = db.relationship(
        'User',
        backref='assignee',
        primaryjoin=
        "and_(Request.assignee_id == User.token_id, User.deleted == False)")

    comments = db.relationship(
        'Comment', primaryjoin='foreign(Comment.parent_id) == Request.id')
    request_type = db.relationship('RequestType')

    status = db.Column(
        db.Enum(RequestStatusEnum),
        nullable=False,
        server_default='open',
        name='status')
    closed_by_system = db.Column(db.Boolean, nullable=True, default=False)
    in_progress_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    closed_at = db.Column(db.DateTime, nullable=True)
    due_by = db.Column(db.DateTime, nullable=True)

    # Attribute to track status
    _old_status = None

    def get_child_relationships(self):
        """Method to get all child relationships of a model
         Override in the subclass if the model has child models.
        """
        return None

    def __repr__(self):
        """ Shows a string representation of the model

        Returns:
            String: string representation of a request type
        """
        return f'<Request {self.subject}>'

    @RequestPolicy.delete_update_action()
    def update_(self, *args, **kwargs):
        return super(Request, self).update_(*args, **kwargs)

    @RequestPolicy.delete_update_action()
    def delete(self, *args, **kwargs):
        return super(Request, self).delete(*args, **kwargs)


activity_tracker_listener(Request, RequestTracker)


@listens_for(Request, 'before_insert')
def before_insert(mapper, connect, target):
    """Sets the request due_by

        Sets the request due_by before the request is inserted into the
        database and saves it in the due by field.

        Args:
            mapper (obj): The current model class
            connect (obj): The current database connection
            target (obj): The current model instance

        """

    request_type = RequestType.get(target.request_type_id)

    target.responder_id = request_type.assignee.token_id


@listens_for(Request, 'before_update')
def before_update(mapper, connect, target):
    """Sets the responder id when the request type is changed.
    Sets the request responder id to be the assignee id of the request type
    just before the request is updated into the database.
    Args:
        mapper (obj): The current model class
        connect (obj): The current database connection
        target (obj): The current model instance
    """

    request_type = RequestType.get(target.request_type_id)

    if target.status == RequestStatusEnum.in_progress.value:
        due_by = request_type.resolution_time
        days = due_by.get('days', '')
        hours = due_by.get('hours', '')
        minutes = due_by.get('minutes', '')
        target.due_by = dt.now() + timedelta(
            days=days, hours=hours, minutes=minutes)

    target.responder_id = request_type.assignee.token_id


@listens_for(Request, 'after_insert')
def after_insert(mapper, connect, target):
    """Event handler on after insert.

    Args:
        mapper (obj): The current model class
        connect (obj): The current database connection
        target (obj): The current model instance

    """
    #handle sending of events to client when new request is inserted to db.
    responder_id = target.responder_id
    where_clause = ['responder_id', 'like', responder_id.lower()]
    responder_summary = request_summary(*where_clause)
    publish({
        'responderId': responder_id,
        'totalOpenRequests': responder_summary['totalOpenRequests'] + 1
    }, 'new_requests')

    from api.tasks.notifications.request import RequestNotifications

    # handles sending out the notification.
    RequestNotifications.notify_request_type_assignee_handler(target)


@listens_for(Request, 'after_update')
def after_update(mapper, connect, target):
    """Event handler on after update

    Args:
        mapper (obj): The current mapper class
        connect (obj): The current database connection
        target (obj): The current model instance
    """

    responder_id = target.responder_id
    where_clause = ['responder_id', 'like', responder_id.lower()]
    responder_requests_summary = request_summary(*where_clause)
    if target.status == RequestStatusEnum.in_progress:
        publish({
            'responderId':
            responder_id,
            'totalInProgressRequests':
            responder_requests_summary['totalInProgressRequests'] + 1
        }, 'in_progress_requests')

    if target.status == RequestStatusEnum.completed:
        publish({
            'responderId':
            responder_id,
            'totalCompletedRequests':
            responder_requests_summary['totalCompletedRequests'] + 1
        }, 'completed_requests')

    if target.status == RequestStatusEnum.closed:
        publish({
            'responderId':
            responder_id,
            'totalClosedRequests':
            responder_requests_summary['totalClosedRequests'] + 1
        }, 'closed_requests')

    from ..tasks.notifications.request import RequestNotifications

    RequestNotifications.notify_technician_handler(target)


@listens_for(Request.status, 'set')
def set_status(target, value, oldvalue, initiator):
    """Event handler on set status attribute

    Args:
        target (obj): The current model instance
        value (any): The value being set
        oldvalue (any): The previous value being replaced
        initiator (obj): Represents the initiation of the event
    """

    target._old_status = oldvalue


@listens_for(Request, 'after_update')
def after_update(mapper, connect, target):
    """Gets the subject, status, responder name and responder id then
        sends out an email after every update on the status.

    Args:
        mapper (obj): The current mapper class
        connect(any): The current database connection
        target(any): The model instance
    """
    from api.tasks.notifications.request import RequestNotifications
    RequestNotifications.status_change_handler(target)


def request_summary(*where_clause):
    """ Query summary of all the request

        Args :
            Request(tuple):where clause from the dynamic filter

         Returns:
            dict: a dictionary of totalRequest,
            totalOpenRequest, totalClosedRequest,
            totalInProgressRequest and totalOverdueRequests
    """

    extract_where = " "
    try:
        key, ops, values = where_clause
    except ValueError:
        extract_where = extract_where
    else:
        extract_where = f"""where lower({key})  {ops}  '%{values}%'"""

    request_summary_sql_query = sql_queries['get_summary_request'].format(
        extract_where)

    result = db.engine.execute(text(request_summary_sql_query)).first()

    (total_requests, total_open_requests, total_in_progress_requests,
     total_completed_requests, total_closed_requests,
     total_over_due_requests) = result

    return {
        'totalRequests': total_requests or 0,
        'totalOpenRequests': total_open_requests or 0,
        'totalInProgressRequests': total_in_progress_requests or 0,
        'totalCompletedRequests': total_completed_requests or 0,
        'totalClosedRequests': total_closed_requests or 0,
        'totalOverdueRequests': total_over_due_requests or 0
    }
