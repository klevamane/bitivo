"""Module for token validation"""

# Standard library
from functools import wraps
from base64 import b64decode

# Third party
from flask import request
import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# Utilities
from api.utilities.constants import CHARSET
from api.utilities.messages.error_messages import jwt_errors

# app config
from config import AppConfig


def get_token(http_request=request):
    """Get token from request object

    Args:
        http_request (HTTPRequest): Http request object

    Returns:
        token (string): Token string

    Raises:
        ValidationError: Validation error raised when there is no token
                         or bearer keyword in authorization header
    """
    from .base_validator import ValidationError
    token = http_request.headers.get('Authorization')
    if not token:
        raise ValidationError({'message': jwt_errors['NO_TOKEN_MSG']}, 401)
    elif 'bearer' not in token.lower():
        raise ValidationError({'message': jwt_errors['NO_BEARER_MSG']}, 401)
    token = token.split(' ')[-1]
    return token


def token_required(func):
    """Authentication decorator. Validates token from the client

    Args:
        func (function): Function to be decorated

    Returns:
        function: Decorated function

    Raises:
        ValidationError: Validation error
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        from .base_validator import ValidationError

        token = get_token()
        try:
            flask_env = AppConfig.FLASK_ENV
            public_key_64 = AppConfig.JWT_PUBLIC_KEY
            decode_public_key_64 = lambda key_64: b64decode(key_64).decode(CHARSET)
            decode_public_key_64_test = lambda key_64: serialization.load_pem_public_key(
                key_64.encode(), backend=default_backend())
            public_key_mapper = {
                'testing': decode_public_key_64_test,
                'production': decode_public_key_64
            }
            public_key = public_key_mapper.get(
                flask_env, decode_public_key_64)(public_key_64)

            decoded_token = jwt.decode(
                token,
                public_key,
                algorithms=['RS256'],
                options={
                    'verify_signature': True,
                    'verify_exp': True
                })
        except jwt.exceptions.InvalidAudienceError:
            decoded_token = jwt.decode(
                token,
                public_key,
                algorithms=['RS256'],
                audience='andela.com',
                issuer="accounts.andela.com",
                options={
                    'verify_signature': True,
                    'verify_exp': True
                })
        except (
                ValueError,
                TypeError,
                jwt.ExpiredSignatureError,
                jwt.DecodeError,
                jwt.InvalidSignatureError,
                jwt.InvalidAlgorithmError,
                jwt.InvalidIssuerError,
        ) as error:
            exception_mapper = {
                ValueError: (jwt_errors['SERVER_ERROR_MESSAGE'], 500),
                TypeError: (jwt_errors['SERVER_ERROR_MESSAGE'], 500),
                jwt.ExpiredSignatureError: (jwt_errors['EXPIRED_TOKEN_MSG'],
                                            401),
                jwt.DecodeError: (jwt_errors['INVALID_TOKEN_MSG'], 401),
                jwt.InvalidIssuerError: (jwt_errors['ISSUER_ERROR'], 401),
                jwt.InvalidAlgorithmError: (jwt_errors['ALGORITHM_ERROR'],
                                            401),
                jwt.InvalidSignatureError: (jwt_errors['SIGNATURE_ERROR'], 500)
            }
            message, status_code = exception_mapper.get(
                type(error), (jwt_errors['SERVER_ERROR_MESSAGE'], 500))
            raise ValidationError({'message': message}, status_code)

        # setting the payload to the request object and can be accessed with \
        # request.decoded_token from the view
        setattr(request, 'decoded_token', decoded_token)
        return func(*args, **kwargs)

    return decorated_function
