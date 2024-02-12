"""Module for asset note model"""
# Database
from .database import db

# Auditable Base Model
from .base.auditable_model import AuditableBaseModel

# Base query class
from .base.base_query import CustomBaseQuery
# Base Policy
from .base.base_policy import BasePolicy


class AssetNotePolicy(BasePolicy):
    pass


class AssetNote(AuditableBaseModel):
    """
    Model for asset note
    """
    policies = {'patch': 'owner', 'delete': 'owner'}

    __tablename__ = 'asset_notes'

    query_class = CustomBaseQuery

    title = db.Column(db.String, nullable=False)
    body = db.Column(db.Text, nullable=False)
    asset_id = db.Column(db.String, db.ForeignKey('asset.id'))
    asset = db.relationship('Asset')

    def get_child_relationships(self):
        """Method to get all child relationships of this model"""
        return None

    @AssetNotePolicy.delete_update_action()
    def update_(self, *args, **kwargs):
        return super(AssetNote, self).update_(*args, **kwargs)

    @AssetNotePolicy.delete_update_action()
    def delete(self, *args, **kwargs):
        return super(AssetNote, self).delete(*args, **kwargs)

    def __repr__(self):
        return '<AssetNote {}>'.format(self.title)
