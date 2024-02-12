"""Module for stock count model"""

# Models
from .base.auditable_model import AuditableBaseModel

# Base query class
from .base.base_query import CustomBaseQuery
# Base Policy
from .base.base_policy import BasePolicy

# Database instance
from .database import db

# Activity Tracker
from api.utilities.history.activity_tracker import ActivityTracker
from api.utilities.history.tracker_listener import activity_tracker_listener


class StockCountPolicy(BasePolicy):
    pass


class StockCount(AuditableBaseModel):
    """Model for stock count """
    policies = {"patch": None, "delete": "owner"}
    __tablename__ = 'stock_counts'

    query_class = CustomBaseQuery

    asset_category_id = db.Column(
        db.String, db.ForeignKey('asset_categories.id'), nullable=False)
    center_id = db.Column(
        db.String, db.ForeignKey('centers.id'), nullable=False)
    token_id = db.Column(
        db.String, db.ForeignKey('users.token_id'), nullable=False)
    user = db.relationship('User')
    week = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, nullable=False)

    def get_child_relationships(self):
        """
        Method to get all child relationships a model has. Overide in the
        subclass if the model has child models.

        """
        return None

    def __repr__(self):
        return '<StockCount asset_category_id:{} count:{} week:{} >'.format(
            self.asset_category_id, self.count, self.week)

    @StockCountPolicy.delete_update_action()
    def update_(self, *args, **kwargs):
        return super(StockCount, self).update_(*args, **kwargs)

    @StockCountPolicy.delete_update_action()
    def delete(self, *args, **kwargs):
        return super(StockCount, self).delete(*args, **kwargs)


# listens for activities on this model
activity_tracker_listener(StockCount, ActivityTracker)
