"""Module for comment model"""

# SQLAlchemy
from sqlalchemy.event import listens_for
import enum
from sqlalchemy_utils.types import TSVectorType

# Models
from .base.auditable_model import AuditableBaseModel

# Base query class
from .base.base_query import CustomBaseQuery
# Base Policy
from .base.base_policy import BasePolicy
from .database import db

from ..utilities.enums import ParentType


class CommentPolicy(BasePolicy):
    pass


class Comment(AuditableBaseModel):
    """Model for a comment."""

    policies = {'patch': 'owner', 'delete': 'owner'}
    __tablename__ = 'comments'

    query_class = CustomBaseQuery

    body = db.Column(db.Text, nullable=False)
    parent_id = db.Column(db.String, nullable=True)
    search_vector = db.Column(TSVectorType('body'))
    author_id = db.Column(
        db.String, db.ForeignKey('users.token_id'), nullable=False)
    parent_type = db.Column(
        db.Enum(ParentType),
        nullable=True,
        server_default='Request',
        name='parent_type')
    author = db.relationship('User')

    def get_child_relationships(self):
        """Method to get all child relationships of this model.

        Returns:
            children(tuple): children of this model
        """
        return None

    def __repr__(self):
        """Computes the string representation of comment"""

        return f'<Comment {self.body}>'

    @CommentPolicy.delete_update_action()
    def update_(self, *args, **kwargs):
        return super(Comment, self).update_(*args, **kwargs)

    @CommentPolicy.delete_update_action()
    def delete(self, *args, **kwargs):
        return super(Comment, self).delete(*args, **kwargs)


# SQLAlchemy event handler
@listens_for(Comment, 'after_insert')
def after_insert(mapper, connect, target):
    """Runs when a comment is inserted

    Args:
        mapper (obj): The current model class
        connect (obj): The current database connection
        target (obj): The current model instance

    Returns:
        None
    """
    schedule_value, request_value = ParentType.Schedule.value, ParentType.Request.value
    target_values = [schedule_value, request_value]
    if target.parent_type.value in target_values:
        from ..tasks.notifications.comment import CommentNotifications
        CommentNotifications.comment_notification_handler(target)
