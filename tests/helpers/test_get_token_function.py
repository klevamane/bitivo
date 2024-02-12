"""
Module of tests for get token available function
"""

#pytest
from pytest import raises

# utilities
from api.middlewares.token_required import get_token
from api.middlewares.base_validator import ValidationError

# mocks
from tests.mocks.request import Request

# error messages
from api.utilities.messages.error_messages import jwt_errors


class TestGetToken:
    """Tests for get-token function"""

    def test_returns_the_token(self):
        """Should return token"""
        token_mock = 'token'
        request_mock = Request({'Authorization': f'bearer {token_mock}'})
        token = get_token(request_mock)
        assert token == token_mock

    def test_get_token_available_without_token_fails(self):
        """Should fail with no token"""
        request_mock = Request({})
        with raises(ValidationError) as error:
            get_token(request_mock)
        assert error.value.error['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_get_token_available_when_a_token_does_not_contain_bearer_fails(
            self):
        """Should fail with no keyword bearer in the authorization header"""
        request_mock = Request({'Authorization': 'token'})
        with raises(ValidationError) as error:
            get_token(request_mock)
        assert error.value.error['message'] == jwt_errors['NO_BEARER_MSG']
