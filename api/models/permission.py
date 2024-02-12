"""Module for permission model"""

from .base.auditable_model import AuditableBaseModel
from .base.soft_delete import BaseSoftDelete
from .database import db


class Permission(AuditableBaseModel):
    """
    Model for permissions
    """

    __tablename__ = 'permissions'

    query_class = BaseSoftDelete

    type = db.Column(db.String(60), nullable=False, unique=True)  # pylint: disable=E1101

    def get_child_relationships(self):
        """
        Method to get all child relationships of this model

        Returns:
             children(tuple): children of this model
        """
        return ()

    def __repr__(self):
        return f'<Permission {self.type}>'
