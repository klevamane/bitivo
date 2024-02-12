"""Module for export analytics report as csv format"""

# Library Imports
import flask_excel as excel
from flask_restplus import Resource
from sqlalchemy import text

# Local Imports
from api.utilities.swagger.collections.asset import asset_namespace
from api.utilities.swagger.constants import ANALYTICS_REQUEST_PARAMS

# database
from api.models.database import db

from ..middlewares.token_required import token_required
from ..utilities.validators.analytics_validator import report_query_validator
from ..schemas.asset import AssetInflowAnalyticsSchema
from ..utilities.constants import ASSET_REPORT_QUERIES
from ..utilities.enums import AssigneeType
from ..utilities.verify_date_range import report_query_date_validator
from ..utilities.sql_queries import sql_queries

# Model
from ..models import Asset, AssetCategory
# Schema
from ..schemas.export_stock_level import ExportStockLevelSchema
# Resources
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@asset_namespace.route('/analytics/export')
class ExportAssetAnalyticsReportResource(Resource):
    """Resource class for exporting analytics in csv format"""

    @token_required
    @permission_required(Resources.ASSETS)
    @report_query_validator(ASSET_REPORT_QUERIES)
    @report_query_date_validator
    @asset_namespace.doc(params=ANALYTICS_REQUEST_PARAMS)
    def get(self, report_query, start_date, end_date):
        """Handles get request for /assets/analytics/export endpoint

        Args:
            report_query (str): The value of the report parameter in the request.
            start_date (datetime): The start date value.
            end_date (datetime): The end date value.

        Returns:
            csv: The return value from any of the methods handling
                  the corresponding report parameter value
        """

        # Maps the methods of this class that generates report in csv to a key
        report_mapper = {
            "assetflow": self.asset_flow,
            "assetinflow": self.asset_inflow,
            "assetoutflow": self.asset_outflow,
            "stocklevel": self.stock_level,
        }

        report = report_mapper.get(report_query)

        # records when no report query is provided
        if not report:
            records = [{'to_be_implemented': "Endpoint yet to be implemented"}]

        # executes the method to return the records for the csv file
        else:
            records = report(start_date, end_date)

        # makes a csv response from the records
        return excel.make_response_from_records(records, 'csv')

    def asset_inflow(self, start_date, end_date):
        """Handles asset inflow

          Args:
            self (obj): The instance object.
            start_date (datetime): The start date value.
            end_date (datetime): The end date value.

         Returns:
             list: a list of records (dict)
        """

        only = [
            'tag', 'category', 'store', 'center', 'assigned_by',
            'date_assigned'
        ]

        asset_inflow_data = self.get_records(
            Asset, AssetInflowAnalyticsSchema, start_date, end_date,
            Asset.assignee_type == AssigneeType.store, only)
        return asset_inflow_data

    def asset_outflow(self, start_date, end_date):
        """Handles asset outflow

         Args:
            self (obj): The instance object.
            start_date (datetime): The start date value.
            end_date (datetime): The end date value.

         Returns:
             list: a list of records (dict)
        """

        only = [
            'tag', 'category', 'assignee', 'center', 'assigned_by',
            'date_assigned'
        ]

        asset_outflow_data = self.get_records(
            Asset, AssetInflowAnalyticsSchema, start_date, end_date,
            Asset.assignee_type != AssigneeType.store, only)

        return asset_outflow_data

    def asset_flow(self, start_date, end_date):
        """Handles flow of asset

         Args:
            self (obj): The instance object.
            start_date (datetime): The start date value.
            end_date (datetime): The end date value.

         Returns:
             list: a list of records (dict)
         """
        asset_flow_query = sql_queries['get_asset_flow_count'].format(
            start_date, end_date)
        reconciliation_query = sql_queries['get_total_reconciliation'].format(
            start_date, end_date)

        # execute the query and get back sqlalchemy result proxy object
        asset_flow_proxy = db.engine.execute(text(asset_flow_query))
        asset_flow_result = list(asset_flow_proxy)[0]

        # execute the query and get back sqlalchemy result proxy object
        reconciliation = db.engine.execute(
            text(reconciliation_query)).first()[0]

        asset_flows = [{
            'Asset Inflow':
            asset_flow_result[0],
            'Asset Outflow':
            asset_flow_result[1],
            'Asset category requiring reconciliation':
            reconciliation
        }]
        return asset_flows

    def stock_level(self, start_date, end_date):
        """Handles stock level of asset

         Args:
            self (obj): The instance object.
            start_date (datetime): The start date value.
            end_date (datetime): The end date value.

         Returns:
             list: a list of records (dict)
         """

        stock_level = self.get_stock_level_records(
            AssetCategory, ExportStockLevelSchema, start_date, end_date)
        return stock_level

    def get_records(self, *args):
        """Helper method to return data csv data

        Args:
            model (class): The model.
            schema (class): The schema to serialize data
            end_date (datetime): The end date value.

         Returns:
             list: a list of records (dict)
        """

        model, schema, start_date, end_date, query_filter, only = args

        records = model.query.filter_by() \
            .filter(query_filter) \
            .filter(Asset.date_assigned.between(start_date, end_date)).order_by(Asset.date_assigned.desc()).all()

        records_data = schema(many=True, only=only) \
            .dump(records).data

        return records_data

    def get_stock_level_records(self, model, schema, start_date, end_date):
        """Helper method to return csv data.

         Args:
            model (class): The model.
            schema (class): The schema to serialize data
            start_date (datetime): The start date value.
            end_date (datetime): The end date value.

          Returns:
             list: a list of records (dict)
        """
        records = model.query_().all()
        only = ['name', 'stock_count', 'running_low', 'low_in_stock']
        context = {'start_date': start_date, 'end_date': end_date}
        records_data = schema(many=True, only=only, context=context)\
            .dump(records).data
        return records_data
