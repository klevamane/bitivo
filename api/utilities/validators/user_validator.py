"""Module for handling user resource validations"""

# Third party
from marshmallow import ValidationError as MarshValidationError

# Middleware
from api.middlewares.base_validator import ValidationError

# Models
from api.models import Role, Center, User

# Utilities
from api.utilities.error import raises
from api.utilities.query_parser import QueryParser
from api.utilities.string_converter import snake_case_to_title_case

# Error messages
from ..messages.error_messages import serialization_errors


class UserValidator:
    """Validate user details"""

    @classmethod
    def validate(cls, data):
        """Validate user fields against database"""
        if len(data) < 1:
            raise MarshValidationError(serialization_errors['not_provided'])
        resources = [(data.get('role_id'), Role),
                     (data.get('center_id'), Center)]

        for item_id, model in resources:
            if item_id:
                # get user, center or role or raise 404 error
                model.get_or_404(item_id)

        cls.validate_email_and_token_id_unique(data)

    @classmethod
    def validate_email_and_token_id_unique(cls, data):
        """
        Check that email does not already exist in the database

        Parameters:
            data(dict): the request data
        """
        email = data.get('email')
        if email:
            token_id = data.get('token_id')
            unique_mapper = {"email": email, "token_id": token_id}
            for key, value in unique_mapper.items():
                cls.check_user(**{key: value})
            return

    @classmethod
    def check_user(cls, **kwargs):
        """Check if user exists by checking the email and then token id.

        Args:
            kwargs(dict): keyword arguments containing fields to filter query by

        Raises:
            (ValidationError): Used to raise exception if invalid query is
                   made.
        """

        column = list(kwargs.keys())[0]
        user = User.query.include_deleted().filter_by(**kwargs).first()
        if user:
            if user.deleted:
                raises('archived', 409, f'{snake_case_to_title_case(column)}')
            raises('exists', 409, f'{snake_case_to_title_case(column)}')

    @classmethod
    def check_included_query_exists(cls, query_value,
                                    excluded_user_attributes):
        """Check if 'include' key value valid.

        Args:
            query_value (str): string holding the value of the 'include' key.
            excluded_user_attributes (list): List containing all columns to be
                                            excluded by schema.
        Raises:
            (ValidationError): Used to raise exception if invalid query is
                   passed to the 'include' key in the request query.
        """
        include_values = {
            'permissions': 'role.resource_access_levels',
        }
        if query_value is not None and query_value.lower(
        ) not in include_values:
            raise ValidationError({
                'message':
                serialization_errors['invalid_query_strings'].format(
                    'include', query_value)
            }, 400)
        # Remove the query_value from the RoleSchema excluded values
        excluded_user_attributes.remove(include_values[query_value])

    @classmethod
    def check_query_valid(cls, query_keys, request_args, excluded_attributes):
        """Check if url query key-value pair are valid.

        Args:
            cls (Class): UserValidator class.
            query_keys (tuple): tuple containing allowable 'include' query
                                key values.
            request_args (dict): immutableMultiDict holding all query data.
            excluded_attributes (list): List containing all columns to be
                                        excluded by schema.
        """

        QueryParser.validate_include_key(query_keys, request_args)
        if request_args.get('include'):
            cls.check_included_query_exists(
                request_args.get('include').lower(), excluded_attributes)
