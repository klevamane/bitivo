from .base.auditable_model import AuditableBaseModel

# Base query class
from .base.base_query import CustomBaseQuery

from .database import db


class Attribute(AuditableBaseModel):
    """
    Model for attributes
    """

    query_class = CustomBaseQuery

    _key = db.Column(db.String(60), nullable=False)
    label = db.Column(db.String(60), nullable=False)
    is_required = db.Column(db.Boolean, nullable=False)
    input_control = db.Column(db.String(60), nullable=False)
    choices = db.Column(db.String(250), nullable=True)
    asset_category_id = db.Column(
        db.String, db.ForeignKey('asset_categories.id'), nullable=False)
    default = db.Column(db.Boolean, nullable=True, default=False)

    def get_child_relationships(self):
        """
        Method to get all child relationships a model has. Overide in the
        subclass if the model has child models.
        """
        return None

    def __repr__(self):
        return '<Attribute {}>'.format(self.label)
