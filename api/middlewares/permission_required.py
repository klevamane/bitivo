"""Module for permission validation"""

# System imports
from functools import wraps

# Third party
from flask import request

# Errors
from .base_validator import ValidationError

# Utilities
from ..utilities.constants import PERMISSION_TYPES
from ..utilities.helpers.permissions import check_user_permissions
# Messages
from ..utilities.messages.error_messages import authorization_errors
from ..utilities.helpers.check_user_role import is_super_user


class Resources:
    """ Resources constants """
    ASSETS = 'Assets'
    CENTERS = 'Centers'
    PEOPLE = 'People'
    PERMISSIONS = 'Permissions'
    ASSET_CATEGORIES = 'Asset Categories'
    SPACES = 'Spaces'
    ROLES = 'Roles'
    STOCK_COUNT = 'Stock Count'
    HISTORY = 'History'
    REQUESTS = 'Requests'
    REQUEST_TYPES = 'Request Types'
    COMMENTS = "Comments"
    HOT_DESKS = "Hot Desks"
    MAINTENANCE_CATEGORIES = "Maintenance Categories"
    SCHEDULES = "Schedules"
    WORK_ORDERS = "Work Orders"


def permission_required(resource_name):
    """
    Permission required decorator determines if a given user has permission

    Args:
        resource_name (string): resource name 

    Returns:
        decorator (function): decorated function

    Raises:
        ValidationError: is raised if user has permissions on a resource
    """

    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            token_id = request.decoded_token.get('UserInfo').get('id')
            action = PERMISSION_TYPES.get(request.method)
            has_permission = check_user_permissions(token_id, resource_name,
                                                    action)
            if is_super_user(token_id) or has_permission:
                return func(*args, **kwargs)
            raise ValidationError({
                'message':
                authorization_errors['permissions_error'].format(
                    action.lower(), resource_name.lower())
            }, 403)

        return decorated_function

    return decorator


def is_center_centric(func):
    """Makes data center centric
        Args:
            func (function): A function to be decorated
        Returns:
            decorator (function): decorated function
    """

    @wraps(func)
    def decorated_function(*args):
        if hasattr(args[0], 'center_id'):
            from api.models import User
            if request and request.decoded_token:
                token_id = request.decoded_token['UserInfo']['id']
                if is_super_user(token_id):
                    return args[1]  # returns query object
                user = User.get_or_404(token_id)
                center_id = user.center_id
                return func(*args, center_id)
            return args[1]
        return args[1]

    return decorated_function
