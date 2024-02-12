"""Module for SupportDocument model"""

from .base.auditable_model import AuditableBaseModel
from .database import db
from ..utilities.enums import AssetSupportingDocumentTypeEnum
from sqlalchemy.event import listens_for
# Base Policy
from .base.base_policy import BasePolicy
# Base query class
from .base.base_query import CustomBaseQuery


class AssetSupportingDocumentPolicy(BasePolicy):
    pass


class AssetSupportingDocument(AuditableBaseModel):
    """
    Model for support_documents
    """

    policies = {'patch': 'owner', 'delete': 'owner'}

    __tablename__ = 'asset_supporting_documents'

    query_class = CustomBaseQuery

    document_name = db.Column(db.String(60), nullable=False)
    document_type = db.Column(
        db.Enum(AssetSupportingDocumentTypeEnum),
        nullable=False,
        default='purchase receipts',
        name='document_type')
    asset_id = db.Column(
        db.String(60), db.ForeignKey('asset.id'), nullable=True)
    document = db.Column(db.JSON(), nullable=True)

    def get_child_relationships(self):
        """
        Method to get all child relationships of this model

        Returns:
             children(tuple): children of this model
        """
        return None

    def __repr__(self):
        return f'<AssetSupportingDocument: {self.document_name}>'

    @AssetSupportingDocumentPolicy.delete_update_action()
    def update_(self, *args, **kwargs):
        return super(AssetSupportingDocument, self).update_(*args, **kwargs)

    @AssetSupportingDocumentPolicy.delete_update_action()
    def delete(self, *args, **kwargs):
        return super(AssetSupportingDocument, self).delete(*args, **kwargs)


@listens_for(AssetSupportingDocument, 'after_update')
def after_update(mapper, connection, target):
    """Runs after a supporting document is updated

    When the supporting document is deleted, the deleted column will be True
    after the operation and then the request to delete on
    cloudinary will be performed

    Args:
        mapper (obj): The current model class
        connection (obj): The current database connection
        target (obj): The current model instance

    Returns:
        None
    """

    from ..tasks.cloudinary.delete_cloudinary_image import DeleteCloudinaryImage
    if target.deleted:
        DeleteCloudinaryImage.delete_cloudinary_image(
            target.document['public_id'])
