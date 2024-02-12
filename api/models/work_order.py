"""Module that holds work order model class."""

from datetime import datetime

# Third Party Library
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy_utils.types import TSVectorType
# Database
from sqlalchemy.event import listens_for
from api.utilities.validators.schedule_creator import (create_schedules,
                                                       regenerate_schedules)

# Auditable Base Model
from .base.auditable_model import AuditableBaseModel
# Base Policy
from .base.base_policy import BasePolicy
from .database import db

# Base query class
from .base.base_query import CustomBaseQuery

# Enum
from ..utilities.enums import FrequencyEnum, StatusEnum


class WorkOrderPolicy(BasePolicy):
    pass


class WorkOrder(AuditableBaseModel):
    """
    model for work order
    """
    policies = {'patch': 'owner', 'delete': 'owner'}

    __tablename__ = 'work_orders'

    query_class = CustomBaseQuery

    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text, nullable=False)
    maintenance_category_id = db.Column(
        db.String, db.ForeignKey('maintenance_categories.id'), nullable=True)
    assignee_id = db.Column(
        db.String, db.ForeignKey('users.token_id'), nullable=True)
    frequency = db.Column(
        db.Enum(FrequencyEnum),
        nullable=False,
        server_default='daily',
        name='frequency')
    status = db.Column(
        db.Enum(StatusEnum),
        nullable=False,
        server_default='enabled',
        name='status')
    custom_occurrence = db.Column(JSON, nullable=True)
    start_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)
    assignee = db.relationship('User', backref='work_order')
    maintenance_category = db.relationship(
        'MaintenanceCategory', backref='maintenance_categories')
    search_vector = db.Column(TSVectorType('title', 'description'))

    def get_child_relationships(self):
        """Method to get all child relationships of a model
         Override in the subclass if the model has child models.
        """
        return None

    def __repr__(self):
        """Shows a string representation of the model

        Returns:
            String: string representation of a work order type
        """
        return f'<WorkOrder {self.title}>'

    @WorkOrderPolicy.delete_update_action()
    def update_(self, *args, **kwargs):
        return super(WorkOrder, self).update_(*args, **kwargs)

    @WorkOrderPolicy.delete_update_action()
    def delete(self, *args, **kwargs):
        return super(WorkOrder, self).delete(*args, **kwargs)


@listens_for(WorkOrder, 'after_insert')
@listens_for(WorkOrder, 'after_update')
def after_insert_update(mapper, connect, target):
    """Event handler on after insert or after update .
    Args:
        mapper (obj): The current model class
        connect (obj): The current database connection
        target (obj): The current model instance
    """

    from api.tasks.notifications.work_orders import WorkOrderNotifications

    # handles sending out work order notifications.
    WorkOrderNotifications.notify_assignee_handler(target)


@listens_for(WorkOrder, 'after_insert')
def after_insert(mapper, connect, target):
    """Event handler on after insert.
     Args:
        mapper (obj): The current model class
        connect (obj): The current database connection
        target (obj): The current model instance
     """

    create_schedules(target)


@listens_for(WorkOrder, 'after_update')
def after_update(mapper, connection, target):
    """Regenerates schedules after a work_oder is updated
     Args:
        mapper (obj): The current mapper class
        connection (obj): The current database connection
        target (obj): The current Work_order instance
    """

    state = db.inspect(target)
    changed_fields = []

    for attr in state.attrs:
        hist = state.get_history(attr.key, True)

        if hist.has_changes():
            changed_fields.append(attr.key)

    if changed_fields and 'deleted' not in changed_fields:
        regenerate_schedules(target, changed_fields)
