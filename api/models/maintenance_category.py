"""Module that holds maintenance category model class."""

# Auditable Base Model
from .base.auditable_model import AuditableBaseModel

# Base query class
from .base.base_query import CustomBaseQuery
# Base Policy
from .base.base_policy import BasePolicy

# Models
from api.models.work_order import WorkOrder

# Database
from .database import db

from api.utilities.history.activity_tracker import ActivityTracker
from api.utilities.history.tracker_listener import activity_tracker_listener


class MaintenanceCategoryPolicy(BasePolicy):
    pass


class MaintenanceCategory(AuditableBaseModel):
    """Model for maintenance category """

    policies = {'patch': 'owner', 'delete': 'owner'}

    __tablename__ = 'maintenance_categories'

    query_class = CustomBaseQuery

    title = db.Column(db.String(60), nullable=False)
    asset_category_id = db.Column(
        db.String, db.ForeignKey('asset_categories.id'), nullable=False)
    center_id = db.Column(
        db.String, db.ForeignKey('centers.id'), nullable=False)
    asset_category = db.relationship(
        'AssetCategory', backref='maintenance_categories')
    center = db.relationship('Center', backref='maintenance_categories')
    work_orders = db.relationship(
        'WorkOrder',
        backref='maintenance_categories',
        cascade='save-update, delete',
        lazy='dynamic',
        primaryjoin=
        "and_(WorkOrder.maintenance_category_id == MaintenanceCategory.id, WorkOrder.deleted == False)"
    )

    def get_child_relationships(self):
        """Method to get all child relationships of a model

        Overrides the subclass if the model has child models.
        """
        return (self.work_orders, )

    def __repr__(self):
        """Shows a string representation of the model

        Returns:
            (str): string representation of a work order type
        """
        return f'<MaintenanceCategory {self.title}>'

    @MaintenanceCategoryPolicy.delete_update_action()
    def update_(self, *args, **kwargs):
        return super(MaintenanceCategory, self).update_(*args, **kwargs)

    @MaintenanceCategoryPolicy.delete_update_action()
    def delete(self, *args, **kwargs):
        return super(MaintenanceCategory, self).delete(*args, **kwargs)

    @property
    def work_order_count(self):
        return self.work_orders.count()


activity_tracker_listener(MaintenanceCategory, ActivityTracker)
