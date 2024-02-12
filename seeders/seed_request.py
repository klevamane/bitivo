# Models
from api.models import Center, User, RequestType, Request

# Utilities
from api.utilities.json_parse_objects import json_parse_objects

# App config
from config import AppConfig

ATTACHMENTS = [{
    "url": "https://somerandomimage.com/image.jpg"
}, {
    "url": "https://somerandomimage.com/image.jpg"
}, {
    "url": "https://somerandomimage.com/image.jpg"
}]


def seed_request(clean_data=False):
    """ Seeds multiple requests into the database

    Args:
        clean_data (bool): Determines if seed data is to be cleaned.

    Returns:
        None
    """
    # If in production and clean_data is False, do not seed
    if AppConfig.FLASK_ENV in ('production', 'staging') and not clean_data:
        return

    # Centers
    center_one = Center.query_()[0]
    center_two = Center.query_()[1]
    center_three = Center.query_()[2]
    # Users
    user_one = User.query_()[0]
    user_two = User.query_()[1]
    user_three = User.query_()[2]

    # regular users
    regular_user_one = User.query.filter_by(
        email="yahya.hussei@andela.com").first()
    regular_user_two = User.query.filter_by(
        email="grace.zawad@andela.com").first()
    regular_user_three = User.query.filter_by(
        email="arnold.osor@andela.com").first()
    # RequestTypes
    request_type_one = RequestType.query_()[0]
    request_type_two = RequestType.query_()[1]
    request_type_three = RequestType.query_()[2]

    requests_data = [
        create_request_data(
            title='My iPhone Screen',
            center=center_one,
            request_type=request_type_one,
            description=
            'The iphone screen cracked when it fell and needs fixing',
            requester=user_one,
            responder=request_type_one.assignee_id,
            assignee=user_two),
        create_request_data(
            title='Macbook is hot',
            center=center_two,
            request_type=request_type_two,
            description='The Macbook just keeps getting hot unexplainably',
            requester=user_two,
            responder=request_type_two.assignee_id,
            assignee=user_two),
        create_request_data(
            title='Dongle is missing',
            center=center_three,
            request_type=request_type_three,
            description=
            "Left the dongle at work yesterday and I can't find it again",
            requester=user_three,
            responder=request_type_three.assignee_id,
            assignee=user_two),
        create_request_data(
            title='My Laptop Screen',
            center=center_one,
            request_type=request_type_one,
            description='My laptop screen fell',
            requester=regular_user_one,
            responder=request_type_one.assignee_id,
            assignee=user_two),
        create_request_data(
            title='Macbook keyboad',
            center=center_two,
            request_type=request_type_two,
            description='Some keys are not working',
            requester=regular_user_two,
            responder=request_type_two.assignee_id,
            assignee=user_two),
        create_request_data(
            title='Screen saver',
            center=center_three,
            request_type=request_type_three,
            description="Screen seams not to change this days",
            requester=regular_user_three,
            responder=request_type_three.assignee_id,
            assignee=user_two),
    ]
    Request.bulk_create(requests_data)


def create_request_data(**kwargs):
    """ Creates a dict for a request
        Args:
            kwargs (dict): arguments of data needed to created the request
        Returns:
            dict: A dictionary of a request
    """
    json_dumped_attachments = json_parse_objects(ATTACHMENTS)

    return {
        "subject": kwargs['title'],
        "request_type_id": kwargs['request_type'].id,
        "center_id": kwargs['center'].id,
        "description": kwargs['description'],
        "attachments": json_dumped_attachments,
        "requester_id": kwargs['requester'].token_id,
        "responder_id": kwargs['responder'],
        "assignee_id": kwargs['assignee'].token_id,
    }
