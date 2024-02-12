# Third Party
from sqlalchemy.event import listens_for
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy_utils.types import TSVectorType

# Models
from .asset import Asset
from .base.auditable_model import AuditableBaseModel

# Base query class
from .base.base_query import CustomBaseQuery
# Base Policy
from .base.base_policy import BasePolicy

# Database
from .database import db

# Enums
from ..utilities.enums import RepairLogStatusEnum, AssetStatus

# Utilities
from api.utilities.history.asset_status_activity import asset_status_activity_on_repair_log


class AssetRepairLogPolicy(BasePolicy):
    pass


class AssetRepairLog(AuditableBaseModel):
    """
    Model for Asset Repair Log
    """

    policies = {'patch': 'owner', 'delete': 'owner'}

    __tablename__ = 'asset_repair_logs'

    query_class = CustomBaseQuery

    repairer = db.Column(db.String, nullable=True)
    asset_id = db.Column(db.String, db.ForeignKey('asset.id'), nullable=False)
    issue_description = db.Column(db.Text, nullable=False)
    date_reported = db.Column(db.DateTime, nullable=True)
    expected_return_date = db.Column(db.DateTime, nullable=False)
    defect_type = db.Column(db.String, nullable=True)
    search_vector = db.Column(TSVectorType('issue_description'))
    status = db.Column(
        db.Enum(RepairLogStatusEnum),
        default=RepairLogStatusEnum.open.value,
        nullable=False,
    )

    asset = db.relationship(
        'Asset',
        backref='asset',
        primaryjoin=
        "and_(AssetRepairLog.asset_id == Asset.id, Asset.deleted == False)")

    def get_child_relationships(self):
        """
        Method to get all child relationships of this model

        Returns:
             children(tuple): children of this model
        """
        return None

    def __repr__(self):
        return f'<AssetRepairLog {self.id} {self.issue_description}>'

    @AssetRepairLogPolicy.delete_update_action()
    def update_(self, *args, **kwargs):
        return super(AssetRepairLog, self).update_(*args, **kwargs)

    @AssetRepairLogPolicy.delete_update_action()
    def delete(self, *args, **kwargs):
        return super(AssetRepairLog, self).delete(*args, **kwargs)


@listens_for(AssetRepairLog, "after_insert")
def after_insert(mapper, connect, target):
    """
    Will handle updating the asset status
    after a repair log has been created
    Args:
        mapper (obj): The current model class
        connect (obj): The current database connection
        target (obj): The current model instance
    Returns:
        None
    """

    @listens_for(Session, 'after_flush', once=True)
    def update_the_asset_status(session, context):
        """ will update the asset status
        args:
            session(obj): The current database session
            context(obj): Handles the details of the flush
        returns:
            None
        """

        prev_status = Asset.get(target.asset_id).status
        asset = Asset.__table__
        session.execute(asset.update().where(
            and_(asset.c.id == target.asset_id)).values(
                status=AssetStatus.IN_REPAIRS.value))
        asset_status_activity_on_repair_log\
            (target.asset_id, prev_status, session)
