"""Module for HotDeskResponse model"""

# Auditable Base Model
from .base.auditable_model import AuditableBaseModel

# Base query class
from .base.base_query import CustomBaseQuery

# Database
from .database import db

# Enum
from ..utilities.enums import HotDeskResponseStatusEnum


class HotDeskResponse(AuditableBaseModel):
    """
    Model for tracking Hot desks Response
    """

    __tablename__ = 'hot_desk_responses'

    status = db.Column(
        db.Enum(HotDeskResponseStatusEnum), nullable=False, default='pending', name='status')
    query_class = CustomBaseQuery
    assignee_id = db.Column(
        db.String(60), db.ForeignKey('users.token_id'), nullable=False)
    hot_desk_request_id = db.Column(
        db.String(60), db.ForeignKey('hot_desk_requests.id'), nullable=False)
    is_escalated = db.Column(db.Boolean, default=False, nullable=True)

    def get_child_relationships(self):
        """Method to get all child relationships of this model"""
        return None

    def __repr__(self):
        return f'<HotDeskResponse {self.hot_desk_request_id} {self.status} {self.assignee_id}>'
