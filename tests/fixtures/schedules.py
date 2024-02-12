"""Module with schedules fixtures """

# Third Party Modules
import pytest
import datetime as dt

# Models
from api.models import Schedule, WorkOrder


@pytest.fixture(scope='function')
def new_schedule(app, init_db, new_work_order, new_user):
    """Fixture for creating a new schedule for a work order
    Args:
        app (object): Instance of Flask test app
        init_db (fixture): Fixture to initialize the test database operations.
        new_user (User): Instance of a user
        new_work_order (WorkOrder): Instance of a Work Order

     Returns:
        schedule (Schedule): Object of the created schedule
    """
    new_user.save()
    new_work_order.save()

    schedule = Schedule(
        work_order_id=new_work_order.id,
        assignee_id=new_user.token_id,
        status='done',
        due_date=str(dt.datetime.now() + dt.timedelta(days=5)))

    return schedule


@pytest.fixture(scope='module')
def schedule_list(app, init_db, new_user, new_work_order,
                  new_work_order_with_assigner):
    """Fixture for creating a new schedule
         Args:
            app (object): Instance of Flask test app
            init_db (fixture): Fixture to initialize the test database operations.
            new_user (User): Instance of a user
            new_work_order (WorkOrder): Instance of a Work Order
        Returns:
            schedule(List): List of created schedules
    """

    new_user.save()
    new_work_order.save()

    schedules = [{
        'work_order_id': new_work_order.id,
        'assignee_id': new_user.token_id,
        'created_by': new_user.token_id,
        'status': 'pending',
        'due_date': str(dt.datetime.now() + dt.timedelta(days=5))
    } for x in range(5)]
    return Schedule.bulk_create(schedules)


def create_schedule(new_user, new_work_order, no_of_days, status='pending'):
    """Returns a new schedule object
     Args:
        new_user (User): Instance of a user
        new_work_order (WorkOrder): Instance of a Work Order
        no_of_days (Integer): An Integer specifying number of days to calculate the due_date with
        status (str): Status of the schedule
     Returns:
        schedule (Schedule): Object of the created schedule
    """

    time_due = str(dt.datetime.utcnow() + dt.timedelta(days=no_of_days))

    return Schedule(
        work_order_id=new_work_order.id,
        assignee_id=new_user.token_id,
        status=status,
        due_date=time_due)


@pytest.fixture(scope='module')
def new_schedule(app, init_db, new_work_order, new_user):
    """Fixture for creating a new schedule for a work order
     Args:
        app (object): Instance of Flask test app
        init_db (fixture): Fixture to initialize the test database operations.
        new_user (User): Instance of a user
        new_work_order (WorkOrder): Instance of a Work Order
     Returns:
        new_schedule (Schedule): Object of the created schedule
    """
    new_user.save()
    new_work_order.save()

    return create_schedule(new_user, new_work_order, 5)


@pytest.fixture(scope='module')
def new_test_schedule(app, init_db, new_work_order, new_user):
    """Fixture for creating a new schedule for a work order
     Args:
        app (object): Instance of Flask test app
        init_db (fixture): Fixture to initialize the test database operations.
        new_user (User): Instance of a user
        new_work_order (WorkOrder): Instance of a Work Order
     Returns:
        new_test_schedule (Schedule): Object of the created schedule
    """
    new_user.save()
    new_work_order.save()

    return create_schedule(new_user, new_work_order, 0, 'pending')


@pytest.fixture(scope='function')
def new_schedule_with_assigner(app, init_db, new_work_order_with_assigner,
                               new_user, new_user_two):
    """Fixture for creating a new schedule for a work order
    Args:
        app (object): Instance of Flask test app
        init_db (fixture): Fixture to initialize the test database operations.
        new_user (User): Instance of a user
        new_work_order (WorkOrder): Instance of a Work Order
     Returns:
        schedule (Schedule): Object of the created schedule
    """
    new_user.save()
    new_work_order_with_assigner.save()

    schedule = Schedule(
        work_order_id=new_work_order_with_assigner.id,
        assignee_id=new_user.token_id,
        status='pending',
        created_by=new_user_two.token_id,
        due_date=str(dt.datetime.now() + dt.timedelta(days=5)))

    return schedule


@pytest.fixture(scope='function')
def new_test_schedule_completed(app, init_db, new_work_order_for_schedules,
                                new_user, new_test_user):
    """Fixture for creating a new schedule for a work order
     Args:
        app (object): Instance of Flask test app
        init_db (fixture): Fixture to initialize the test database operations.
        new_user (User): Instance of a user
        new_work_order (WorkOrder): Instance of a Work Order
     Returns:
        schedule (Schedule): Object of the created schedule
    """
    new_test_user.save()
    new_user.save()
    new_work_order_for_schedules.save()
    time_due = str(dt.datetime.now() + dt.timedelta(days=20))
    schedule_details = {
        "created_by": new_test_user.token_id,
        "work_order_id": new_work_order_for_schedules.id,
        "assignee_id": new_user.token_id,
        "status": "pending",
        "due_date": time_due
    }
    return Schedule(**schedule_details)
