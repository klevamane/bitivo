"""Module for role model"""

from sqlalchemy import select, func

from .base.auditable_model import AuditableBaseModel

# Base query class
from .base.base_query import CustomBaseQuery

# Base Policy
from .base.base_policy import BasePolicy
from .database import db


class RolePolicy(BasePolicy):
    pass


class Role(AuditableBaseModel):
    """
    Model for roles
    """
    policies = {'patch': 'owner', 'delete': 'owner'}

    __tablename__ = 'roles'

    query_class = CustomBaseQuery

    title = db.Column(db.String(60), nullable=False)  # pylint: disable=E1101
    description = db.Column(db.String(250), nullable=False)
    users = db.relationship(  # pylint: disable=E1101
        'User',
        backref='role',
        cascade='delete',
        lazy='dynamic')

    resource_access_levels = db.relationship(
        'ResourceAccessLevel',
        backref='role',
        cascade='save-update,delete',
        lazy='dynamic')
    super_user = db.Column(db.Boolean, nullable=True, default=False)

    @property
    def user_count(self):
        """
        Get users count for roles

        Returns:
            result(int): users count for corresponding roles
        """

        from .user import User

        query = select([func.count(User.id)]).where(User.role_id == self.id)
        result = db.engine.execute(query).scalar()
        return result

    def get_child_relationships(self):
        """
        Method to get all child relationships of this model

        Returns:
             children(tuple): children of this model
        """
        return (self.users, )

    def __repr__(self):
        return f'<Role: {self.title}>'

    @RolePolicy.delete_update_action()
    def update_(self, *args, **kwargs):
        return super(Role, self).update_(*args, **kwargs)

    @RolePolicy.delete_update_action()
    def delete(self, *args, **kwargs):
        return super(Role, self).delete(*args, **kwargs)
