"""Module with authorization fixtures """

# Third Party Modules
import pytest
from flask import current_app, request

# Models
from api.models import Schedule

# Utilities
from tests.helpers.generate_token import generate_token
from api.utilities.constants import MIMETYPE, MIMETYPE_TEXT, MIMETYPE_FORM_DATA


@pytest.fixture(scope='module')
def auth_header(generate_token=generate_token):
    return {
        'Authorization': generate_token(),
        'Content-Type': MIMETYPE,
        'Accept': MIMETYPE
    }


@pytest.fixture(scope='module')
def auth_header_text(generate_token=generate_token):
    return {
        'Authorization': generate_token(),
        'Content-Type': MIMETYPE_TEXT,
        'Accept': MIMETYPE_TEXT
    }


@pytest.fixture(scope='module')
def auth_header_form_data(generate_token=generate_token):
    return {
        'Authorization': generate_token(),
        'Content-Type': MIMETYPE_FORM_DATA,
        'Accept': MIMETYPE_FORM_DATA
    }


@pytest.fixture(scope='module')
def mock_request_obj_decoded_token():
    """
    Mock decoded_token from request object
    """
    decoded_token = setattr(
        request, 'decoded_token',
        {'UserInfo': {
            'name': 'Ayobami',
            'id': '-Lsdi97y6uyeABD5S'
        }})

    return decoded_token


@pytest.fixture(scope='module')
def mock_request_two_obj_decoded_token(new_user, request_ctx):
    """
    Mock decoded_token from request object for new_user
    """
    decoded_token = setattr(
        request, 'decoded_token',
        {'UserInfo': {
            'name': 'Ayobami22',
            'id': new_user.token_id
        }})

    return decoded_token


@pytest.fixture(scope='module')
def mock_request_three_obj_decoded_token(new_user_three):
    """
    Mock decoded_token from request object for new_user_three
    """
    decoded_token = setattr(
        request, 'decoded_token',
        {'UserInfo': {
            'name': 'Ayobami',
            'id': new_user_three.token_id
        }})

    return decoded_token


@pytest.fixture(scope='module')
def mock_request_four_obj_decoded_token(new_user_two, request_ctx):
    """
    Mock decoded_token from request object for new_user_three
    """
    decoded_token = setattr(
        request, 'decoded_token',
        {'UserInfo': {
            'name': 'Ayobami',
            'id': new_user_two.token_id
        }})

    return decoded_token


@pytest.fixture(scope='module')
def mock_request_five_obj_decoded_token(new_user_two, request_ctx):
    """
    Mock decoded_token from request object for new_user_three
    """
    decoded_token = setattr(
        request, 'decoded_token',
        {'UserInfo': {
            'name': 'Ayobami2',
            'id': new_user_two.token_id
        }})

    return decoded_token


@pytest.fixture(scope='module')
def mock_request_six_obj_decoded_token(test_user, request_ctx):
    """
    Mock decoded_token from request object for test_user
    """
    decoded_token = setattr(
        request, 'decoded_token',
        {'UserInfo': {
            'name': 'Dave',
            'id': test_user.token_id
        }})

    return decoded_token


@pytest.fixture(scope='module')
def auth_header_two(init_db, new_user, request_ctx, mock_request_obj_decoded_token):
    """
    Mock decoded_token from request object for new_user_three
    """
    new_user.save()
    setattr(
        request, 'decoded_token',
        {'UserInfo': {
            'name': new_user.name,
            'id': new_user.token_id
        }})
    return {
        'Authorization': generate_token(token_id=new_user.token_id),
        'Content-Type': MIMETYPE,
        'Accept': MIMETYPE
    }

@pytest.fixture(scope='module')
def auth_header_three(init_db, test_user, request_ctx, mock_request_obj_decoded_token):
    """
    Mock decoded_token from request object for test_user_three
    """
    test_user.save()
    setattr(
        request, 'decoded_token',
        {'UserInfo': {
            'name': test_user.name,
            'id': test_user.token_id
        }})
    return {
        'Authorization': generate_token(token_id=test_user.token_id),
        'Content-Type': MIMETYPE,
        'Accept': MIMETYPE
    }
