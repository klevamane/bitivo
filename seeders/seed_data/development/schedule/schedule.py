"""Development/Testing environment schedule seed data module"""

# Models
from api.models import User, WorkOrder


def schedule_data():
    """Creates a dict for a schedule

        Returns:
            dict: A dictionary of schedules
    """
    # WorkOrder
    work_order_one, work_order_two, work_order_three = WorkOrder.query_(
    ).limit(3).all()

    # Users
    user_one, user_two, user_three = User.query_().limit(3).all()

    return [
        {
            "work_order_id": work_order_one.id,
            "assignee_id": user_one.token_id,
            "due_date": '2050-12-12 00:00:00',
            "status": 'pending'
        },
        {
            "work_order_id": work_order_two.id,
            "assignee_id": user_two.token_id,
            "due_date": '2055-12-12 00:00:00',
            "status": 'done'
        },
        {
            "work_order_id": work_order_three.id,
            "assignee_id": user_three.token_id,
            "due_date": '2060-12-12 00:00:00',
            "status": 'pending'
        },
    ]
