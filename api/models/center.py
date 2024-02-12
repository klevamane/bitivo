"""Module for center model"""

from sqlalchemy.orm import column_property
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import select, func
from sqlalchemy.event import listens_for
from sqlalchemy_utils.types import TSVectorType
# Base Policy
from .base.base_policy import BasePolicy
from . import User
from .base.auditable_model import AuditableBaseModel
from .database import db

# Base query class
from .base.base_query import CustomBaseQuery


class CenterPolicy(BasePolicy):
    pass


class Center(AuditableBaseModel):
    """
    Model for centers
    """
    policies = {'patch': 'owner', 'delete': 'owner'}

    __tablename__ = 'centers'

    query_class = CustomBaseQuery

    name = db.Column(db.String(60), nullable=False)
    image = db.Column(JSON, nullable=False)
    search_vector = db.Column(TSVectorType('name'))
    assets = db.relationship(
        'Asset', backref='center', cascade='delete', lazy='dynamic')
    users = db.relationship(
        'User', backref='center', cascade='delete', lazy='dynamic')
    spaces = db.relationship(
        'Space', backref='center', cascade='delete', lazy='dynamic')

    def get_child_relationships(self):
        """
        Method to get all child relationships of this model

        Returns:
             children(tuple): children of this model
        """
        return self.assets, self.users, self.spaces

    def __repr__(self):
        return f'<Center {self.name}>'

    @CenterPolicy.delete_update_action()
    def update_(self, *args, **kwargs):
        return super(Center, self).update_(*args, **kwargs)

    @CenterPolicy.delete_update_action()
    def delete(self, *args, **kwargs):
        return super(Center, self).delete(*args, **kwargs)


Center.user_count = column_property(
    select([func.count(User.id)]).where(User.center_id == Center.id))


@listens_for(Center, 'after_update')
def after_update(mapper, connection, target):
    """Runs after a center is updated

    When the center is deleted, the deleted column will be True
    after the operation and then the request to delete on
    cloudinary will be performed

    Args:
        mapper (obj): The current model class
        connect (obj): The current database connection
        target (obj): The current model instance

    Returns:
        None
    """

    from ..tasks.cloudinary.delete_cloudinary_image import DeleteCloudinaryImage
    if target.deleted:
        DeleteCloudinaryImage.delete_cloudinary_image_handler(
            target.image['public_id'])
