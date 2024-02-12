"""This file has validation for creating work orders"""

# datetime
from datetime import datetime, date

# Models
from api.models import MaintenanceCategory, User

# Helpers
from api.utilities.verify_date_range import verify_date_range, check_date_order
from ..error import raises
from .date_validator import date_validator
from ..verify_date_range import check_date_order
from .validate_category import validate_category_exists


def validate_title_duplicate(model, data, work_order_id=None):
    """This function checks whether the title given has only been used
    on the same maintenance category and in the same center.

     Args:
        model (model): The model we are going to check for duplicates
        data (json): The work order object received.
        work_order_id (string id): The existing work_order id
    """
    title = data.get('title')
    maintenance_category_id = data.get('maintenance_category_id')
    result = model.query_().filter_by(
        title=title, maintenance_category_id=maintenance_category_id).filter(
            id != work_order_id).first()
    if result and result.id != work_order_id:
        raises('work_order_exists', 409, title)


def validate_work_order_dates(data, start_date, end_date):
    """This method verify and validates the dates.

    Args:
        start (string): work-order start date
        example is '2021-1-9 11:00:00'

         end (string): work-order end date
        example is '2021-1-9 11:00:00'

        date(dict): work-order object

    Returns:
    """
    start = data['startDate'].strftime(
        "%Y-%m-%d %H:%M:%S") if not start_date else start_date
    end = data['endDate'].strftime(
        "%Y-%m-%d %H:%M:%S") if not end_date else end_date
    today = datetime.strptime(date.today().strftime('%Y-%m-%d'), '%Y-%m-%d')
    start_date = start
    end_date = end
    args = (start, end, start_date, end_date, today)
    check_date_order(*args)


def maintenance_category_exists(category_id):
    """Checks if maintenance category exists
    
    Args:
        category_id (str): id to check
        
    Raises: 
        Marshmallow Validation error if the asset category doesn't exist.
    """
    validate_category_exists(MaintenanceCategory, category_id)


def validate_assignee_as_member_of_center(data,
                                          center_id=None,
                                          assignee_id=None):
    """Checks if a user belongs to the specified center
    Args:
        data (dict): The request object
        center_id (kwarg: str): The id of the center if available
        assignee_id (kwarg: str): The id of the assignee if the assignee is not updated
    Raises:
        ValidationError: If an assignee does not belong
        to the specified center.
    """
    token_id = data.get('assigneeId', assignee_id)
    center_id = data.get('centerId', center_id)
    if token_id and center_id:
        user = User.query_().filter_by(
            token_id=token_id, center_id=center_id).first()
        if not user:
            raises('assignee_not_found', 400)
