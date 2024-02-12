def is_super_user(token_id):
    from api.models import User, Role
    """Checks if the current user is super_super """
    user = User.get_or_404(token_id).role_id
    return Role.get(user).super_user
