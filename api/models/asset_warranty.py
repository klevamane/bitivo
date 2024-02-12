"""Module for asset warranty model"""
# system imports
from datetime import datetime

# Database
from .database import db

# Auditable Base Model
from .base.auditable_model import AuditableBaseModel
# Base Policy
from .base.base_policy import BasePolicy

# Enum
from ..utilities.enums import AssetWarrantyStatusEnum


class AssetWarrantyPolicy(BasePolicy):
    pass


class AssetWarranty(AuditableBaseModel):
    """
    Model for asset warranty
    """
    policies = {'patch': 'owner', 'delete': 'owner'}

    __tablename__ = 'asset_warranties'

    status = db.Column(
        db.Enum(AssetWarrantyStatusEnum),
        default=AssetWarrantyStatusEnum.active.value,
        nullable=False,
    )
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    asset_id = db.Column(db.String, db.ForeignKey('asset.id'))
    asset = db.relationship('Asset')

    def get_child_relationships(self):
        """Method to get all child relationships of this model"""
        return None

    def __repr__(self):
        return '<AssetWarranty {}>'.format(self.status)

    @AssetWarrantyPolicy.delete_update_action()
    def update_(self, *args, **kwargs):
        return super(AssetWarranty, self).update_(*args, **kwargs)

    @AssetWarrantyPolicy.delete_update_action()
    def delete(self, *args, **kwargs):
        return super(AssetWarranty, self).delete(*args, **kwargs)
