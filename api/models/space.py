"""Module for space model"""

from .base.auditable_model import AuditableBaseModel

# Base query class
from .base.base_query import CustomBaseQuery

# Base Policy
from .base.base_policy import BasePolicy
from .database import db


class SpacePolicy(BasePolicy):
    pass


class Space(AuditableBaseModel):
    """
    Model for spaces
    """
    policies = {'patch': 'owner', 'delete': 'owner'}

    __tablename__ = 'spaces'

    query_class = CustomBaseQuery

    name = db.Column(db.String(60), nullable=False)

    parent_id = db.Column(
        db.String(60), db.ForeignKey('spaces.id'), nullable=True)

    space_type_id = db.Column(
        db.String(60), db.ForeignKey('space_types.id'), nullable=False)

    center_id = db.Column(
        db.String(60), db.ForeignKey('centers.id'), nullable=False)

    spaceType = db.relationship('SpaceType', lazy='joined')

    children = db.relationship('Space', lazy='joined')

    children_reference = db.relationship('Space', lazy='dynamic')

    @property
    def children_count(self):
        """Get direct children count"""

        return self.children_reference.count()

    @SpacePolicy.delete_update_action()
    def update_(self, *args, **kwargs):
        return super(Space, self).update_(*args, **kwargs)

    @SpacePolicy.delete_update_action()
    def delete(self, *args, **kwargs):
        return super(Space, self).delete(*args, **kwargs)

    def get_child_relationships(self):
        """
        Method to get all child relationships of this model

        Returns:
             children(tuple): children of this model
        """
        return (self.children_reference, )

    def __repr__(self):
        return f'<Space {self.name} {self.children}>'
