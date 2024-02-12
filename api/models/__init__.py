# Third Party Libraries
from sqlalchemy import event

# Models
from .asset_repair_log import AssetRepairLog
from .user import User
from .asset import Asset
from .asset_category import AssetCategory
from .center import Center
from .role import Role
from .permission import Permission
from .space import Space
from .space_type import SpaceType
from .resource import Resource
from .resource_access_level import ResourceAccessLevel
from .stock_count import StockCount
from .history import History
from .request_type import RequestType
from .request import Request
from .comment import Comment
from .work_order import WorkOrder
from .schedule import Schedule
from .maintenance_category import MaintenanceCategory
from .hot_desk import HotDeskRequest
from .hot_desk_response import HotDeskResponse
from .asset_supporting_document import AssetSupportingDocument
from .asset_note import AssetNote
from .asset_insurance import AssetInsurance
from .asset_warranty import AssetWarranty

# Model helpers
from .attribute import Attribute
from .push_id import PushID

# Services
import api.services.email_notification
import api.services.request
import api.services.schedule_notification


def fancy_id_generator(mapper, connection, target):
    """A function to generate unique identifiers on insert."""
    push_id = PushID()
    target.id = push_id.next_id()


# associate the listener function with models, to execute during the
# "before_insert" event
tables = [
    Asset, AssetCategory, Attribute, Center, User, Role, Permission, Space,
    SpaceType, Resource, ResourceAccessLevel, StockCount, History, RequestType,
    Request, Comment, WorkOrder, Schedule, MaintenanceCategory, HotDeskRequest,
    HotDeskResponse, AssetRepairLog, AssetSupportingDocument, AssetNote, AssetInsurance, AssetWarranty
]

for table in tables:
    event.listen(table, 'before_insert', fancy_id_generator)
