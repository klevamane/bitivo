"""Module that holds asset model class"""

# Standard library
import enum
import datetime as dt

# Flask
from flask import request
# Base Policy
from .base.base_policy import BasePolicy
from ..utilities.enums import AssigneeType

# Third party libraries
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.event import listens_for
from sqlalchemy.orm import validates
from sqlalchemy_utils.types import TSVectorType

# Database
from .database import db

# Auditable base model
from .base.auditable_model import AuditableBaseModel

# Base query class
from .base.base_query import CustomBaseQuery

# Activity Tracker
from api.utilities.history.asset_activity_tracker import AssetActivityTracker
from api.utilities.history.tracker_listener import activity_tracker_listener

# Validators
from ..utilities.validators.asset_status_validator import validate_asset_status

# Enum
from ..utilities.enums import AssigneeType


class AssetPolicy(BasePolicy):
    pass


class Asset(AuditableBaseModel):
    """
    Model for assets
    """

    query_class = CustomBaseQuery
    policies = {'patch': 'owner', 'delete': 'owner'}

    tag = db.Column(db.String(60), nullable=False, unique=True)
    custom_attributes = db.Column(JSON, nullable=True)
    asset_category_id = db.Column(
        db.String, db.ForeignKey('asset_categories.id'), nullable=False)
    center_id = db.Column(db.String, db.ForeignKey('centers.id'))
    assignee_type = db.Column(
        db.Enum(AssigneeType),
        nullable=False,
        server_default='space',
        name='assignee_type')
    assignee_id = db.Column(db.String(60))
    assigned_by = db.Column(db.String(60), nullable=True)
    date_assigned = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(60), nullable=False, server_default='ok')
    search_vector = db.Column(TSVectorType('tag'))

    def get_child_relationships(self):
        """
        Method to get all child relationships a model has. Override in the
        subclass if the model has child models.
        """
        return None

    @property
    def assignee(self):
        """Property method to return the asset's assignee
        Returns:
            assignee (obj): The asset's assignee. Can be either a user or a
            space
        """
        from . import User, Space
        assignee_mapper = {'user': User, 'space': Space, 'store': Space}
        assignee = assignee_mapper[self.assignee_type.value].get(
            self.assignee_id)
        return assignee

    def __repr__(self):
        return '<Asset {}>'.format(self.tag)

    @AssetPolicy.delete_update_action()
    def update_(self, *args, **kwargs):
        return super(Asset, self).update_(*args, **kwargs)

    @AssetPolicy.delete_update_action()
    def delete(self, *args, **kwargs):
        return super(Asset, self).delete(*args, **kwargs)

    @validates('status')
    def validate_status(self, key, status):
        """Check that the supplied status is one of the accepted types
        Args:
            self (Asset): Instance of an Asset record
            status (string): The status field to validate
        Raises:
            ValidationError: When the status supplied is not a valid status
        Returns:
            func: Validates status field and return lowercase or throw error
        """
        return validate_asset_status(status)


# listens for activities on this model
activity_tracker_listener(Asset, AssetActivityTracker)


@listens_for(Asset, 'before_insert')
def before_insert(mapper, connect, target):
    """Gets the asset's assignee
    Gets the asset's assignee object before the asset is inserted into the
    database and saves it in the assignee field.
    Args:
        mapper (obj): The current model class
        connect (obj): The current database connection
        target (obj): The current model instance
    Raises:
        Exception: If assignee object is not found
    """
    from . import User, Space

    assignee_mapper = {'user': User, 'space': Space, 'store': Space}
    assignee = assignee_mapper[target.assignee_type].get(target.assignee_id)
    if not assignee:
        raise Exception('Assignee object not found')
    if isinstance(assignee, Space) and assignee.space_type.type == 'Store':
        target.assignee_type = AssigneeType.store.value
    if request and request.decoded_token:
        target.assigned_by = request.decoded_token['UserInfo']['name']


@listens_for(Asset, 'before_update')
def before_update(mapper, connect, target):
    """Updates assigned_by and date_assigned columns
    Checks whether the assignee id has changed. If it has, the date assigned
    is updated and the name of the user performing the operation is saved in
    the assigned_by column
    Args:
        mapper (obj): The current mapper class
        connect (obj): The current database connection
        target (obj): The current model instance
    """
    hist = db.inspect(target).attrs.assignee_id.history
    if hist.has_changes():
        if request and request.decoded_token:
            target.assigned_by = request.decoded_token['UserInfo']['name']
            target.date_assigned = dt.datetime.utcnow()
