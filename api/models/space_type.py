"""Module for space type model"""
from .base.auditable_model import AuditableBaseModel

# Base query class
from .base.base_query import CustomBaseQuery

from .database import db


class SpaceType(AuditableBaseModel):
    """
    Model for space type
    """

    __tablename__ = 'space_types'

    query_class = CustomBaseQuery

    type = db.Column(db.String(60), nullable=False, unique=True)
    color = db.Column(db.String(60), unique=True, nullable=False)

    spaces = db.relationship(
        'Space', backref='space_type', cascade='delete', lazy='dynamic')

    def get_child_relationships(self):
        """
        Method to get all child relationships of this model

        Returns:
             children(tuple): children of this model
        """
        return (self.spaces, )

    def __repr__(self):
        return f'<SpaceType {self.type}>'
