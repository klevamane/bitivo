from .asset_category import AssetCategoryStats
from api.views.asset_category import AssetCategoryResource, AssetSubcategoryResource
from .asset_category_attributes import AssetCategoryAttributes
from .asset import AssetResource
from .asset_bulk import AssetBulkResource
from .asset_category_csv import ExportAssetCategories
from .asset_csv import ExportAssets
from .center import CenterResource
from .user import UserResource
from .user import AddUserResource
from .role import RoleResource
from .permission import PermissionResource
from .space import SpaceResource
from .space import SingleSpaceResource
from .user_csv import ExportUserResource
from .asset_analytics import AssetAnalyticsReportResource
from .stock_count_csv import ExportStockCountResource
from .stock_count import StockCountResource
from .history import HistoryResource
from .asset_analytics_csv import ExportAssetAnalyticsReportResource
from .request_type import RequestTypeResource, SingleRequestTypeResource
from .request import SingleRequestResource, UserRequestResource
from .request import RequestResource
from .comment import CommentResource, RequestCommentsResource, SingleCommentResource
from .work_order import WorkOrderResource, SingleWorkOrderResource
from .sheet_transformer import SheetTransformerResource
from .schedule import SingleScheduleResource, ScheduleResource
from .maintenance_category import SingleMaintenanceCategoryResource, MaintenanceCategoryResource
from .hot_desk_analytics_csv import ExportHotDeskAnalyticsReportResource
from .hot_desk_analytics import HotDesksAnalyticsReportResource
from .request import OverdueRequestResource
from .hot_desk_resource import HotDesksResource
from .hot_desk_activity_log import SpecificUserActivityLogResource
from .hot_desk import SingleHotDeskRequest
from .hot_desk_activities import CancelHotDeskRequestResource
from .hot_desk_resource import HotDeskComplaintsResource
from .hot_desk import CancelledHotDeskResource
from .asset_repair_log import AssetRepairLogResource, SingleRepairLogResource
from .asset_note import SingleNoteResource, AssetNoteResource
from .asset_warranty import AssetWarrantyResource
from .asset_supporting_document import DeleteAssetSupportingDocumentResource, AssetSupportingDocumentResource
from .asset_insurance import AssetInsuranceResource, SingleAssetInsuranceResource
from .global_search import SearchResource
