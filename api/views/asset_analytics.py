"""Module for analytics report"""  # pylint: disable=F0002
import datetime
from sqlalchemy import text
from flask_restplus import Resource  # pylint: disable=E0401

from flask import request

# Local Imports
from api.utilities.swagger.collections.asset import asset_namespace
from api.utilities.swagger.constants import ASSET_ANALYTICS_REQUEST_PARAMS

# Models
from ..models import Asset

# decorators
from api.models.database import db
from ..utilities.sql_queries import sql_queries
from ..middlewares.token_required import token_required
from ..utilities.validators.analytics_validator import report_query_validator

# Utilities
from ..utilities.messages.success_messages import SUCCESS_MESSAGES
from ..utilities.constants import ASSET_REPORT_QUERIES, EXCLUDED_FIELDS, HOT_DESK_REPORT_QUERY_PARAMS
from ..utilities.verify_date_range import report_query_date_validator
from ..utilities.enums import AssigneeType, AssetStatus
from ..utilities.paginator import list_paginator
from ..utilities.enums import AssigneeType, AssetStatus, HotDeskRequestStatusEnum
from ..utilities.validators.hot_desk_report_query_validator import validate_query_param
from ..utilities.base_analytics import AnalyticsBase
from ..utilities.helpers.add_center_to_sql import add_center_to_query

# schemas
from ..schemas.stock_level import StockLevelSchema
from ..schemas.asset import AssetInflowOutflowSchema
from ..schemas.hot_desk import HotDeskRequestSchema
# Resources
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@asset_namespace.route('/analytics')
class AssetAnalyticsReportResource(Resource, AnalyticsBase):
    """Analytics report resource
    Generates report for asset flow, asset inflow, asset outflow and stock level
    """

    @token_required
    @permission_required(Resources.ASSETS)
    @report_query_validator(ASSET_REPORT_QUERIES)
    @report_query_date_validator
    @asset_namespace.doc(params=ASSET_ANALYTICS_REQUEST_PARAMS)
    def get(self, report_query, start_date, end_date):
        """Handles get request for /analytics endpoint
        Determines the report to be generated based on the query strings provided.
        Returns:
            JSON
        """
        # Maps the methods of this class that generates report to a key.
        report_mapper = {
            "assetflow": self.asset_flow,
            "assetinflow": self.asset_inflow,
            "assetoutflow": self.asset_outflow,
            "stocklevel": self.stock_level,
            "incidencereport": self.incidence_report
        }

        # Maps the query strings provided to a camelCase response to be returned
        response_mapper = {
            "assetflow": "assetFlow",
            "assetinflow": "assetInflow",
            "assetoutflow": "assetOutflow",
            "stocklevel": "stockLevel",
            "incidencereport": "incidenceReport"
        }

        asset_analytics = {
            "assetFlow": {},
            "assetInflow": {},
            "assetOutflow": {},
            "stockLevel": {},
            "incidenceReport": {}
        }

        report = report_mapper.get(report_query)
        # Response structure if the report query string is not provided
        response = {
            "status": "Success",
            "message":
            SUCCESS_MESSAGES['asset_report'].format('assets analytics'),
            "data": asset_analytics
        }

        if not report:
            query = (report_mapper, response, report, start_date, end_date,
                     response_mapper)
            return self.all_report(*query)
            # Overrides the response to be sent if the report query string is not provided
        response_key = response_mapper.get(report_query)
        report_data = report(start_date, end_date)
        return self.response_output(report_data, response_key)

    @classmethod
    def flow_types(cls, start_date, end_date, flow_method="assetinflow"):
        """Generates report for asset inflow or outflow.

        Total number of assets that came into or left the store

        Args:
            start_date (datetime): The start date value to query the database by which is passed from the Analytics class
            end_date (datetime): The end date value is to query the database by which is passed from the Analytics class
            flow_method (str): The asset flow method type which could be either assetinflow or assetoutflow

        Returns:
            (tuple): a class tuple of the asset data and meta data
        """
        condition = Asset.assignee_type == AssigneeType.store.value if flow_method == "assetinflow" else Asset.assignee_type != AssigneeType.store.value
        asset = Asset.query_().filter(
            condition, Asset.date_assigned.between(start_date, end_date))
        formatted = [data for data in AssetInflowOutflowSchema.grouped(asset)]
        data, pagination_object = list_paginator(formatted)
        return {'data': data, 'meta': pagination_object}

    def asset_flow(self, start_date, end_date):
        """Generates report for asset flow
        The data of the asset flow to be returned are:
        total number of asset inflow: Total number of assets that came to the store
        total number of asset outflow: Total number of assets that left the store
        total number of asset category requiring reconciliation: Total number of asset category requiring reconciliation

         Args:
            start_date (datetime): The start date value to query the database by which is passed from the Analytics class
            end_date (datetime): The end date value is to query the database by which is passed from the Analytics class

        Returns:
            (dict): a dictionary of assetoutflow, assetinflow and reconciliation data
        """

        # Query the DB and get the result count for asset in flow and out flow
        asset_in_flow = Asset.query_().filter(
            Asset.assignee_type == AssigneeType.store.value,
            Asset.date_assigned.between(start_date, end_date)).count()
        asset_out_flow = Asset.query_().filter(
            Asset.assignee_type != AssigneeType.store.value,
            Asset.date_assigned.between(start_date, end_date)).count()

        # Get the total number of reconcilable asset categories
        get_total_reconciliation = add_center_to_query(
            sql_queries['get_total_reconciliation'].format(
                start_date, end_date))
        result = db.engine.execute(text(get_total_reconciliation)).first()
        return {
            'data': {
                'outflow': asset_out_flow,
                'inflow': asset_in_flow,
                'reconciliation': result[0],
            }
        }

    @classmethod
    def asset_inflow(cls, start_date, end_date):
        """Generates report for asset inflow
        Total number of assets that came into the store

        Args:
            start_date (datetime): it indicates the start date for a date range
            end_date (datetime): it indicates the end date for a date range

        Returns:
             dictionary: a dictionary of the asset data and meta data
        """

        return cls.flow_types(start_date, end_date, "assetinflow")

    @classmethod
    def asset_outflow(cls, start_date, end_date):
        """Generates report for asset outflow.
        Total number of assets that left the store

        Args:
            start_date (datetime): The start date value.
            end_date (datetime): The end date value.

        Returns:
            dictionary: a dictionary of the asset data and meta data
        """
        return cls.flow_types(start_date, end_date, "assetoutflow")

    def stock_level(self, start_date, end_date):
        """Generates report for stock level

        Args:
            start_date (date): Start date
            end_date (date): End date

        Returns
            List: The stock level report

        """

        # makes a copy of the excluded fields list and append 'assets_count'
        # to it
        excludes = EXCLUDED_FIELDS.copy()
        excludes.extend(['id', 'assets_count'])

        # defining the context for the schema
        context = {'start_date': start_date, 'end_date': end_date}

        # Generates the query for all asset categories
        asset_categories_stats = text(
            add_center_to_query(sql_queries['categories_with_stats'].format(
                filter='', sort='created_at', order='desc')))
        params = {'limit': None, 'offset': None}
        records = db.engine.execute(asset_categories_stats,
                                    **params).fetchall()
        # stock level schema instance
        schema = StockLevelSchema(many=True, exclude=excludes, context=context)
        # serializes and returns the data
        return {'data': schema.dump(records).data}

    def incidence_report(self, start_date, end_date):
        """Generates report for incidence reporting

        Args:
            start_date (date): Start date
            end_date (date): End date

        Returns
            List: The report for incidence reporting
        """
        get_incidence_report = list(
            db.engine.execute(
                text(
                    add_center_to_query(sql_queries['get_incidence_report'],
                                        'requests'))))
        report_by_categories = []
        total_open, total_in_progress, total_completed, total_closed, total_overdue = \
            0, 0, 0, 0, 0
        for report in get_incidence_report:
            incidence_report = {
                'requestType': report[5],
                'openRequests': report[0],
                'inProgressRequests': report[1],
                'completedRequests': report[2],
                'closedRequests': report[3],
                'overdueRequests': report[4]
            }
            report_by_categories.append(incidence_report)
            total_open = total_open + report[0]
            total_in_progress = total_in_progress + report[1]
            total_completed = total_completed + report[2]
            total_closed = total_closed + report[3]
            total_overdue = total_overdue + report[4]
        return {
            'data': {
                'categories': report_by_categories,
                'total': {
                    'totalOpenRequests': total_open,
                    'totalInProgressRequests': total_in_progress,
                    'totalCompletedRequests': total_completed,
                    'totalClosedRequests': total_closed,
                    'totalOverdueRequests': total_overdue,
                }
            }
        }
