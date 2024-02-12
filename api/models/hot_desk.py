"""Module for HotDeskRequest model"""
# Auditable Base Model
from .base.auditable_model import AuditableBaseModel

# Base query class
from .base.base_query import CustomBaseQuery

# Database
from .database import db

# Enum
from ..utilities.enums import HotDeskRequestStatusEnum

from sqlalchemy.event import listens_for
from sqlalchemy.orm import Session, attributes

# Models
from api.models import User

from api.models.hot_desk_response import HotDeskResponse
from sqlalchemy import and_
from sqlalchemy_utils.types import TSVectorType

# Tracker
from api.utilities.history.hot_desk_tracker import HotDeskTracker
activity_tracker = HotDeskTracker()


class HotDeskRequest(AuditableBaseModel):
    """
    Model for Hot desks Requests
    """

    __tablename__ = 'hot_desk_requests'

    requester_id = db.Column(
        db.String(60), db.ForeignKey('users.token_id'), nullable=True)
    query_class = CustomBaseQuery

    status = db.Column(
        db.Enum(HotDeskRequestStatusEnum), nullable=False, default='pending')
    hot_desk_ref_no = db.Column(db.String(60), nullable=False)
    assignee_id = db.Column(
        db.String(60), db.ForeignKey('users.token_id'), nullable=False)
    reason = db.Column(db.Text, nullable=True)
    requester = db.relationship(
        'User',
        backref='hot_desk_requester',
        primaryjoin=
        "and_(HotDeskRequest.requester_id == User.token_id, User.deleted == False)"
    )
    complaint = db.Column(db.Text, nullable=True)
    complaint_created_at = db.Column(db.DateTime, nullable=True)
    assignee = db.relationship(
        'User',
        backref='hot_desk_assignee',
        primaryjoin=
        "and_(HotDeskRequest.assignee_id == User.token_id, User.deleted == False)"
    )
    search_vector = db.Column(TSVectorType('hot_desk_ref_no', 'complaint'))

    def get_child_relationships(self):
        """Method to get all child relationships of this model"""
        return None

    def __repr__(self):
        return f'<HotDeskRequest {self.requester_id} {self.hot_desk_ref_no} {self.assignee_id}>'


@listens_for(HotDeskRequest, "after_insert")
def after_insert(mapper, connect, target):
    """
    Will call the class that sends the message
    Args:
        mapper (obj): The current model class
        connect (obj): The current database connection
        target (obj): The current model instance
    Returns:
        None
    """
    from bot.views.bot_actions import ActionResource
    from api.tasks.notifications.hot_desk import HotDeskNotifications
    from api.utilities.helpers.env_resource_adapter import adapt_resource_to_env
    from api.models.hot_desk_response import HotDeskResponse

    @listens_for(Session, 'after_flush', once=True)
    def add_hotdesk_response(session, context):
        """ will populate the hot desk response table
        args:
            session(obj): The current database session
            context(obj): Handles the details of the flush
        returns:
            None
        """
        handle_add_hot_desk(session, target)

    assignee_email = User.query_().filter_by(
        token_id=target.assignee_id).first().email
    requester_email = User.query_().filter_by(
        token_id=target.requester_id).first().email
    hot_desk_ref_no = target.hot_desk_ref_no
    hot_desk_id = target.id

    approval_menus = adapt_resource_to_env(ActionResource.approval_menus)
    approval_menus(assignee_email, requester_email, hot_desk_ref_no,
                   hot_desk_id)

    HotDeskNotifications.send_notifications_handler(target)

    activity_tracker.record_history(target, db.session, 'POST')


@listens_for(HotDeskRequest, "after_update")
def after_update(mapper, connect, target):
    """
    Will call the class that sends the message
    Args:
        mapper (obj): The current model class
        connect (obj): The current database connection
        target (obj): The current model instance
    Returns:
        None
    """

    from api.tasks.notifications.hot_desk import HotDeskNotifications

    @listens_for(Session, 'after_flush', once=True)
    def update_hotdesk_response(session, context):
        """ will update the hot desk response table
        args:
            session(obj): The current database session
            context(obj): Handles the details of the flush
        returns:
            None
        """
        handle_hot_desk_update(session, context, target)

    status_changed = attributes.get_history(target, 'status')[2]
    activity_tracker.record_history(target, db.session, 'PATCH')
    if status_changed:
        HotDeskNotifications.send_hot_desk_decision_handler(target)


def handle_hot_desk_update(session, context, target):
    """
        Listens for changes in the HotDeskRequest
        args:
            session (obj): the current database session
            context(obj): Handles the details of the flush
            target (obj): the current model instance
        returns:
            None
    """
    assignee_old_value = attributes.get_history(target, 'assignee_id')[2]
    if assignee_old_value:
        handle_add_hot_desk(session, target)

    status_new_value, _, status_old_value = attributes.get_history(target, 'status')
    if status_old_value and status_old_value[0].value != HotDeskRequestStatusEnum.approved.value:
        hot_desk_response = HotDeskResponse.__table__
        session.execute(hot_desk_response.update().where(
            and_(
                hot_desk_response.c.hot_desk_request_id == target.id,
                hot_desk_response.c.assignee_id == target.assignee_id)).values(
                    status=target.status.value))

    if status_old_value and status_new_value[0].value == HotDeskRequestStatusEnum.cancelled.value and\
        status_old_value[0].value == HotDeskRequestStatusEnum.approved.value:

        handle_add_hot_desk(session, target)

def handle_add_hot_desk(session, target):
    """ handle add hot desk response table
        args:
            session(obj): The current database session
            target (obj): The current model instance
        returns:
            None
        """
    session.add(
        HotDeskResponse(
            hot_desk_request_id=target.id,
            assignee_id=target.assignee_id,
            status=target.status.value))
