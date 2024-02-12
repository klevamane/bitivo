"""Module for role resources"""

from flask_restplus import Resource
from flask import jsonify, request

# Schemas
from ..schemas.role import RoleSchema
from ..schemas.permission import PermissionSchema
from ..schemas.resource import ResourceSchema

# Middlewares
from ..middlewares.token_required import token_required

# Utilities
from ..utilities.validators.validate_json_request import (
    validate_json_request, validate_resource_access_level_field)

from ..utilities.helpers.role_endpoint import update_resource_access_levels
from ..utilities.helpers.filter_resource_list import filter_resource_list
from ..utilities.query_parser import QueryParser
from ..utilities.swagger.collections.role import role_namespace
from ..utilities.swagger.swagger_models.role import role_model

# Models
from ..models import Role, Resource as ResourceModel, Permission

# Messages
from ..utilities.messages.success_messages import SUCCESS_MESSAGES

# Constants
from ..utilities.constants import EXCLUDED_FIELDS

# Validators
from ..utilities.validators.validate_id import validate_id

# Helpers
from ..utilities.helpers.resource_manipulation_for_delete import delete_by_id
from ..utilities.helpers.endpoint_response import get_success_responses_for_post_and_patch
# Resourses
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@role_namespace.route('/')
class RoleResource(Resource):
    """
    Resource class for creating and getting roles
    """

    @token_required
    @permission_required(Resources.ROLES)
    def get(self):
        """
        Gets list of all roles

        Args:
            self (RoleResource): instance of role resource

        Returns:
            JSON: list of roles, permissions, and resources
        """

        # Resources to be sided loaded
        additional_resources = {
            'permissions': (Permission, PermissionSchema, ['id', 'type']),
            'resources': (ResourceModel, ResourceSchema, ['id', 'name'])
        }

        additional_data = {}
        query_strings = request.args.getlist('include')
        include = request.args.to_dict().get('include')

        for query in query_strings:
            query = query.lower()
            if query in additional_resources:
                model, schema, only = additional_resources[query]
                additional_data[query] = schema(
                    many=True, only=only).dump(
                        filter_resource_list(model, query).all()).data
        if request.args:
            query_dict = request.args.to_dict()
            query_keys = ('include')
            QueryParser.validate_include_key(query_keys, query_dict)

        roles = RoleResource.get_roles(include, query_strings,
                                       additional_resources, additional_data)

        only = ['id', 'title', 'description', 'user_count',
                'resource_access_levels', 'deleted'] if include == 'deleted' \
                    else ['id', 'title', 'description', 'user_count', 'resource_access_levels']

        roles_data = RoleSchema(
            many=True,
            only=only,
        ).dump(roles).data

        return jsonify({
            'status': 'success',
            'message': SUCCESS_MESSAGES['fetched'].format('Roles'),
            'data': roles_data,
            **additional_data
        })

    @staticmethod
    def get_roles(*args):
        """Returns roles depending on the params passed
        """
        include, query_strings, additional_resources, additional_data = args
        for query in query_strings:
            query = query.lower()
            if query in additional_resources:
                model, schema, only = additional_resources[query]
                additional_data[query] = schema(
                    many=True, only=only).dump(
                        filter_resource_list(model, query).all()).data

        roles = Role.query_().all()
        roles = Role.query_(include_deleted=True).all() \
            if include == 'deleted' else roles

        return roles

    @token_required
    @permission_required(Resources.ROLES)
    @validate_json_request
    @validate_resource_access_level_field
    @role_namespace.expect(role_model)
    def post(self):
        """
        Creates a role

        Returns:
            (dict): Returns status and success message
            data(dict): Returns the id, title and description of the role created
        """

        request_data = request.get_json()
        role_schema = RoleSchema(exclude=EXCLUDED_FIELDS)
        role_schema.context['request'] = request
        role_data = role_schema.load_object_into_schema(request_data)

        role = Role(**role_data)
        role.save()
        update_resource_access_levels(
            role.id, role_schema.validated_resource_access_levels)

        return (
            {
                "status": "success",
                "message": SUCCESS_MESSAGES["created"].format("Role"),
                "data": role_schema.dump(role).data,
            },
            201,
        )


@role_namespace.route('/<string:role_id>')
class SingleRoleResource(Resource):
    """
    Resource class for carrying out operations on a single role
    for example patch a single role
    """

    @token_required
    @permission_required(Resources.ROLES)
    @validate_id
    def delete(self, role_id):
        """
        Delete a role

        Arguments:
            role_id (string): Id of the particular role

        Raises:
            ValidationError: Use to raise exception if role does not exist

        Returns:
            (dict) -- Returns status and success message
        """

        return delete_by_id(Role, role_id, 'Role')

    @token_required
    @permission_required(Resources.ROLES)
    @validate_id
    @validate_json_request
    @role_namespace.expect(role_model)
    def patch(self, role_id):
        """
        PATCH method for updating roles.

        Method parameters:
            role_id (str): the unique id of the role in question

        Request payload should have the following parameters:
            title (str): the name of the role to update
            description (str): gives more details about the title

        Response payload should have the following parameters:
            data (dict): a dictionary with the updated information
            message (str): a message showing role update success
            status (str): a message showing role was updated successfully
        """

        role = Role.get_or_404(role_id)
        request_data = request.get_json()
        request_data['id'] = role_id

        role_schema = RoleSchema(exclude=EXCLUDED_FIELDS)
        role_schema.context['request'] = request

        role_data = role_schema.load_object_into_schema(
            request_data, partial=True)

        role.update_(**role_data)

        return get_success_responses_for_post_and_patch(
            role, role_schema, 'Role', status_code=200, message_key='updated')
