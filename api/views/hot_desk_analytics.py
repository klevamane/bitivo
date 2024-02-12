"""Module for hot desk analytics report"""
from sqlalchemy import text
from flask_restplus import Resource  # pylint: disable=E0401
from flask import request

from main import api
from api.models import HotDeskRequest, User
from api.schemas.hot_desk import HotDeskRequestSchema
from api.schemas.user import UserSchema

# bot imports
from bot.utilities.google_sheets.google_sheets_helper import GoogleSheetHelper

# decorators
from api.models.database import db
from ..utilities.sql_queries import sql_queries
from ..utilities.validators.validate_id import validate_id
from ..middlewares.token_required import token_required
from ..utilities.validators.analytics_validator import report_query_validator
from ..utilities.messages.success_messages import SUCCESS_MESSAGES
from ..utilities.validators.validate_json_request import validate_json_request, validate_reason
from ..utilities.validators.analytics_validator import hot_desk_query_validator

# Utilities
from api.utilities.swagger.collections.hot_desk import hot_desk_namespace
from api.utilities.swagger.constants import (ANALYTICS_REQUEST_PARAMS,
                                             HOTDESK_ANALYTICS_REQUEST_PARAMS,
                                             PAGINATION_PARAMS)
from api.utilities.helpers.endpoint_response import get_success_responses_for_post_and_patch
from ..utilities.constants import (
    EXCLUDED_FIELDS, HOT_DESK_REPORT_QUERY_PARAMS, HOT_DESK_QUERY_KEYS)
from ..utilities.verify_date_range import report_query_date_validator
from ..utilities.helpers.trends_allocations import trends_allocations_helper
from ..utilities.constants import USER_SCHEMA_FIELDS

from ..utilities.validators.hot_desk_report_query_validator import validate_query_param
from ..utilities.base_analytics import AnalyticsBase
from ..utilities.error import raises
from ..utilities.helpers.trends_allocations import weekly_trends, monthly_trends, yearly_trends, \
    quarterly_trends, daily_trends
from ..utilities.paginator import list_paginator, get_pagination_option

# schemas
from ..schemas.hot_desk import (
    HotDeskRequestSchema, CancelHotDeskRequestSchema, HotDeskComplaintSchema)
from bot.utilities.user_hot_desk import cancel_hot_desk_by_id
from api.utilities.enums import HotDeskRequestStatusEnum
from api.utilities.helpers.hot_desk import get_hotdesk_of_specific_user_by_requester_id

# Models
from ..models.user import User
from ..models.hot_desk import HotDeskRequest

# enum
from api.utilities.enums import HotDeskRequestStatusEnum
# Resources
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@hot_desk_namespace.route('/analytics')
class HotDesksAnalyticsReportResource(Resource, AnalyticsBase):
    """Resource class for analytics on hot desks"""

    @token_required
    @permission_required(Resources.HOT_DESKS)
    @report_query_validator(HOT_DESK_REPORT_QUERY_PARAMS)
    @report_query_date_validator
    @hot_desk_namespace.doc(params=HOTDESK_ANALYTICS_REQUEST_PARAMS)
    def get(self, report_query, start_date, end_date):
        """Handles GET request for hot desks and returns response based
        on the query parameter supplied.
        """
        validate_query_param(request, HOT_DESK_QUERY_KEYS)
        reports = {
            "approvedrequests": self.approved_requests,
            "currentallocations": self.get_current_report,
            "trendsallocations": self.trends_allocations,
        }

        responses = {
            "approvedrequests": "approvedRequests",
            "currentallocations": "currentAllocations",
            "trendsallocations": "trendsAllocations",
        }

        hot_desk_analytics = {
            "approvedRequests": {},
            "currentAllocations": {},
            "trendsAllocations": {},
        }

        report = reports.get(report_query)

        response = {
            'status':
            'Success',
            'data':
            hot_desk_analytics,
            'message':
            SUCCESS_MESSAGES['asset_report'].format('Hot desks analytics'),
        }
        if report:
            response = responses.get(report_query)
            data = report(start_date, end_date)
            return self.response_output(data, response)
        query = (reports, response, report, start_date, end_date, responses)
        return self.all_report(*query)

    def approved_requests(self, start_date, end_date):
        """Gets hot desk allocations of different users

        Args:
            report_query (string): query parameter for report. Defaults to approved
            start_date (date): Start date. Defaults to 7 days difference from the end_date
            end_date (date): End date. Defaults to the current date

        Returns:
            dictionary: a dictionary of the hot-desk allocation data and meta data

        """
        approved_hot_desk_requests = sql_queries[
            'get_hot_desks_of_users'].format('approved', start_date, end_date)
        data = db.engine.execute(text(approved_hot_desk_requests)).fetchall()
        schema = HotDeskRequestSchema(many=True, exclude=EXCLUDED_FIELDS)
        data, meta = list_paginator(schema.dump(data).data)
        return {'data': data, 'meta': meta}

    def get_current_report(self, start_date, end_date):
        """ This function will map report values
        Args:
            report_id(string): Value of args params
        returns:
            response(flask response): response of report
        """
        hot_desks_numbers = self.get_hot_desk_report()
        response = {
            "data": {
                "available": hot_desks_numbers[0],
                "approved": hot_desks_numbers[1]
            }
        }
        return response

    def get_hot_desk_report(self):
        """This function will call google sheet and get all hot_desk
        it will filter occupied and non occupied
        Returns:
            empty_hot_desk_number(int) Empty hot_desk,
            occupied_hot_desk(int) occupied hot_desk
        """
        google_helper = GoogleSheetHelper()
        hot_desk_record = google_helper.open_sheet()
        hot_desk_number_list = list(range(623, 644)) + [646]
        if hot_desk_record[0]:
            hot_desks = [
                work_place for work_place in hot_desk_record[0]
                if work_place["S/N"] in hot_desk_number_list
            ]
            empty_hot_desk_number = len([
                hot_desk for hot_desk in hot_desks
                if hot_desk["Name"].lower().strip() == "hot desk"
            ])
            occupied_hot_desk = len(hot_desks) - empty_hot_desk_number
            return empty_hot_desk_number, occupied_hot_desk

    def trends_allocations(self, start_date, end_date):
        """
        This method returns all trends_allocations
        Args:
            start_date(string): Value of start_date query param
            end_date(string): Value of end_date query param
        returns:
            data (dictionary): data of trend allocation
        """
        trends_allocations_data = trends_allocations_helper(
            start_date, end_date)
        return trends_allocations_data


@hot_desk_namespace.route("/analytics/<string:user_id>")
class UserHotDeskAnalytics(HotDesksAnalyticsReportResource):
    @token_required
    @permission_required(Resources.HOT_DESKS)
    @report_query_validator(['trendsallocations'])
    @report_query_date_validator
    @hot_desk_query_validator(HOT_DESK_QUERY_KEYS)
    @validate_id
    @hot_desk_namespace.doc(params=ANALYTICS_REQUEST_PARAMS)
    def get(self, *args, **kwargs):
        """
        Handles GET request for hot desks and returns response based
        on the query parameter supplied.
        Args:
            *args:
                report(str): The value of the report query parameter
                start_date(str): The value of the startDate query param in the format (YYYY-MM-DD)
                end_date(str): The value of the endDate query param in the format (YYYY-MM-DD)
            *kwargs:
                user_id(str): The token id of the requester
        """
        user_token_id = kwargs.get('user_id')
        report, start_date, end_date, _ = args
        User.get_or_404(user_token_id)
        reports = {"trendsallocations": self.trends_allocations}
        report = reports.get(report)
        if report:
            data = report(start_date, end_date, user_token_id)
            return self.response_output(data, 'trendsAllocations')

    def trends_allocations(self, start_date, end_date, user):
        """
        This method returns all trends_allocations
        Args:
            start_date(string): Value of start_date query param
            end_date(string): Value of end_date query param
        returns:
            data (dictionary): data of trend allocation
        """
        return trends_allocations_helper(
            start_date,
            end_date,
            query_key='trends_allocation_of_user',
            user_id=user)


@hot_desk_namespace.route('/cancelled/<string:requester_id>')
class CancelledHotDeskRequestsByUser(Resource):
    """Resource to fetch all cancelled hot desk requests by a user"""

    @token_required
    @permission_required(Resources.HOT_DESKS)
    @validate_id
    @report_query_date_validator
    @hot_desk_namespace.doc(params=PAGINATION_PARAMS)
    def get(self, *args, **kwargs):
        """Endpoint to fetch all cancelled hot desk requests made by a user
        Args:
            args (tuple): Tuple containing the start and end date
            kwargs (dict): Dictionary containing the requester_id
        Returns:
            dict: A dictionary containing the response sent to the user
        """
        requester_id = kwargs.get('requester_id')
        start_date, end_date = args
        paginate = get_pagination_option()

        excluded = EXCLUDED_FIELDS.copy()
        excluded.extend(['requester_id', 'requester', 'count'])

        # Get requester
        user = User.get_or_404(requester_id)
        requester = UserSchema(
            only=USER_SCHEMA_FIELDS, exclude=['role', 'image_url',
                                              'center']).dump(user).data
        # Get cancelled hot desk request
        cancelled_hot_desks = HotDeskRequest.query.filter_by(deleted=False) \
            .filter(HotDeskRequest.requester_id == requester_id,
                    HotDeskRequest.status == HotDeskRequestStatusEnum.cancelled,
                    HotDeskRequest.created_at.between(start_date, end_date)).all()
        schema = HotDeskRequestSchema(many=True, exclude=excluded)

        # Paginate the data
        hot_desk_data, meta = list_paginator(
            schema.dump(cancelled_hot_desks).data, paginate=paginate)
        data = {'requester': requester, 'hotDesks': hot_desk_data}
        return {
            'status':
            'success',
            'message':
            SUCCESS_MESSAGES['fetched'].format(
                'Cancelled hot desk requests for user'),
            'data':
            data,
            'meta':
            meta
        }
