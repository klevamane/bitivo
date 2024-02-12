"""Module with work orders fixtures """

# Third Party Modules
import pytest

# Database
from api.models.database import db

# Models
from api.models import WorkOrder


@pytest.fixture(scope='module')
def new_work_order(app, init_db, new_maintenance_category, new_user):
    new_maintenance_category.save()
    new_user.save()

    details = {
        'title': 'Fuel Level',
        'description': 'change the fuel of the car',
        'maintenance_category_id': new_maintenance_category.id,
        'assignee_id': new_user.token_id,
        'frequency': 'weekly',
        'status': 'enabled',
        'start_date': '2018-12-12 00:00:00',
        'end_date': '2019-02-1 00:00:00',
        'created_by': new_user.token_id,
    }
    return WorkOrder(**details)


@pytest.fixture(scope='module')
def work_order_with_invalid_assignee_id(app, init_db,
                                        new_maintenance_category):
    db.session.rollback()
    new_maintenance_category.save()

    details = {
        'title': 'Fuel Level',
        'description': 'change the fuel of the car',
        'maintenance_category_id': new_maintenance_category.id,
        'assignee_id': '-L757573939',
        'frequency': 'weekly',
        'status': 'enabled',
        'start_date': '2018-12-12 00:00:00',
        'end_date': '2019-02-1 00:00:00',
    }
    return WorkOrder(**details)


@pytest.fixture(scope='module')
def work_order_with_invalid_maintenance_category_id(app, init_db, new_user):
    db.session.rollback()

    details = {
        'title': 'Fuel Level',
        'description': 'change the fuel of the car',
        'maintenance_category_id': '-L757573939-90',
        'assignee_id': new_user.token_id,
        'frequency': 'weekly',
        'status': 'enabled',
        'start_date': '2018-12-12 00:00:00',
        'end_date': '2019-02-1 00:00:00',
    }
    return WorkOrder(**details)


@pytest.fixture(scope='module')
def work_order_with_missing_fields(app, init_db):
    db.session.rollback()

    details = {
        'description': 'change the fuel of the car',
        'maintenance_category_id': '-L757573939-90',
        'frequency': 'weekly',
        'start_date': '2018-12-12 00:00:00',
        'end_date': '2019-02-1 00:00:00',
    }
    return WorkOrder(**details)


@pytest.fixture(scope='module')
def new_work_order_duplicate(app, init_db, new_user, new_maintenance_category):
    """Fixture for creating a new work order to prevent duplicate in
    the same center

    Args:
        app (object): Instance of Flask test app
        init_db (fixture): Fixture to initialize the test database operations.
        new_user (User): Instance of a user
        new_maintenance_category (Maintenance Category): Instance of an Maintenance Category

    Returns:
        request (dic): Dictionary of the created work order
    """

    new_user.save()
    new_maintenance_category.save()
    return WorkOrder(
        title='work order 2',
        description='A very long description',
        frequency='daily',
        status='enabled',
        assignee_id=new_user.token_id,
        maintenance_category_id=new_maintenance_category.id,
        start_date='2011-08-12 00:00:00',
        end_date='2019-08-12 00:00:00')


@pytest.fixture(scope='module')
def new_work_order_with_assignee_in_center(app, new_user,
                                           new_maintenance_category):
    new_user.save()
    new_maintenance_category.save()
    return WorkOrder(
        title='Test Work Order',
        description='A very long description',
        frequency='daily',
        status='enabled',
        assignee_id=new_user.token_id,
        maintenance_category_id=new_maintenance_category.id,
        start_date='2011-08-12 00:00:00',
        end_date='2019-08-12 00:00:00',
        created_by=new_user.token_id)


@pytest.fixture(scope='function')
def updated_work_order(app, new_user, new_maintenance_category):
    """Fixture for creating an updated work order
    Args:
        app (obj): Instance of Flask test app
        new_user (obj): Instance of a user
        new_maintenance_category(obj): Instance of an Maintenance Category
    Returns:
        work order (dict): Dictionary of the created updated work order
    """
    new_user.save()
    new_maintenance_category.save()
    return WorkOrder(
        title='updated work order',
        description='A very long description',
        frequency='daily',
        status='enabled',
        assignee_id=new_user.token_id,
        maintenance_category_id=new_maintenance_category.id,
        start_date='2011-08-12 00:00:00',
        end_date='2019-08-12 00:00:00',
        created_by=new_user.token_id,
        updated_by=new_user.token_id)


@pytest.fixture(scope='function')
def new_work_order_for_schedules(app, new_maintenance_category, new_user):
    """Fixture for creating an no repeat work order
        Args:
            app (obj): Instance of Flask test app
            new_maintenance_category(obj): Instance of an Maintenance Category
            new_user (obj): Instance of a user
        Returns:
            work order (object): Object of the non created  work order
    """
    new_maintenance_category.save()
    new_user.save()

    details = {
        'title': 'Fuel Level',
        'description': 'change the fuel of the car',
        'maintenance_category_id': new_maintenance_category.id,
        'assignee_id': new_user.token_id,
        'start_date': '2018-12-12 00:00:00',
        'end_date': '2019-02-1 00:00:00',
        'frequency': 'no_repeat'
    }
    return WorkOrder(**details)


@pytest.fixture(scope='module')
def new_work_order_with_assigner(app, init_db, new_maintenance_category,
                                 new_user, new_user_two):
    """
        Fixture for creating a work order with assigner

           Args:
               app (obj): Instance of Flask test app
               new_maintenance_category(obj): Instance of an Maintenance Category
               new_user (obj): Instance of a user
               new_user_two (obj): Instance of user two
           Returns:
             work order (object): Object of the  created  work order

    """

    new_maintenance_category.save()
    new_user.save()
    new_user_two.save()

    details = {
        'title': 'Fuel Level',
        'description': 'change the fuel of the car',
        'maintenance_category_id': new_maintenance_category.id,
        'assignee_id': new_user.token_id,
        'created_by': new_user_two.token_id,
        'frequency': 'weekly',
        'status': 'enabled',
        'start_date': '2018-12-12 00:00:00',
        'end_date': '2019-02-1 00:00:00',
        'created_by': new_user_two.token_id
    }
    return WorkOrder(**details)


@pytest.fixture(scope='module')
def new_work_order_with_assignee_not_in_center(
        app, new_user, new_maintenance_category, new_center,
        new_work_order_user):
    """Fixture for creating a new work order with different center
     Args:
        app (object): Instance of Flask test app
        new_user (User): Instance of a user
        new_user_two (User): Instance of a another user
     Returns:
        work order (dict): Dictionary of the created work order
    """
    new_user.save()
    new_work_order_user.save()
    new_maintenance_category.save()
    return WorkOrder(
        title='Incorrect Center Work Order',
        description='A very long description',
        frequency='weekly',
        assignee_id=new_work_order_user.token_id,
        maintenance_category_id=new_maintenance_category.id,
        start_date='2011-08-12 00:00:00',
        end_date='2019-08-12 00:00:00',
        created_by=new_user.token_id,
        updated_by=new_user.token_id)


@pytest.fixture(scope='function')
def create_bulk_work_orders(app, init_db, new_maintenance_category, new_user):
    """Fixture for creating bulk work orders
     Args:
        app (object): Instance of Flask test app
        init_db (fixture): Fixture to initialize the test database operations.
        new_maintenance_category(obj): Instance of an Maintenance Category
        new_user (obj): Instance of a user
     Returns:
        work orders (dict): List of the created work orders
    """
    new_maintenance_category.save()
    new_user.save()
    title_list = ['Fuel Level', 'work order 2', 'work order 3']
    work_orders = []
    for title in title_list:
        details = {
            'title': title,
            'description': 'Some description about work order',
            'maintenance_category_id': new_maintenance_category.id,
            'assignee_id': new_user.token_id,
            'frequency': 'weekly',
            'status': 'enabled',
            'start_date': '2018-12-12 00:00:00',
            'end_date': '2019-02-1 00:00:00',
            'created_by': new_user.token_id,
        }
        work_order = WorkOrder(**details)
        work_orders.append(work_order)
    return work_orders
