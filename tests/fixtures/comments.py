"""Module with comments fixtures """

# Third Party Modules
import pytest
from faker import Faker

# Models
from api.models import Comment
from unittest.mock import Mock

# tasks
from api.tasks.notifications.comment import CommentNotifications, SendEmail

# utilities
from api.utilities.emails.email_factories.concrete_sendgrid import \
    ConcreteSendGridEmail

from api.utilities.enums import ParentType

fake = Faker()


@pytest.fixture(scope='module')
def new_comment(app, init_db, new_user, new_request):
    """Fixture for creating a new request
         Args:
            app (object): Instance of Flask test app
            init_db (fixture): Fixture to initialize the test database operations.
            new_user (User): Fxiture for creating a user
            new_request (Request): Fixture for creating a request
         Returns:
            comment (Comment): Comment object
    """
    new_user.save()
    new_request.save()
    comment = Comment(
        body=fake.sentence(),
        parent_id=new_request.id,
        author_id=new_user.token_id,
        created_by=new_user.token_id)
    return comment


@pytest.fixture(scope='module')
def new_comment_user_two(app, init_db, second_user, new_request):
    """Fixture for creating a second comment on request
         Args:
            app (object): Instance of Flask test app
            init_db (fixture): Fixture to initialize the test database operations.
            new_user_for_comment (User): Fxiture for creating a user

    """
    second_user.save()
    new_request.save()
    comment = Comment(
        body=fake.sentence(),
        parent_id=new_request.id,
        author_id=second_user.token_id)

    return comment


@pytest.fixture(scope='module')
def delete_comment(app, init_db, new_user, new_request):
    """Fixture for creating a new soft deleted comment

         Args:
            app (object): Instance of Flask test app
            init_db (fixture): Fixture to initialize the test database operations.
            new_user (User): Fxiture for creating a user
            new_request (Request): Fixture for creating a request
         Returns:
            comment (Comment): Comment object
    """
    new_user.save()
    new_request.save()
    comment = Comment(
        body=fake.sentence(),
        parent_id=new_request.id,
        author_id=new_user.token_id,
        deleted=True)
    return comment


@pytest.fixture(scope='module')
def new_comment2(app, init_db, new_user_two, new_request):
    """Fixture for creating a new comment

         Args:
            app (object): Instance of Flask test app
            init_db (fixture): Fixture to initialize the test database operations.
            new_user_two (User): Fxiture for creating a user

            new_request (Request): Fixture for creating a request
         Returns:
            comment (Comment): Comment object
    """
    new_user_two.save()
    new_request.save()
    comment = Comment(
        body=fake.sentence(),
        parent_id=new_request.id,
        author_id=new_user_two.token_id)

    return comment


@pytest.fixture(scope='module')
def new_schedule_comment(app, init_db, new_user, new_schedule):
    """Fixture for creating a new schedule comment
         Args:
            app (object): Instance of Flask test app
            init_db (fixture): Fixture to initialize the test database operations.
            new_user (User): Fixture for creating a user
            new_schedule (Schedule): Fixture for creating a schedule
         Returns:
            comment (Comment): Comment object
    """
    new_user.save()
    new_schedule.save()
    comment = Comment(
        body=fake.sentence(),
        parent_id=new_schedule.id,
        author_id=new_user.token_id,
        parent_type=ParentType.Schedule)
    return comment
