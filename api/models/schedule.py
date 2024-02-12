"""Module that holds schedule model class."""

# Auditable Base Model
from .base.auditable_model import AuditableBaseModel

# Base query class
from .base.base_query import CustomBaseQuery

# Third Party Library
from sqlalchemy.dialects.postgresql import ARRAY

# Database
from .database import db
from sqlalchemy.event import listens_for

# Enum
from ..utilities.enums import ScheduleStatusEnum


class Schedule(AuditableBaseModel):
    """Model for schedule."""

    __tablename__ = 'schedules'

    query_class = CustomBaseQuery

    work_order_id = db.Column(
        db.String, db.ForeignKey('work_orders.id'), nullable=False)
    assignee_id = db.Column(
        db.String, db.ForeignKey('users.token_id'), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(
        db.Enum(ScheduleStatusEnum), nullable=False, name='status')
    attachments = db.Column(ARRAY(db.Text), nullable=True)
    work_order = db.relationship('WorkOrder', backref='schedules')
    assignee = db.relationship('User', backref='schedules')
    comments = db.relationship(
        'Comment', primaryjoin='foreign(Comment.parent_id) == Schedule.id')

    def get_child_relationships(self):
        """Method to get all child relationships of a model
         Override in the subclass if the model has child models.
        """
        return None

    def __repr__(self):
        """Shows a string representation of the model

        Returns:
            String: string representation of a schedule
        """
        return f'<Schedule: schedule: {self.id} status: {self.status}>'


# SQLAlchemy event handler
@listens_for(Schedule, 'after_update')
def after_update(mapper, connect, target):
    """When Schedule after a work order schedule status is done.

    Args:
        mapper (obj): The current mapper class
        connect (any): The current database connection
        target (any): The model instance

    Returns:
        None
    """

    if target.status == ScheduleStatusEnum.done:
        from ..tasks.notifications.schedule import SchedulesNotifications
        SchedulesNotifications.schedule_status_notification_handler(target)
