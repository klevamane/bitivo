# Third Party
from sqlalchemy.orm import column_property
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import select, func
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy.event import listens_for

# Database
from .database import db

# Models
from . import Asset
from .base.auditable_model import AuditableBaseModel

# Base query class
from .base.base_query import CustomBaseQuery
# Base Policy
from .base.base_policy import BasePolicy
from api.utilities.enums import Priority


class AssetCategoryPolicy(BasePolicy):
    pass


class AssetCategory(AuditableBaseModel):
    """
    Model for asset categories
    """
    policies = {'patch': 'owner', 'delete': 'owner'}

    __tablename__ = 'asset_categories'

    query_class = CustomBaseQuery

    name = db.Column(db.String(60), nullable=False, unique=False)
    description = db.Column(db.Text, nullable=True)
    parent_id = db.Column(
        db.String(60), db.ForeignKey('asset_categories.id'), nullable=True)
    image = db.Column(JSON, nullable=True)
    running_low = db.Column(db.Integer, nullable=False, server_default="0")
    low_in_stock = db.Column(db.Integer, nullable=False, server_default="0")
    search_vector = db.Column(TSVectorType('name'))
    assets = db.relationship(
        'Asset',
        backref='asset_category',
        cascade='save-update, delete',
        lazy='dynamic')
        
    attributes = db.relationship(
        'Attribute',
        backref='asset_category',
        cascade='save-update, delete',
        lazy='dynamic')
    eager_loaded_attributes = db.relationship(
        'Attribute', lazy='joined', viewonly=True)
    stock_counts = db.relationship(
        'StockCount',
        backref='asset_category',
        cascade='save-update, delete',
        lazy='dynamic')
    priority = db.Column(
        db.Enum(Priority),
        nullable=True,
        server_default='key',
        name='priority')
    children = db.relationship('AssetCategory', lazy='joined')
    children_reference = db.relationship('AssetCategory', lazy='dynamic')

    def get_child_relationships(self):
        return (self.assets, )

    def child_count(self):
        return len(
            [child for child in self.children if child.deleted == False])

    def __repr__(self):
        return '<AssetCategory {}>'.format(self.name)

    @AssetCategoryPolicy.delete_update_action()
    def update_(self, *args, **kwargs):
        return super(AssetCategory, self).update_(*args, **kwargs)

    @AssetCategoryPolicy.delete_update_action()
    def delete(self, *args, **kwargs):
        return super(AssetCategory, self).delete(*args, **kwargs)


AssetCategory.assets_count = column_property(
    select([func.count(
        Asset.id)]).where(Asset.asset_category_id == AssetCategory.id).where(
            Asset.deleted == False))


@listens_for(AssetCategory, 'after_update')
def after_update(mapper, connection, target):
    """Runs after an Asset Category is updated
    When an Asset Category is deleted, the deleted column will be True
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
        if target.image:
            DeleteCloudinaryImage.delete_cloudinary_image.delay(
                target.image.get('public_id'))
