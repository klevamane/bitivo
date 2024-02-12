"""Module for History model"""
# system imports
from datetime import datetime

# database & models
from .base.base_model import BaseModel

# Base query class
from .base.base_query import CustomBaseQuery

from .database import db
from sqlalchemy.dialects.postgresql import JSON


class History(BaseModel):
    """Model for history.
    Tracks user activity on different resources
    """

    query_class = CustomBaseQuery

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resource_id = db.Column(db.String(60), index=True, nullable=False)
    resource_type = db.Column(db.String(60), index=True, nullable=False)
    action = db.Column(db.String(60), index=True, nullable=False)
    actor_id = db.Column(
        db.String, db.ForeignKey('users.token_id'), nullable=False)
    actor = db.relationship('User')
    activity = db.Column(db.Text(), nullable=False)

    def get_child_relationships(self):
        """Method to get all child relationships of this model

        Returns:
            None
        """
        return None

    def __repr__(self):
        return f'<History on {self.resource_type}>'
