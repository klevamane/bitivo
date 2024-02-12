"""Module for resource model"""

from .base.auditable_model import AuditableBaseModel

# Base query class
from .base.base_query import CustomBaseQuery

from .database import db


class Resource(AuditableBaseModel):
    """
    Model for resource
    """

    __tablename__ = 'resources'

    query_class = CustomBaseQuery

    name = db.Column(db.String(60), nullable=False)

    def get_child_relationships(self):
        """
        Method to get all child relationships of this model

        Returns:
             children(tuple): children of this model
        """
        return ()

    def __repr__(self):
        return f'<Resource: {self.name}>'
