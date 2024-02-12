"""Module for permission resources"""
from flask_restplus import Resource
from flask import request

from main import api

# Schemas
from ..schemas.permission import PermissionSchema

# Decorators
from api.middlewares.token_required import token_required
from api.middlewares.permission_required import permission_required, Resources

# Utilities
from api.utilities.constants import EXCLUDED_FIELDS
from api.utilities.validators.validate_json_request import validate_json_request

# Models
from ..models.permission import Permission

# Messages
from ..utilities.messages.success_messages import SUCCESS_MESSAGES

# Helpers
from ..utilities.helpers.endpoint_response import get_success_responses_for_post_and_patch

from ..utilities.dump_data import dump_data
from api.utilities.swagger.collections.permission import permission_namespace
from api.utilities.swagger.swagger_models.permission import permission_model


@permission_namespace.route('/')
class PermissionResource(Resource):
    """
    Resource class for creating and getting permissions
    """

    @token_required
    @permission_required(Resources.PERMISSIONS)
    @validate_json_request
    @permission_namespace.expect(permission_model)
    def post(self):
        """
        Permissions endpoint

        Payload should have the following parameters:
            type(str): type of the permission
        """
        request_data = request.get_json()

        permission_schema = PermissionSchema(exclude=EXCLUDED_FIELDS)
        permission_data = permission_schema.load_object_into_schema(
            request_data)

        permission = Permission(**permission_data)
        permission.save()

        return get_success_responses_for_post_and_patch(
            permission,
            permission_schema,
            'Permission',
            status_code=201,
            message_key='created')

    @token_required
    @permission_required(Resources.PERMISSIONS)
    def get(self):
        """
        Gets list of all permissions
        """
        args = request.args.to_dict()
        deleted = args.get('include')

        permissions = Permission.query_()

        permissions = Permission.query_(include_deleted=True)\
            if deleted and deleted == 'deleted' else permissions

        only = ['id', 'type']

        only = ['id', 'type', 'deleted'
                ] if deleted and deleted == 'deleted' else only

        permission_schema = PermissionSchema(many=True, only=only)

        data = dump_data(permission_schema, permissions, deleted, args)

        return {
            'status': 'success',
            'message': SUCCESS_MESSAGES['fetched'].format('Permissions'),
            'data': data,
        }
