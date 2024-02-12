from functools import wraps

from flask import request

from api.middlewares.base_validator import ValidationError
from api.utilities.messages.error_messages.authorization_errors import error_dict
from api.utilities.helpers.check_user_role import is_super_user


class BasePolicy(object):
    @staticmethod
    def get_user_id():
        """Get the token id of the current user """
        token_id = request.decoded_token.get('UserInfo').get('id')
        return token_id

    @classmethod
    def delete_update_action(cls):
        """
        Decorator. Validates the user allowed to update and delete.
        Args:
            func (function): Function to be decorated
            Returns:
            function: Decorated function
        Raises:
            ValidationError: Validation error when user is not authorized
            to update or delete
        """

        def decorator(func):
            @wraps(func)
            def decorated_function(*args, **kwargs):
                model_instance = args[0]
                request_type = request.method.lower()
                token_id = BasePolicy.get_user_id()
                if is_super_user(token_id):
                    return func(*args, **kwargs)
                BasePolicy.check_request_type(request_type, model_instance)
                return func(*args, **kwargs)

            return decorated_function

        return decorator

    @staticmethod
    def check_request_type(request_type, model_instance):
        """
        Check the request type.
        Args:
            request_type (str): request type
            model_instance (obj): instance of the target model
            Returns:
            function: Decorated function
        Return:
            None
        """
        if request_type == 'patch' or request_type == 'delete':
            BasePolicy.check_policy(request_type, model_instance,
                                    'make changes to this')

    @staticmethod
    def check_policy(request_type, model_instance, message):
        """
        Checks the models policy .
        Args:
        request_type: type of request either patch or delete
        model_instance: the particular model to which the request is being made
        message: respose to user
        Raises:
        ValidationError: Validation error when policy check fails
        """
        allow = False
        policy = model_instance.policies.get(request_type, None)
        if policy == 'owner' and model_instance.created_by == BasePolicy.get_user_id(
        ) or policy is None:
            allow = True
        if not allow:
            raise ValidationError({
                'message':
                error_dict['permissions_error'].format(
                    message,
                    type(model_instance).__name__)
            }, 403)
