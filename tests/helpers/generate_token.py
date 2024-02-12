"""Module for token generation"""

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from config import AppConfig
from ..mocks.user import user_one, user_two, user_three
from api.utilities.constants import CHARSET
from api.models import User
from api.schemas.user import UserSchema
from api.utilities.constants import EXCLUDED_FIELDS


def generate_token(exp=None, token_id=None):
    """
    Generates jwt tokens for testing purpose
    params:
        exp: Token Expiration. This could be datetime object or an integer
    result:
        token: This is the bearer token in this format 'Bearer token'
    """

    if token_id:
        excluded = EXCLUDED_FIELDS
        excluded.extend(['center', 'created_at', 'updated_at'])
        user_obj = User.get_or_404(token_id)
        user_data = UserSchema(exclude=excluded).dump(user_obj).data
        user_data['id'] = token_id
        user = user_data
    else:
        user_one_data = user_one.to_dict()
        user_one_data['picture'] = 'https://someimage.url'
        user = user_one_data

    secret_key_text = AppConfig.JWT_SECRET_KEY
    secret_key = serialization.load_pem_private_key(
        secret_key_text.encode(), password=None, backend=default_backend())
    payload = {'UserInfo': user}
    payload.__setitem__('exp', exp) if exp is not None else ''
    token = jwt.encode(payload, secret_key, algorithm='RS256').decode(CHARSET)
    return 'Bearer {0}'.format(token)
