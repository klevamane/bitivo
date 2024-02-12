"""Module that handles request related operations"""

# Flask
import json
from flask import request, jsonify
from datetime import datetime

# Third-party libraries
from flask_restplus import Resource

# Model
from api.models import Request, User
from api.models.request import request_summary

# Decorator
from api.middlewares.token_required import token_required

# Schemas
from ..schemas.request import RequestSchema, EagerLoadRequestSchema

# Validators
from ..utilities.validators.validate_id import validate_id
from ..utilities.validators.validate_json_request import validate_json_request

# utilities
from api.utilities.json_parse_objects import json_parse_objects, json_parse_request_data
from ..utilities.messages.success_messages import SUCCESS_MESSAGES
from ..utilities.error import raises
from ..utilities.messages.error_messages import request_errors
from ..utilities.error import raise_error_helper
from ..utilities.helpers.pagination_conditional import should_resource_paginate
from ..utilities.helpers.request_endpoints import user_update_data
from ..utilities.paginator import list_paginator
from ..utilities.enums import RequestStatusEnum
from ..utilities.swagger.collections.request import request_namespace
from ..utilities.swagger.collections.user import user_namespace
from ..utilities.swagger.swagger_models.request import request_model
from ..utilities.swagger.constants import (
    REQ_REQUEST_PARAMS, PAGINATION_PARAMS, SINGLE_REQUEST_PARAMS)

# Helpers
from ..utilities.helpers.endpoint_response import (
    get_success_responses_for_post_and_patch)
from ..utilities.paginator import pagination_helper

# Constants
from ..utilities.constants import EXCLUDED_FIELDS
# Resources
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@request_namespace.route('/')
class RequestResource(Resource):
    """Resource class for performing crud on request"""

    @token_required
    @request_namespace.doc(params=REQ_REQUEST_PARAMS)
    @permission_required(Resources.REQUESTS)
    def get(self):
        """Gets the list of requests"""

        include = request.args.get('include')
        response, meta = should_resource_paginate(request, Request,
                                                  RequestSchema)
        data = {
            "status": 'success',
            "message": SUCCESS_MESSAGES['fetched'].format('Requests'),
            "data": response,
            "meta": meta
        }
        where_clause = request.args.get(
            'where',
            '',
        ).split(',')

        if include and include != 'summary' and include != 'deleted':
            raises('invalid_include_key', 400, 'summary or deleted')

        elif include == 'summary':
            summary_request = request_summary(*where_clause)
            data['data'].append({'requestSummary': summary_request})
            return data
        return data

    @token_required
    @permission_required(Resources.REQUESTS)
    @validate_json_request
    @request_namespace.expect(request_model)
    def post(self):
        """POST method for creating requests.
        Payload should have the following parameters:
           subject(str): title of the request
           requestTypeId(str): id of request type
           centerId(str): id of center
           description(str): description of request
           requesterId(str): token id of requester
           attachments(list): optional image meta data dictionary
        """
        request_details = request.get_json()
        request_details['attachments'] = json_parse_objects(
            request_details.get('attachments', []))
        exclude = EXCLUDED_FIELDS.copy()
        request_schema = RequestSchema(exclude=exclude)
        request_data = request_schema.load_object_into_schema(request_details)
        request_details = Request(**request_data)
        request_details.save()
        return get_success_responses_for_post_and_patch(
            request_details,
            request_schema,
            'Request',
            status_code=201,
            message_key='created')


@request_namespace.route('/<string:request_id>')
class SingleRequestResource(Resource):
    """Request Resource class for implementing HTTP verbs."""

    @token_required
    @permission_required(Resources.REQUESTS)
    @validate_id
    @request_namespace.doc(params=SINGLE_REQUEST_PARAMS)
    def get(self, request_id):
        """Endpoint to get a request"""

        include = request.args.get('include')

        request_obj = Request.get_or_404(request_id)

        exclude = EXCLUDED_FIELDS.copy()

        request_schema = RequestSchema(exclude=exclude)

        if include == 'comments':
            request_schema = EagerLoadRequestSchema(exclude=exclude)
        elif include and include != 'comments':
            raises('invalid_include_key', 400, 'comments')

        request_data = request_schema.dump(request_obj).data

        return {
            'data': request_data,
            'message': SUCCESS_MESSAGES['fetched'].format('Request'),
            'status': 'success'
        }

    @token_required
    @permission_required(Resources.REQUESTS)
    @validate_id
    def delete(self, request_id):
        """Method to delete an existing request.
            Args:
                request_id (str): the request id
            Returns
                (dict):message and status
        """

        request_to_be_deleted = Request.get_or_404(request_id)

        # validate user
        user_id = request.decoded_token['UserInfo']['id']

        # retrieve Request status value
        status = request_to_be_deleted.status._value_

        open_status = bool(status == 'open')

        if (user_id == request_to_be_deleted.requester_id and open_status):
            request_to_be_deleted.delete()
            return {
                "status": "success",
                "message": SUCCESS_MESSAGES["deleted"].format("Request")
            }, 200
        elif not open_status:
            raises('processed status', 403, 'Request')
        else:
            raises('cannot_delete', 403, 'Request')

    @token_required
    @permission_required(Resources.REQUESTS)
    @validate_id
    @validate_json_request
    @request_namespace.expect(request_model)
    def patch(self, request_id):
        """Method to update an existing request.
         Args:
            request_id (int): the request id
         Returns:
            dict: a dictionary of the updated request, message and status
        """
        request_to_edit = Request.get_or_404(request_id)
        request_schema = RequestSchema()
        request_data = request.get_json()

        requester_id = request_to_edit.requester_id
        current_user_id = request.decoded_token['UserInfo']['id']

        responder_id = request_to_edit.responder_id

        if current_user_id == requester_id and current_user_id == responder_id:
            raise_error_helper(True, request_errors,
                               'cannot_be_requester_responder')
        is_not_allowed = current_user_id not in [requester_id, responder_id]
        raise_error_helper(is_not_allowed, request_errors, 'not_allowed')

        json_parse_request_data(request_data)

        update_data = request_schema.load_object_into_schema(
            request_data, partial=True)

        user_action = user_update_data(current_user_id, requester_id)

        update_data = user_action(update_data, request_to_edit)
        request_to_edit.update_(**update_data)

        edited_request = request_schema.dump(request_to_edit).data

        return {
            "data": edited_request,
            "status": "success",
            "message": SUCCESS_MESSAGES['edited'].format('Request')
        }


@user_namespace.route('/<string:person_id>/requests')
class UserRequestResource(Resource):
    """Resource class for getting a user requests"""

    @token_required
    @permission_required(Resources.REQUESTS)
    @validate_id
    @user_namespace.doc(params=PAGINATION_PARAMS)
    def get(self, person_id):
        """Method to get request of a particular user.
         Args:
            person_id (str): the user token
         Returns:
            dict: a dictionary of the user's request, message and status
        """

        User.get_or_404(person_id)

        extra_query = {'requester_id': person_id}
        data, pagination_object = should_resource_paginate(
            request, Request, RequestSchema, extra_query=extra_query)

        return {
            "status": 'success',
            "message": SUCCESS_MESSAGES['fetched'].format('Requests'),
            "data": data,
            "meta": pagination_object
        }


@request_namespace.route('/overdue')
class OverdueRequestResource(Resource):
    """Resource class for getting overdue requests """

    @token_required
    @permission_required(Resources.REQUESTS)
    @request_namespace.doc(params=PAGINATION_PARAMS)
    def get(self):
        """ Method to get a list of all overdue requests """
        response = Request.query_().filter(
            Request.due_by < datetime.now(),
            Request.status.in_(
                [RequestStatusEnum.open,
                 RequestStatusEnum.in_progress])).all()
        request_schema = RequestSchema(many=True, exclude=EXCLUDED_FIELDS)
        overdue = request_schema.dump(response).data
        result, meta = list_paginator(overdue)
        data = {
            'status': 'success',
            'message': SUCCESS_MESSAGES['fetched'].format('Requests'),
            'data': result,
            'meta': meta
        }
        return data
