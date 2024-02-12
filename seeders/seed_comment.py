""" Module for seeding comments for development."""

# Standard Library
import random

#Third party
from faker import Faker

# Models
from api.models import Request, Comment, User

# App config
from config import AppConfig


def seed_comments(clean_data=False):
    """ Seeder for the comments table.
     Args:
        clean_data (bool): Determines if seed data is to be cleaned.
     Returns:
        None
    """
    if AppConfig.FLASK_ENV in ('production', 'staging') and not clean_data:
        return
    requests = Request.query_().all()
    users = User.query_().all()
    fake = Faker()
    comments = [{
        'parent_id': request.id,
        'body': fake.sentence(),
        'author_id': random.choice(users).token_id
    } for request in requests]
    Comment.bulk_create(comments)
