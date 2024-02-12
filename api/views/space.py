"""Module for spaces resource"""
from flask_restplus import Resource
from flask import request
from sqlalchemy import text

# Documentation
from api.utilities.swagger.collections.space_type import space_namespace
from api.utilities.swagger.swagger_models.space_type import space_models

from api.middlewares.base_validator import ValidationError
from api.models.database import db
from ..schemas.space_type import SpaceTypeSchema
from ..models import Center, SpaceType, Space
from ..schemas.space import SpaceSchema
from ..middlewares.token_required import token_required
from ..utilities.messages.error_messages import database_errors
from ..utilities.validators.validate_id import validate_id
from ..utilities.helpers.spaces import space_query, update_space_type
from ..utilities.validators.space_validator import SpaceValidator
from ..utilities.validators.space_query_validator import validate_query
from ..utilities.validators.validate_json_request import validate_json_request
from ..utilities.messages.success_messages import SUCCESS_MESSAGES
from ..utilities.query_parser import QueryParser
from ..utilities.helpers.resource_manipulation_for_delete import delete_by_id
from ..utilities.helpers.endpoint_response \
    import get_success_responses_for_post_and_patch
from ..utilities.sql_queries import sql_queries
from api.utilities.swagger.constants import SPACE_REQUEST_PARAMS
# Resources
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@space_namespace.route('/')
class SpaceResource(Resource):
    """Resource class for adding space"""

    @token_required
    @permission_required(Resources.SPACES)
    @validate_json_request
    @space_namespace.expect(space_models)
    def post(self):
        """
        Add a space to a center

        Raises:
            (ValidationError): Used to raise exception if validation during
            creation of space fails

        Returns:
            (tuple): Returns status, success message and relevant space details
        """
        request_data = request.get_json()

        # Initializes the space schema
        space_schema = SpaceSchema(only=[
            'id', 'name', 'parent_id', 'space_type_id', 'center_id',
            'children', 'space_type'
        ])

        # Deserializes and validates space data.
        space_data = space_schema.load_object_into_schema(request_data)

        # Checks if specified center exists.
        center = Center.get_or_404(request_data['centerId'])

        # Checks if specified space_type exists.
        space = SpaceValidator.validate(request_data, space_data)

        # Creates space model and saves data to database.
        space.save()

        # Returns a response
        return get_success_responses_for_post_and_patch(
            space,
            space_schema,
            space.name,
            center.name,
            status_code=201,
            message_key='added_to_center')

    @token_required
    @permission_required(Resources.SPACES)
    @validate_id
    @space_namespace.doc(params=SPACE_REQUEST_PARAMS)
    def get(self):
        """
        Gets list of all spaces

        Please provide:
            center_id (str): the unique id of the center
            or
            building_id(str): the unique id of the building

        """
        center_id = None
        building_id = None
        args = request.args.to_dict()
        include = args.get('include')

        if request.args:
            # convert the query parameter from a multidict to a dictionary
            query_dict = request.args.to_dict()
            query_keys = (
                'centerId',
                'buildingId',
                'include',
            )

            center_id = query_dict.get('centerId')
            building_id = query_dict.get('buildingId')
            QueryParser.validate_include_key(query_keys, query_dict)
            SpaceValidator.check_center_id(center_id)
        spaces = SpaceType.query_().all()  # pylint: disable=W0212
        spaces = space_query(spaces, include=include)
        only = ['id', 'type', 'color', 'spaces']
        only = ['id', 'deleted', 'type', 'color', 'spaces'
                ] if include and include == 'deleted' else only
        context = {'center_id': center_id}
        space_type_schema = SpaceTypeSchema(
            many=True, only=only, context=context)

        data = space_type_schema.dump(spaces).data

        if args and include == 'deleted':
            data = space_type_schema.dump(spaces, request_args=args).data

        space_types, grouped_spaces = SpaceTypeSchema.organize_output(data)

        # Check if buildingId filter param is provided. If so, validate it
        # and use it to filter response before returning it
        if building_id:
            SpaceValidator.validate_parent_exists(building_id)
            space_sql_query = sql_queries['get_building_spaces'].format(
                building_id)
            space_types_sql_query = sql_queries['get_space_types']

            # execute the query and get back sqlalchemy result proxy object
            spaces = db.engine.execute(text(space_sql_query))
            space_types = db.engine.execute(text(space_types_sql_query))

            # Mapping dictionary with rows values
            spaces = [dict(row) for row in spaces]
            space_types = [dict(row) for row in space_types]
            grouped_spaces = update_space_type(space_types, spaces)
        return {
            'status': 'success',
            'message': SUCCESS_MESSAGES['fetched'].format('Spaces'),
            'data': grouped_spaces,
            'spaceTypes': space_types
        }


@space_namespace.route('/<string:space_id>')
class SingleSpaceResource(Resource):
    """Resource class for carrying out operations on a single Space"""

    @token_required
    @permission_required(Resources.SPACES)
    @validate_id
    def delete(self, space_id):
        """
        A method for deleting a space

        Arguments:
            space_id (str): the unique id of the space to be deleted

        Raises:
            ValidationError (Exception):
                1. A message showing that the space with the sent id does not exist.
                2. A message showing the space with that id has children and so can not
                   be deleted

        Returns:
            (tuple): returns a status of success and message showing what has been
                    deleted
        """

        try:
            return delete_by_id(Space, space_id, 'Space')
        except ValidationError as error:

            if error.status_code == 404:
                raise error
            raise ValidationError(
                dict(message=database_errors['model_delete_children'].format(
                    "Space", "child space(s)")),
                status_code=403)

    @token_required
    @permission_required(Resources.SPACES)
    @validate_id
    def get(self, space_id):
        """
        Get information on a single space
        :param space_id:
        :returns dict with information on specified space
        """
        included_fields = ['id', 'name', 'parent_id', 'space_type']
        query = request.args.to_dict()
        # validate request query and modify array of fields to filter in schema
        validate_query(query, included_fields)

        space = Space.get_or_404(space_id)
        space_schema = SpaceSchema(only=included_fields)
        return {
            'status': 'success',
            'message': SUCCESS_MESSAGES['fetched'].format('Space'),
            'data': space_schema.dump(space).data
        }

    @token_required
    @permission_required(Resources.SPACES)
    @validate_id
    @validate_json_request
    @space_namespace.expect(space_models)
    def patch(self, space_id):
        """
        An endpoint for updating single space
        """
        request_data = request.get_json()
        request_data['id'] = space_id

        only = [
            'id', 'name', 'parent_id', 'space_type_id', 'space_type',
            'center_id'
        ]
        space_schema = SpaceSchema(only=only)
        space_data = space_schema.load_object_into_schema(
            request_data, partial=True)

        # Validate the data sent and check if it exists
        space = SpaceValidator.validate_space_update(request_data)
        space.update_(**space_data)

        return get_success_responses_for_post_and_patch(
            space,
            space_schema,
            'Space',
            status_code=200,
            message_key='updated')
