"""Module for User model."""
# System imports
import enum

# Third-party libraries
from sqlalchemy.event import listens_for
from sqlalchemy.orm import attributes
from sqlalchemy.sql import select
from sqlalchemy_utils.types import TSVectorType

# Models
from api.models.role import Role
from api.models.base.auditable_model import AuditableBaseModel

# Base query class
from .base.base_query import CustomBaseQuery

# Base Policy
from .base.base_policy import BasePolicy

#middlewares
from ..middlewares.base_validator import ValidationError

# Database
from api.utilities.server_events import publish
from .database import db


class Status(enum.Enum):
    disabled = 'disabled'
    enabled = 'enabled'


class UserPolicy(BasePolicy):
    pass


class User(AuditableBaseModel):
    """Class for user db table."""

    policies = {'patch': None, 'delete': 'owner'}

    __tablename__ = 'users'

    query_class = CustomBaseQuery

    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    image_url = db.Column(db.String)
    center_id = db.Column(db.String, db.ForeignKey('centers.id'))
    role_id = db.Column(
        db.String,
        db.ForeignKey('roles.id'),
        nullable=False,
        default=select([Role.__table__.c.id
                        ]).where(Role.__table__.c.title == 'Regular User'))
    status = db.Column(db.Enum(Status), nullable=False, default='enabled')
    token_id = db.Column(db.String(60), nullable=False, unique=True)
    search_vector = db.Column(TSVectorType('name', 'email'))

    def get_child_relationships(self):
        """
        Method to get all child relationships a model has. Overide in the
        subclass if the model has child models.
        """
        return None

    @UserPolicy.delete_update_action()
    def update_(self, *args, **kwargs):
        return super(User, self).update_(*args, **kwargs)

    @UserPolicy.delete_update_action()
    def delete(self, *args, **kwargs):
        return super(User, self).delete(*args, **kwargs)

    @classmethod
    def get_or_404(cls, id):
        """Return the user with token_id = id
        Args:
            cls (class): The user model class
            id (string): token_id of the user
        Returns:
            user (object): the user object which has token_id = id
        """
        user = User.query.filter_by(token_id=id, deleted=False).first()
        if not user:
            raise ValidationError({'message': f'{cls.__name__ } not found'},
                                  404)
        return user

    def get(id):
        """
        return entries by id
        """
        return User.query.filter_by(token_id=id).first()

    def __repr__(self):
        return f'<User {self.name}>'


@listens_for(User, 'after_update')
def after_update(mapper, connect, target):
    """Event handler on after insert.

        Args:
            mapper (obj): The current model class
            connect (obj): The current database connection
            target (obj): The current model instance

        """
    # handle sending of events to client when status or role_id field is updated in the db.
    token_id = target.token_id
    previous_status = attributes.get_history(target, 'status')[2]
    previous_role_id = attributes.get_history(target, 'role_id')[2]

    if previous_status:
        current_status = target.status
        publish({
            'tokenId': token_id,
            'status': current_status
        }, 'changed_status')

    if previous_role_id:
        current_role_id = target.role_id
        publish({
            'tokenId': token_id,
            'roleId': current_role_id
        }, 'changed_permission')
