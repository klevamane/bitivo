"""Module for center resources"""

from flask_restplus import Resource
from flask import request

from api.utilities.swagger.collections.center import centers_namespace
from api.utilities.swagger.swagger_models.center import centers_model
from ..schemas.center import CenterSchema
from api.middlewares.token_required import token_required
from api.models.center import Center
from api.models.database import db
from api.utilities.validators.validate_id import validate_id
from ..schemas.user import UserSchema
from ..utilities.validators.validate_json_request import validate_json_request
from ..utilities.messages.success_messages import SUCCESS_MESSAGES
from ..utilities.messages.error_messages import serialization_errors
from ..utilities.constants import EXCLUDED_FIELDS
from ..utilities.helpers.endpoint_response import get_success_responses_for_post_and_patch
from api.middlewares.base_validator import ValidationError
from ..utilities.dump_data import dump_data
# Resources
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@centers_namespace.route("/")
class CenterResource(Resource):
    """
    Resource class for creating and getting centers
    """

    @token_required
    @permission_required(Resources.CENTERS)
    @validate_json_request
    @centers_namespace.expect(centers_model)
    def post(self):
        """
        POST method for creating centers.

        Payload should have the following parameters:
            name(str): name of the center
            image(dict): image meta data
        """

        request_data = request.get_json()

        center_schema = CenterSchema(
            only=["id", "name", "image", "created_at", "updated_at"])
        center_data = center_schema.load_object_into_schema(request_data)

        center = Center(**center_data)
        center.save()
        return get_success_responses_for_post_and_patch(
            center,
            center_schema,
            'Center',
            status_code=201,
            message_key='created')

    @token_required
    def get(self):
        """
        Gets center list and the user count
        """
        args = request.args.to_dict()
        deleted = args.get('include')
        centers = Center.query_(request.args).all()  # pylint: disable=W0212

        centers = Center.query_(request.args, include_deleted=True).all() \
            if deleted == 'deleted' else centers

        # include deleted field when retrieving with deleted objects
        only = ["id", "name", "image", "user_count"]
        only = tuple(only +
                     ['deleted']) if deleted == 'deleted' else tuple(only)

        centers_schema = CenterSchema(many=True, only=only)
        data = dump_data(centers_schema, centers, deleted, args)
        return {
            "data": data,
            "message": SUCCESS_MESSAGES["fetched"].format("Centers"),
            "status": "success",
        }, 200


@centers_namespace.route('/<string:center_id>')
class SingleCenterResource(Resource):
    """Resource class for carrying out operations on a single center"""

    @token_required
    @permission_required(Resources.CENTERS)
    @validate_id
    def delete(self, center_id):  # pylint: disable=C0103, W0622
        """
        A method for deleting a center
        """

        center = Center.get_or_404(center_id)
        center.delete()

        message = SUCCESS_MESSAGES['center_deleted'].format(center.name)

        return {
            'status': 'success',
            'message': message,
        }, 200

    @token_required
    @permission_required(Resources.CENTERS)
    @validate_id
    @validate_json_request
    @centers_namespace.expect(centers_model)
    def patch(self, center_id):  # pylint: disable=C0103, W0622
        """
        PATCH method for updating centers.

        Payload should have the following parameters:
            name(str): name of the center
            image(dict): image meta data

        Return Payload should have the following:
            status(str): status message
            message(str): information on what has been updated
            data(dict): updated center information
        """

        center = Center.get_or_404(center_id)

        request_data = request.get_json()

        request_data['updated_by'] = request.decoded_token['UserInfo']['id']
        request_data['id'] = center_id

        center_schema = CenterSchema()

        center_data = center_schema.load_object_into_schema(
            request_data, partial=True)

        center.update_(**center_data)  # pylint: disable=W0212

        return get_success_responses_for_post_and_patch(
            center,
            center_schema,
            'Center',
            status_code=200,
            message_key='updated')


@centers_namespace.route('/<string:center_id>/people')
class CenterUsersResource(Resource):
    """Resource class for users under a center"""

    @token_required
    @permission_required(Resources.CENTERS)
    @validate_id
    def get(self, center_id):
        """Endpoint to get users in a center."""

        args = request.args.to_dict()

        center = Center.query_(include_deleted=True).get(center_id) \
            if args and args.get('include') == 'deleted' else Center.get_or_404(center_id)

        if not center:
            raise ValidationError(
                {
                    'message': 'Center not found'  # noqa
                },
                404)

        # include deleted field when retrieving data with deleted objects included
        exclude = ['center', 'role.resource_access_levels'] if args and args.get('include')== 'deleted' \
            else ['deleted', 'center', 'role.resource_access_levels']

        user_schema = UserSchema(exclude=exclude, many=True)

        users = center.users.all()
        data = user_schema.dump(users, request_args=args).data if args and args.get('include') == 'deleted' \
                    else user_schema.dump(users).data

        # filter data depending on the args since multiple joins to add
        # 'role.resource_access_levels' reset the data
        data = filter_data(args, users, data)

        return {
            'status': 'success',
            'message':
            SUCCESS_MESSAGES['get_center_people'].format(center.name),
            'data': data
        }, 200


def filter_data(args, users, data):
    """Filter resetted data after further joins

    Args:
        args(dict): dictionary containing request args
        users(list): list of user objects to compare with
        data(list): list of reset data after adding
                    'role.resource_access_levels' for users

    Returns:
        data(list): list of filtered data
    """

    include = args.get('include')
    undeleted = []
    if include != 'deleted':
        # use list comprehension to populate the undeleted list
        list_of_none_objects = [undeleted.append(item) for item in data for user in users\
                if item['name'] == user.name and not user.deleted]
        return undeleted
    return data
