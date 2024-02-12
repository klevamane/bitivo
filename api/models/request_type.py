"""Module that holds RequestType model class"""

# Third party libraries
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.event import listens_for
from sqlalchemy.orm.attributes import get_history

# Database
from .database import db

# Models
from .base.auditable_model import AuditableBaseModel
# Base Policy
from .base.base_policy import BasePolicy

# Base query class
from .base.base_query import CustomBaseQuery

# Utilities
from ..utilities.enums import RequestStatusEnum

# Activity Tracker
from api.utilities.history.request_type_activity_tracker import RequestTypeTracker
from api.utilities.history.tracker_listener import activity_tracker_listener


class RequestTypePolicy(BasePolicy):
    pass


class RequestType(AuditableBaseModel):
    """ Model for request types """
    policies = {'patch': 'owner', 'delete': 'owner'}

    __tablename__ = 'request_types'

    query_class = CustomBaseQuery

    title = db.Column(db.String(60), nullable=False)
    response_time = db.Column(JSON, nullable=False)
    resolution_time = db.Column(JSON, nullable=False)
    closure_time = db.Column(JSON, nullable=False)
    center_id = db.Column(
        db.String, db.ForeignKey('centers.id'), nullable=False)
    assignee_id = db.Column(
        db.String, db.ForeignKey('users.token_id'), nullable=False)

    # Relationship between a user and a request type
    assignee = db.relationship(
        'User', backref='request_types', cascade='save-update, delete')

    # Relationship between the request type and requests
    requests = db.relationship(
        'Request',
        backref='request_types',
        cascade='save-update, delete',
        lazy='dynamic')

    def get_child_relationships(self):
        """Method to get all child relationships of a model
         Override in the subclass if the model has child models.
        """

        return (self.requests, )

    @RequestTypePolicy.delete_update_action()
    def update_(self, *args, **kwargs):
        return super(RequestType, self).update_(*args, **kwargs)

    @RequestTypePolicy.delete_update_action()
    def delete(self, *args, **kwargs):
        return super(RequestType, self).delete(*args, **kwargs)

    @property
    def assignee(self):
        """Property method to return the asset's assignee

        Returns:
            assignee (obj): The asset's assignee. Can be either a user or a
            space
        """
        from . import User
        assignee = User.get(self.assignee_id)
        return assignee

    def __repr__(self):
        """ Shows a string representation of the model
        Returns:
            String: string representation of a request type
        """
        return f'<RequestType {self.title}>'

    @property
    def requests_count(self):
        """Property method to return the number of requests
        on a specific request type

        Returns:
            request_count (int): The number of requests belonging
            to the request type
        """
        from . import Request
        return Request.query_().filter(
            Request.request_type_id == self.id).count()


activity_tracker_listener(RequestType, RequestTypeTracker)


@listens_for(RequestType, 'after_insert')
@listens_for(RequestType, 'after_update')
def after_insert_update(mapper, connect, target):
    """Sends request type email notifications.

    Args:
        connect (obj): The current database connection
        target (obj): The current model instance
    """

    from ..tasks.notifications.request_type import RequestTypeNotification
    RequestTypeNotification.request_type_notifier_handler(target)


@listens_for(RequestType, 'after_update')
def receive_new_assignee_after_update(mapper, connection, target):
    """Updates responder id of active requests under request category

    Args:
        mapper (obj): The target mapper
        connect (obj): The current database connection
        target (obj): The current model instance
    """

    @listens_for(db.session, "after_flush", once=True)
    def receive_session_after_flush(session, context):
        """Receives the current session of the transaction after flush

        - Receives the current session
        - Checks in history for assignee change
        - Then queries for requests with status in_progress and open
        - Update all the requests responder_id with the changed assignee

        Args:
            session (obj): current session object
            context (obj): session transaction context
        """
        from ..models import Request
        new_assignee, unchanged_assignee, old_assignee = get_history(
            target, 'assignee_id')
        if new_assignee and old_assignee and new_assignee[0] != old_assignee[0]:
            requests = session.query(Request).filter(
                (Request.status == RequestStatusEnum.in_progress)
                | (Request.status == RequestStatusEnum.open),
                (Request.request_type_id == target.id)).filter_by(
                    deleted=False)
            requests.update({Request.responder_id: new_assignee[0]})
