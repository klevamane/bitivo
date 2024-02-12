"""Module for users resource"""
# Third-party libraries
from flask_restplus import Resource
from flask import request

# Validators
from ..utilities.validators.user_validator import UserValidator
from ..utilities.validators.validate_query_param_values \
    import validate_query_param_values

# Models
from ..models import User

# Schemas
from ..schemas.user import UserSchema

# Decorators
from ..middlewares.token_required import token_required
from ..utilities.validators.validate_id import validate_id
from ..utilities.validators.validate_json_request import validate_json_request

# Messages
from ..utilities.messages.success_messages import SUCCESS_MESSAGES

# Helpers
from ..utilities.helpers.endpoint_response \
    import get_success_responses_for_post_and_patch
from api.utilities.error import raises
from api.utilities.helpers.pagination_conditional \
    import should_resource_paginate

# Constants
from ..utilities.constants import EXCLUDED_FIELDS
# Resources
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required

# Documentation
from api.utilities.swagger.collections.user import user_namespace
from api.utilities.swagger.swagger_models.user import user_model
from api.utilities.swagger.constants import USER_REQUEST_PARAMS, SINGLE_USER_REQUEST_PARAMS

USER_SCHEMA = UserSchema(exclude=['deleted'])


@user_namespace.route('/<string:token_id>')
class UserResource(Resource):
    """Resource class for users"""

    @staticmethod
    def _return_or_create(token_id):
        new_user = request.decoded_token['UserInfo'].copy()
        new_user['tokenId'] = new_user['id']
        new_user['imageUrl'] = new_user['picture']

        # Deserialize, validate response data
        user_data = USER_SCHEMA.load_object_into_schema(new_user)

        # check if user already exist or add the new user data to the database
        return User.find_or_create(user_data, token_id=token_id)

    @token_required
    @permission_required(Resources.PEOPLE)
    @validate_id
    def delete(self, token_id):
        """Delete a user"""

        person = User.get_or_404(token_id)
        person.delete()

        return {
            'status': 'success',
            'message': SUCCESS_MESSAGES['deleted'].format(person.name)
        }

    @token_required
    @permission_required(Resources.PEOPLE)
    @validate_json_request
    @validate_id
    @user_namespace.expect(user_model)
    def patch(self, token_id):
        """
        PATCH method for editing a user

        Parameters:
             token_id(str): token id of person editing

        Returns:
            response(dict): dict containing status, message and
            updated data if successful
        """

        request_data = request.get_json()
        user_data = USER_SCHEMA.load_object_into_schema(
            request_data, partial=True)
        person = User.get_or_404(token_id)
        person.update_(**user_data)
        return {
            'status': 'success',
            'message': SUCCESS_MESSAGES['person_updated'].format(person.name),
            'data': USER_SCHEMA.dump(person).data
        }

    @token_required
    @validate_id
    @user_namespace.doc(params=SINGLE_USER_REQUEST_PARAMS)
    def get(self, token_id):
        """Get a user's details.

        Args:
            self (Instance): Instance of UserResource class.
            token_id (str): String containing a user's token ID.

        Returns:
            dict: Dictionary containing corresponding response, ie. status,
                 message and data.
        """

        excluded_user_attributes = [
            'deleted', 'center.user_count', 'role.resource_access_levels',
            'created_at', 'updated_at'
        ]
        excluded_user_attributes.extend(EXCLUDED_FIELDS)

        user = User.get(token_id)

        if request.args:
            query_keys = (
                'include',
                'provisionUser',
            )
            UserValidator.check_query_valid(query_keys, request.args,
                                            excluded_user_attributes)
            validate_query_param_values(request.args, ['true'],
                                        'provisionUser')

            if not user and request.args.to_dict()['provisionUser']:
                user = UserResource._return_or_create(token_id)

        if not user:
            raises('not_found', 404, 'User')

        user_schema = UserSchema(exclude=excluded_user_attributes)

        return {
            'status': 'success',
            'message': SUCCESS_MESSAGES['fetched'].format('User'),
            'data': user_schema.dump(user).data
        }


@user_namespace.route('/')
class AddUserResource(Resource):
    """Resource class for adding"""

    @token_required
    @validate_json_request
    @user_namespace.expect(user_model)
    def post(self):
        """Add a user to a center

        Raises:
            ValidationError: Used to raise exception if validation of email,
            role or center fails

        Returns:
            (dict): Returns status, success message and relevant user details
        """

        request_data = request.get_json()
        token_id = request_data.get('tokenId')

        message_key = 'added_to_center' if request_data.get(
            'centerId', None) else 'created'

        # Deserialize, validate response data
        user_data = USER_SCHEMA.load_object_into_schema(request_data)

        # check if user already exist or add the new user data to the database
        user = User.find_or_create(user_data, token_id=token_id)

        return get_success_responses_for_post_and_patch(
            user,
            USER_SCHEMA,
            user.name,
            getattr(user.center, 'name', ''),
            status_code=201,
            message_key=message_key)

    @token_required
    @user_namespace.doc(params=USER_REQUEST_PARAMS)
    def get(self):
        """
        Gets list of people filtered by search query
        """
        excluded_fields = EXCLUDED_FIELDS.copy()
        query_dict = request.args.to_dict()
        user_schema = UserSchema(many=True, exclude=excluded_fields)
        if ('pagination' in query_dict
                and query_dict['pagination'].lower() == 'false'):
            from api.models.database import db
            from sqlalchemy import text
            query = db.engine.execute(
                text('SELECT * FROM users where deleted = false')).fetchall()
            return {
                "status": 'success',
                "message": SUCCESS_MESSAGES['fetched'].format('Users'),
                "data": user_schema.dump(query).data,
                "meta": None
            }
        data, meta = should_resource_paginate(request, User, UserSchema)
        return {
            "status": 'success',
            "message": SUCCESS_MESSAGES['fetched'].format('Users'),
            "data": data,
            "meta": meta
        }


@user_namespace.route('/migrate')
class UserMigrationResource(Resource):
    """Resource class for migrating people data into activo"""

    @token_required
    def post(self):
        """POST method for updating activo user table with andela personnel
        records

        Returns:
            tuple: Success response with 200 status code
        """
        from ..tasks.migration import Migrations

        requester = request.decoded_token['UserInfo']
        headers = {'Authorization': request.headers.get('Authorization')}

        Migrations.migrate_users.delay(requester, headers)
        return {
            'status': 'success',
            'message': SUCCESS_MESSAGES['migrated'].format('Users')
        }, 200
