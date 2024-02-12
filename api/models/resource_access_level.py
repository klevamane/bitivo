"""Module for resource access levels model"""

from .base.auditable_model import AuditableBaseModel

# Base query class
from .base.base_query import CustomBaseQuery

from .database import db

# An association table between permission and resource access level
resource_permissions = db.Table(
    'resource_permissions',
    db.Column(
        'resource_access_level_id',
        db.String,
        db.ForeignKey('resource_access_levels.id'),
        primary_key=True),
    db.Column(
        'permission_id',
        db.String,
        db.ForeignKey('permissions.id'),
        primary_key=True))


class ResourceAccessLevel(AuditableBaseModel):
    """
    Model for resources access level model
    """

    __tablename__ = 'resource_access_levels'

    query_class = CustomBaseQuery

    role_id = db.Column(db.String, db.ForeignKey('roles.id'), nullable=False)
    resource_id = db.Column(
        db.String, db.ForeignKey('resources.id'), nullable=False)
    resource = db.relationship('Resource')
    permissions = db.relationship('Permission', secondary=resource_permissions)

    def get_child_relationships(self):
        """
        Method to get all child relationships of this model

        Returns:
             children(tuple): children of this model
        """
        return ()

    def __repr__(self):
        return f'<ResourceAccessLevel: resource_id: {self.resource_id} role_id: {self.role_id}>'
