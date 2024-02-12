"""This module will receive inserted work order and generate schedules to db"""
from api.models.database import db
from api.utilities.schedule_date_generation_helper import GenerateDates
from api.utilities.enums import ScheduleStatusEnum


def generate_schedule_due_dates(saved_work_order, dates_maps):
    """Helper method to generate and format due dates for
     schedule from work order.
     Args:
        saved_work_order (object): The work order object
        dates_maps(List of dates times] List of deu dates
     Returns:
        (list): list of generated due dates
    """
    work_order_id = saved_work_order.id
    assignee_id = saved_work_order.assignee_id
    created_by = saved_work_order.created_by

    return [
        create_schedule_data(
            created_by=created_by,
            due_date=date,
            work_order_id=work_order_id,
            assignee_id=assignee_id) for date in dates_maps
    ]


def create_schedule_data(**kwargs):
    """Creates a dict for a schedules
         Args:
            kwargs (dict): arguments of data needed to created the schedule
        Returns:
            (dict): A dictionary of schedules
    """

    return {
        "work_order_id": kwargs['work_order_id'],
        "assignee_id": kwargs['assignee_id'],
        "due_date": kwargs['due_date'],
        "created_by": kwargs['created_by'],
        "status": 'pending',
    }


def create_schedules(saved_work_order):
    """ This function will insert generate schedules and insert them
        into schedules model
        Args:
            saved_work_order(object): object of inserted work oder
    """
    if isinstance(saved_work_order.frequency, str):
        # This means '.save' has been used to save the work order.
        # This will not how serializer saves the frequency of work order
        return
    if saved_work_order.frequency.value == "custom" and saved_work_order.custom_occurrence is None:
        return
    schedule_object = GenerateDates(saved_work_order)
    schedule_mapper = {
        "no_repeat": schedule_object.no_repeat_dates,
        "daily": schedule_object.daily_dates,
        "weekly": schedule_object.weekly_dates,
        "weekday": schedule_object.weekday_dates,
        "custom": schedule_object.custom_dates
    }
    dates_maps = schedule_mapper.get(saved_work_order.frequency.value)
    if dates_maps:
        from api.models import Schedule
        schedules_details = generate_schedule_due_dates(
            saved_work_order, dates_maps())
        schedules = [Schedule(**schedule) for schedule in schedules_details]
        db.session.add_all(schedules)


def remove_pending_schedules(schedule_model, work_order):
    """Hard deletes schedules with pending statuses
         Args:
            schedule_model (Schedule): Schedule model class
            work_order (object): updated work_oder instance
    """

    schedules = schedule_model.query.filter_by(
        work_order=work_order, status=ScheduleStatusEnum.pending)
    schedules.delete()


def regenerate_schedules(work_order, changed_fields):
    """Regenerates schedules for the updated work_oder
         Args:
            work_order (object): updated work_oder instance
            changed_fields (list): list if fields changed on a work_order
    """
    from api.models import Schedule
    fields_considered = [
        'frequency', 'custom_occurrence', 'start_date', 'end_date'
    ]
    if any(True for key in changed_fields if key in fields_considered):
        remove_pending_schedules(Schedule, work_order)

    create_schedules(work_order)
