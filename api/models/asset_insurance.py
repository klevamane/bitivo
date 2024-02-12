"""Module that holds asset insurance model class."""

# Activity Tracker
from api.utilities.history.activity_tracker import ActivityTracker
from api.utilities.history.tracker_listener import activity_tracker_listener

# Database
from .database import db

# Auditable Base Model
from .base.auditable_model import AuditableBaseModel
# Base Policy
from .base.base_policy import BasePolicy

# Base query class
from .base.base_query import CustomBaseQuery


class AssetInsurancePolicy(BasePolicy):
    pass


class AssetInsurance(AuditableBaseModel):
    """
    Model for asset insurance
    """
    policies = {'patch': 'owner', 'delete': 'owner'}

    __tablename__ = 'asset_insurances'

    query_class = CustomBaseQuery

    company = db.Column(db.String(250), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    asset_id = db.Column(db.String, db.ForeignKey("asset.id"), nullable=False)
    asset = db.relationship('Asset')

    def get_child_relationships(self):
        """Method to get all child relationships of a model
         Override in the subclass if the model has child models.
        """
        return None

    @AssetInsurancePolicy.delete_update_action()
    def update_(self, *args, **kwargs):
        return super(AssetInsurance, self).update_(*args, **kwargs)

    @AssetInsurancePolicy.delete_update_action()
    def delete(self, *args, **kwargs):
        return super(AssetInsurance, self).delete(*args, **kwargs)

    def __repr__(self):
        """ Shows a string representation of the model

        Returns:
            String: string representation of a request type
        """
        start_date = self.start_date.strftime("%Y-%m-%d")
        end_date = self.end_date.strftime("%Y-%m-%d")
        return f'<AssetInsurance {self.company} ({start_date} - {end_date})>'


# listens for activities on this model
activity_tracker_listener(AssetInsurance, ActivityTracker)
