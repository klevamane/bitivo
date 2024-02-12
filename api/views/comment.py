""" Resources for comments module. """

# Third-party libraries
from flask_restplus import Resource
from flask import request

# Models
from ..models import Comment, Request, Schedule

# Schemas
from ..schemas.comment import CommentSchema

# Middleware
from ..middlewares.token_required import token_required
from ..utilities.validators.validate_id import validate_id

# Utilities
from ..utilities.validators.validate_json_request import validate_json_request
from ..utilities.messages.success_messages import SUCCESS_MESSAGES
from ..utilities.constants import EXCLUDED_FIELDS
from ..utilities.error import raises
from ..utilities.helpers.endpoint_response import get_success_responses_for_post_and_patch
from api.utilities.paginator import pagination_helper
from api.utilities.helpers.resource_manipulation import get_all_resources
from api.utilities.helpers.pagination_conditional import should_resource_paginate
from api.utilities.swagger.collections.comment import comment_namespace
from api.utilities.swagger.collections.request import request_namespace
from api.utilities.swagger.collections.schedule import schedule_namespace
from api.utilities.swagger.swagger_models.comment import comment_model
from api.utilities.swagger.constants import PAGINATION_PARAMS

# Validators
from api.utilities.validators.validate_id import validate_id
from api.utilities.error import raises
from ..utilities.validators.comments_validator import check_parent_type_value_exists, validate_parent_id_matches_parent_type

# Enums
from ..utilities.enums import ParentType

# Resourses
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@comment_namespace.route('/')
class CommentResource(Resource):
    """ Resource class for creating and getting a list of comments. """

    @token_required
    @permission_required(Resources.COMMENTS)
    @validate_json_request
    @comment_namespace.expect(comment_model)
    def post(self):
        """ Creates a comment.

        Returns:
            Response (dict): Returns status, success message, and data.
        """
        comment_data = request.get_json()
        comment_data['authorId'] = request.decoded_token['UserInfo']['id']
        if comment_data.get('parentType', None):
            check_parent_type_value_exists(comment_data)
        validate_parent_id_matches_parent_type(comment_data)

        schema = CommentSchema(exclude=EXCLUDED_FIELDS)
        data = schema.load_object_into_schema(comment_data)

        comment = Comment(**data)
        comment.save()

        return get_success_responses_for_post_and_patch(
            comment, schema, 'Comment', status_code=201, message_key='created')


@comment_namespace.route('/<string:comment_id>')
class SingleCommentResource(Resource):
    """Resource  to carrying out operations on a single comment"""

    @token_required
    @permission_required(Resources.COMMENTS)
    @validate_json_request
    @comment_namespace.expect(comment_model)
    def patch(self, comment_id):
        """Update a comment

        Args:
            comment_id (str): The id of the comment to edit

        Returns:
            Response (dict) : Returns data, success message, and status.
        """
        comment = Comment.get_or_404(comment_id)
        update = request.get_json()
        if request.decoded_token['UserInfo']['id'] != comment.author_id:
            raises('not_owner', 403)

        schema = CommentSchema(exclude=EXCLUDED_FIELDS)
        data = schema.load_object_into_schema(
            update, partial=['parent_id', 'parent_type', 'author_id'])

        comment.update_(**data)
        return (
            {
                "data": schema.dump(comment).data,
                "status": "success",
                "message": SUCCESS_MESSAGES["edited"].format("Comment"),
            },
            200,
        )

    @token_required
    @permission_required(Resources.COMMENTS)
    @validate_id
    def delete(self, comment_id):
        """Soft delete comment"""

        comment = Comment.get_or_404(comment_id)
        user_id = request.decoded_token['UserInfo']['id']
        if user_id == comment.author_id:
            comment.delete()
        else:
            raises('delete_error', 400, 'Comment')

        return {
            'status': 'success',
            'message': SUCCESS_MESSAGES['deleted'].format('Comment')
        }


@request_namespace.route('/<string:request_id>/comments')
class RequestCommentsResource(Resource):
    """ Resource class for comments CRUD operations """

    @token_required
    @permission_required(Resources.COMMENTS)
    @validate_id
    def get(self, request_id):
        """ Gets all comments belonging to a specific request
        Args:
            self (CommentResource): instance of comment resource
            request_id (string): id of the request to get comments for

        Returns:
            JSON: list of comments
        """
        the_request = Request.get_or_404(request_id)

        # remove deleted field from excluded fields
        excluded_fields = EXCLUDED_FIELDS.copy()
        excluded_fields.remove('deleted')
        comment_schema = CommentSchema(many=True, exclude=excluded_fields)

        return {
            "data": comment_schema.dump(the_request.comments).data,
            "message": SUCCESS_MESSAGES['fetched'].format('Comments'),
            "status": "success"
        }


@schedule_namespace.route('/<string:schedule_id>/comments')
class ScheduleCommentsResource(Resource):
    """ Resource class for comments """

    @token_required
    @permission_required(Resources.COMMENTS)
    @validate_id
    @schedule_namespace.doc(params=PAGINATION_PARAMS)
    def get(self, schedule_id):
        """ Gets all comments belonging to a specific schedule
        Args:
            self (CommentResource): instance of comment resource
            schedule_id (string): the id of the schedule

        Returns:
            JSON: list of comments
        """

        excluded_fields = EXCLUDED_FIELDS.copy()
        excluded_fields.append('parent_type')
        schedule_object = Schedule.get_or_404(schedule_id)
        data, pagination_object = should_resource_paginate(
            request, Comment, CommentSchema, exclude=excluded_fields)

        return {
            "status": 'success',
            "message":
            SUCCESS_MESSAGES['successfully_fetched'].format('Comments'),
            "data": data,
            "meta": pagination_object
        }
