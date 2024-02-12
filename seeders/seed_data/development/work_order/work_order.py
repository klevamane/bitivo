"""Development/Testing environment work_order seed data module"""

# Models
from api.models import User, Center, MaintenanceCategory


def work_order_data():
    """ Creates a dict for a work order
        Args:
            kwargs (dict): arguments of data needed to created the work order
        Returns:
            dict: A dictionary of a request
    """
    # Centers
    center_one, center_two, center_three = Center.query_().limit(3).all()

    # Users
    user_one, user_two, user_three = User.query_().limit(3).all()

    # Asset Categories
    maintenance_category_one, maintenance_category_two, maintenance_category_three = \
    MaintenanceCategory.query_().limit(3).all()

    return [
        {
            "title": 'Check fuel Level',
            "description":
            'The fuel level needs to be checked for maintenance',
            "maintenance_category_id": maintenance_category_one.id,
            "assignee_id": user_one.token_id,
            "frequency": 'daily',
            "status": 'enabled',
            "start_date": '2018-12-12 00:00:00',
            "end_date": '2019-02-1 00:00:00',
        },
        {
            "title": 'Clean Battery terminals',
            "description":
            'The baterry terminals of the Generator needs to be cleaned',
            "maintenance_category_id": maintenance_category_two.id,
            "assignee_id": user_two.token_id,
            "frequency": 'weekly',
            "status": 'enabled',
            "start_date": '2018-12-12 00:00:00',
            "end_date": '2019-03-1 00:00:00',
        },
        {
            "title": 'Replace Oil',
            "description": 'The generator oil needs to be replaced',
            "maintenance_category_id": maintenance_category_three.id,
            "assignee_id": user_three.token_id,
            "frequency": 'weekday',
            "status": 'disabled',
            "start_date": '2018-12-12 00:00:00',
            "end_date": '2019-03-1 00:00:00',
        },
        {
            "title": 'With custom occurence',
            "description":
            'The fuel level needs to be checked for maintenance',
            "maintenance_category_id": maintenance_category_one.id,
            "assignee_id": user_one.token_id,
            "frequency": 'no_repeat',
            "status": 'disabled',
            "start_date": '2018-12-12 00:00:00',
            "end_date": '2019-02-1 00:00:00',
        },
        {
            "title": 'Go to garage',
            "description":
            'The fuel level needs to be checked for maintenance',
            "maintenance_category_id": maintenance_category_one.id,
            "assignee_id": user_one.token_id,
            "frequency": 'custom',
            "status": 'enabled',
            "start_date": '2018-12-12 00:00:00',
            "end_date": '2019-02-1 00:00:00',
            "custom_occurrence": {
                "repeat_days": ["Monday", "Tuesday"],
                "repeat_units": 2,
                "repeat_frequency": "week",
                "ends": {
                    "after": 4,
                    "on": "2019-02-14",
                    "never": True
                }
            }
        },
    ]
