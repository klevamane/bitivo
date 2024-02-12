"""Module for Hot Desk Resource report """
from sqlalchemy import text, and_, or_
from main import api

from datetime import datetime, timedelta
from flask import request
from flask_restplus import Resource
from api.models import HotDeskRequest, User, HotDeskResponse
from api.models.database import db
from config import AppConfig

from api.utilities.swagger.collections.hot_desk import hot_desk_namespace
from api.utilities.swagger.constants import (HOTDESK_REQUEST_PARAMS,
                                             PAGINATION_PARAMS)
from ..utilities.sql_queries import sql_queries
from ..utilities.base_analytics import AnalyticsBase
from ..utilities.constants import (
    USER_SCHEMA_FIELDS, EXCLUDED_FIELDS, HOT_DESK_QUERY_PARAMS,
    RESPONDER_SCHEMA_FIELDS, HOT_DESK_SCHEMA_FIELDS)
from ..utilities.helpers.pagination_conditional import should_resource_paginate
from ..utilities.paginator import list_paginator, get_pagination_option
from ..utilities.validators.analytics_validator import hot_desk_query_validator
from ..utilities.validators.validate_id import validate_id
from ..utilities.verify_date_range import report_query_date_validator, verify_date_range
from ..utilities.messages.success_messages import SUCCESS_MESSAGES
from ..utilities.validators.hot_desk_resource_validator import validate_hot_desk_status, validate_param_value
from ..utilities.helpers.hot_desk import filter_hotdesk_response

from ..middlewares.token_required import token_required

from ..schemas.hot_desk import (
    UserHotDeskRequestSchema, HotDeskRequestCancellationCountSchema,
    ResponderHotdeskCountSchema, HotDeskRequestSchema)
from ..schemas.hot_desk_response import HotDeskResponseSchema
from ..schemas.user import UserSchema
# Resources
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@hot_desk_namespace.route('/')
class HotDesksResource(Resource, AnalyticsBase):
    """Resource class for hot desk requests by a user"""

    @token_required
    @permission_required(Resources.HOT_DESKS)
    @hot_desk_query_validator(HOT_DESK_QUERY_PARAMS)
    @report_query_date_validator
    @hot_desk_namespace.doc(params=HOTDESK_REQUEST_PARAMS)
    def get(self, *args):
        """
        Handles GET request for hot-desk requests by a user and returns response based
        on the supplied query params
        Args:
            query_param_value (string): The value of the query parameter
        Returns:
            response_output (func): Function that formats the response sent
        """
        query_param_value, start_date, end_date = args
        status = request.args.get('status', '')
        query_param = request.args.to_dict()
        query_param_key = list(query_param.keys())[0]
        response_mapper = {'requester': 'HotDeskRequestByUser'}
        query_params_mapper = {
            "requester": self.get_requester,
            "responder": self.get_responder,
            "cancel": self.get_cancelled_requests,
            "count": self.get_hot_desk_response_counts,
            "escalation": self.get_escalation_count
        }
        if query_param_key == 'requester':
            query_param_ = query_params_mapper.get(query_param_key, '')
            data = query_param_(query_param_value)
            return self.response_output(data,
                                        response_mapper.get(query_param_key))
        elif query_param_key == 'responder':
            query_param_ = query_params_mapper.get(query_param_key, '')
            data = query_param_(query_param_value, status, start_date,
                                end_date)
            return data
        else:
            query_param_ = query_params_mapper.get(query_param_key, '')
            data = query_param_(query_param_value, start_date, end_date)
            return data

    def get_requester(self, requester):
        """ Gets all hot desk requests by a user
        Args:
            requester (string): The query parameter for the requester's token_id
        Returns:
            dictionary: a dictionary of the data of all requests by the user and the meta data
        """
        user = User.get_or_404(requester)
        requester_info = UserSchema(only=USER_SCHEMA_FIELDS).dump(user).data
        data, meta = should_resource_paginate(
            request,
            HotDeskRequest,
            UserHotDeskRequestSchema,
            extra_query={'requester_id': requester})
        data = {'requester': requester_info, 'hotDesks': data}
        return {'data': data, 'meta': meta}

    def get_responder(self, *args):
        """ Gets all hot desk requests assigned to a responder
        Args:
            responder (str): The responder's token_id from the query param
            status(str): The hot desk request status
            start_date (date): Start date. Defaults to 7 days difference from the end_date
            end_date (date): End date. Defaults to the current date
        Returns:
            dict: A dict of all hot desk requests assigned to the responder
            grouped by status
        """
        responder, status, startdate, enddate = args

        startdate, enddate = verify_date_range(
            startdate.strftime('%Y-%m-%d'), enddate.strftime('%Y-%m-%d'))

        validate_hot_desk_status(status)
        responder_details = UserSchema(only=RESPONDER_SCHEMA_FIELDS).dump(
            User.get_or_404(responder)).data
        approved = filter_hotdesk_response('approved', responder, startdate,
                                           enddate)
        rejected = filter_hotdesk_response('rejected', responder, startdate,
                                           enddate)
        pending_time = (datetime.utcnow() -
                        timedelta(milliseconds=int(AppConfig.BOT_COUNTDOWN)))
        missed = HotDeskResponse.query_().filter(
            or_(
                and_(HotDeskResponse.assignee_id == responder,
                     HotDeskResponse.status == 'pending',
                     HotDeskResponse.created_at < pending_time),
                HotDeskResponse.is_escalated == True)).filter(
                    HotDeskResponse.created_at.between(startdate,
                                                       enddate)).all()
        schema = HotDeskResponseSchema(only=HOT_DESK_SCHEMA_FIELDS, many=True)
        approvedHotDesks, approvedMeta = list_paginator(
            schema.dump(approved).data)
        rejectedHotDesks, rejectedMeta = list_paginator(
            schema.dump(rejected).data)
        pendingHotDesks, pendingMeta = list_paginator(schema.dump(missed).data)
        hot_desks = dict(responder=responder_details)
        if status == 'approved':
            hot_desks['approvedHotDesks'] = approvedHotDesks
            hot_desks['meta'] = approvedMeta
        elif status == 'rejected':
            hot_desks['rejectedHotDesks'] = rejectedHotDesks
            hot_desks['meta'] = rejectedMeta
        else:
            hot_desks['missedHotDesks'] = pendingHotDesks
            hot_desks['meta'] = pendingMeta

        data = {
            "status": "success",
            "message": "Hot desks requests fetched successfully",
            'data': hot_desks
        }
        return data

    def get_cancelled_requests(self, *args):
        """Gets hot desk counts for reasons of cancellation
        Args:
            param_value (string): value for the cancel key param
            start_date (date): Start date. Defaults to 7 days difference from the end_date
            end_date (date): End date. Defaults to the current date
        Returns:
            dictionary: a dictionary of the hot-desk cancelled request data
        """

        param_value, start_date, end_date = args

        validate_param_value(param_value)

        cancelled_hot_dest_reasons_count = sql_queries[
            'get_cancellation_reasons_count'].format(start_date, end_date)
        count_data = db.engine.execute(
            text(cancelled_hot_dest_reasons_count)).fetchall()
        schema = HotDeskRequestCancellationCountSchema(
            many=True, exclude=EXCLUDED_FIELDS)
        reasons_count = schema.dump(count_data).data[0]
        response = {
            'status':
            'Success',
            'data':
            reasons_count,
            'message':
            SUCCESS_MESSAGES['fetched'].format('Hot desk cancellation report'),
        }
        return response

    def get_hot_desk_response_counts(self, *args):
        """Gets the hot desk response count
        - it gives details of hotdesk that has been approved,
        rejected or missed by assignee
        Args:
            param_value(Boolean): The count value
            start_date (date): Start date. Defaults to 7 days difference from the end_date
            end_date (date): End date. Defaults to the current date
        Returns:
            dictionary: a dictionary of the hot-desk assignee counts
        """
        param_value, start_date, end_date = args
        validate_param_value(param_value)
        pending_time = (datetime.utcnow() -
                        timedelta(milliseconds=int(AppConfig.BOT_COUNTDOWN)))
        responders_hot_desk_data = sql_queries[
            'hotdesk_responder_counts'].format(pending_time, start_date,
                                               end_date)

        count_data = db.engine.execute(
            text(responders_hot_desk_data)).fetchall()
        schema = ResponderHotdeskCountSchema(
            many=True, exclude=EXCLUDED_FIELDS)
        all_data, meta = list_paginator(schema.dump(count_data).data)
        hot_desk_count = {}
        hot_desk_count['responseCounts'] = all_data
        hot_desk_count['meta'] = meta
        data = {
            "status":
            "success",
            "message":
            SUCCESS_MESSAGES['successfully_fetched'].format('responseCounts'),
            'data':
            hot_desk_count
        }
        return data

    def get_escalation_count(self, *args):
        """Gets count count of all escalation email sent between a specific period
        Args:
            param_value (string): value for the escalation key param
            start_date (date): Start date. Defaults to 7 days difference from the end_date
            end_date (date): End date. Defaults to the current date

        Returns:
            dictionary: a dictionary of the hot-desk cancelled request data
        """

        param_value, start_date, end_date = args

        validate_param_value(param_value)

        escalation_count = HotDeskResponse.query_().filter_by(
            is_escalated=True).filter(
                HotDeskResponse.created_at.between(start_date,
                                                   end_date)).count()

        data = {
            'status':
            'Success',
            'data': {
                'escalationCount': escalation_count,
            },
            'message':
            SUCCESS_MESSAGES['fetched'].format('Hot desk escalation report'),
        }
        return data


@hot_desk_namespace.route('/complaints/<string:user_id>')
class HotDeskComplaintsResource(Resource):
    """Resource class for hot desk complaints by a user"""

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
        user_id = kwargs.get('user_id')
        start_date, end_date = args
        paginate = get_pagination_option()
        user = User.get_or_404(user_id)
        only = ('name', 'email', 'token_id')
        requester_info = UserSchema(only=only).dump(user).data

        query = HotDeskRequest.query_().filter_by(requester_id=user_id).filter(
            HotDeskRequest.complaint != None,
            HotDeskRequest.complaint_created_at.between(start_date,
                                                        end_date)).all()

        excluded = EXCLUDED_FIELDS.copy()
        excluded.extend(
            ['requester_id', 'assignee_id', 'requester', 'count', 'reason'])
        data = HotDeskRequestSchema(
            exclude=excluded, many=True).dump(query).data
        result, meta = list_paginator(data, paginate)
        return {
            'status':
            'success',
            'message':
            SUCCESS_MESSAGES['fetched'].format('hot desks with complaints'),
            'data': {
                'requester': requester_info,
                'hotDesksWithComplaints': result
            },
            'meta':
            meta
        }
