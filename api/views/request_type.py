"""Module that handles request-type related operations"""

# Third party libraries
from flask_restplus import Resource

# Paginator
from api.utilities.paginator import pagination_helper

# Main
from flask import request

# Models
from ..models import RequestType, User

# Schemas
from ..schemas.request_type import RequestTypeSchema

# Middleware
from ..middlewares.token_required import token_required

# Messages
from ..utilities.messages.success_messages import SUCCESS_MESSAGES
from ..utilities.constants import EXCLUDED_FIELDS

# Validators
from ..utilities.validators.validate_json_request import validate_json_request
from ..utilities.validators.validate_id import validate_id

# Helpers
from ..utilities.helpers.resource_manipulation_for_delete import delete_by_id
from ..utilities.helpers.endpoint_response import get_success_responses_for_post_and_patch

# utilities
from ..utilities.constants import EXCLUDED_FIELDS
from ..utilities.messages.success_messages import SUCCESS_MESSAGES
from ..utilities.helpers.pagination_conditional import should_resource_paginate
from ..utilities.swagger.collections.request_type import request_type_namespace
from ..utilities.swagger.swagger_models.request_type import request_type_model
from ..utilities.swagger.constants import PAGINATION_PARAMS

# Schema
from ..schemas.request_type import RequestTypeSchema
from ..utilities.validators.validate_json_request import validate_json_request
# Resources
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@request_type_namespace.route('/')
class RequestTypeResource(Resource):
    """
    Resource class for getting request-types
    """

    @token_required
    @permission_required(Resources.REQUEST_TYPES)
    @request_type_namespace.doc(params=PAGINATION_PARAMS)
    def get(self):
        """Gets list of request-types.

        Returns:
            dict: The response with the request types data
        """
        data, meta = should_resource_paginate(request, RequestType,
                                              RequestTypeSchema)

        # success message
        message = SUCCESS_MESSAGES['successfully_fetched'].format(
            'Request types')

        return {
            "status": "success",
            "message": message,
            "data": data,
            "meta": meta,
        }

    @token_required
    @permission_required(Resources.REQUEST_TYPES)
    @validate_json_request
    @request_type_namespace.expect(request_type_model)
    def post(self):  # pylint: disable=R0201
        """ An endpoint that creates a new request-type in the database """

        request_data = request.get_json()
        request_type_schema = RequestTypeSchema(exclude=EXCLUDED_FIELDS)
        request_type_data = request_type_schema.load_object_into_schema(
            request_data)
        user_id = request.decoded_token['UserInfo']['id']
        User.get_or_404(user_id)
        request_type_data['created_by'] = user_id
        request_type = RequestType(**request_type_data).save()

        return get_success_responses_for_post_and_patch(
            request_type,
            request_type_schema,
            'Request type',
            status_code=201,
            message_key='created')


@request_type_namespace.route('/<string:request_type_id>')
class SingleRequestTypeResource(Resource):
    """Resource class class for carrying out operations on a single request type"""

    @token_required
    @permission_required(Resources.REQUEST_TYPES)
    @validate_id
    def delete(self, request_type_id):
        """Soft delete request type"""

        return delete_by_id(RequestType, request_type_id, 'Request Type')

    @token_required
    @permission_required(Resources.REQUEST_TYPES)
    def get(self, request_type_id):
        """Gets a role that matches the request_type_id.

        Args:
            request_type_id: the id of the request type

        Returns:
            dict : A dictionary containing the response sent to the user
        """

        request_types = RequestType.get_or_404(request_type_id)
        schema = RequestTypeSchema(exclude=EXCLUDED_FIELDS)
        data = schema.dump(request_types).data

        return {
            "status":
            "success",
            "message":
            SUCCESS_MESSAGES['successfully_fetched'].format("Request type"),
            'data':
            data
        }

    @token_required
    @permission_required(Resources.REQUEST_TYPES)
    @validate_id
    @validate_json_request
    @request_type_namespace.expect(request_type_model)
    def patch(self, request_type_id):
        """
        Handles update for a request type

        Args:
            request_type_id (str): the parameter from the request URL

        Returns:
                json: the updated data
        """

        request_type = RequestType.get_or_404(request_type_id)
        request_data = request.get_json()
        request_type_schema = RequestTypeSchema(
            context={'request_type_id': request_type_id},
            exclude=EXCLUDED_FIELDS)
        request_type_data = request_type_schema.load_object_into_schema(
            request_data, partial=True)

        # update the request type
        request_type.update_(**request_type_data)

        return get_success_responses_for_post_and_patch(
            request_type,
            request_type_schema,
            'Request type',
            status_code=200,
            message_key='edited')
