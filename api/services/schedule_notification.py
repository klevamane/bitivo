"""Module for sending email notifications on schedule due_date and resetting hot desk spreadsheet everyday"""

# Third Party
from sqlalchemy import text
from datetime import datetime, timedelta

# Models
from api.models import HotDeskRequest
from api.models.database import db

# App config
from config import AppConfig

# Utilities
from ..tasks.notifications import SendEmail
from ..utilities.sql_queries import sql_queries
from ..utilities.helpers.get_mailing_params import get_mailing_params
from ..utilities.helpers.calendar import get_start_or_end_of_day

# Bot utilities
from bot.utilities.bugsnag import post_bugsnag_exception

# GoogleSheetHelper
from bot.utilities.google_sheets.google_sheets_helper import GoogleSheetHelper
from bot.utilities.helpers.spreadsheet_helper import update_

# celery scheduler
from . import celery_scheduler


@celery_scheduler.task(name='schedule_due_date_notifier')
def schedule_due_date_notifier():
    """Function to notify assignee of a due schedule."""

    query = sql_queries['get_due_schedules']

    schedules = db.engine.execute(text(query)).fetchall()

    # To help in testing purposes
    notified = False

    for name, email, task_names in schedules:
        data = {
            'username': name,
            'tasks': task_names,
            'domain': AppConfig.DOMAIN
        }
        schedule_params = get_mailing_params('schedule_due_template', name,
                                             data)
        schedule_params = dict(recipient=email, **schedule_params)
        SendEmail.send_mail_with_template(**schedule_params)
        notified = True
    return notified


@celery_scheduler.task(name='reset_hot_desk_spreadsheet')
def reset_hot_desk_spreadsheet():
    """Function to  to reset the hotdesks spreadsheet
    Return:
        None
    """
    yesterday = datetime.today() - timedelta(days=1)
    start_date = get_start_or_end_of_day(yesterday, end=False)
    end_date = get_start_or_end_of_day(yesterday, end=True)

    approved_requests_yesterday = HotDeskRequest.query.filter\
        (HotDeskRequest.status == 'approved',
         HotDeskRequest.created_at.between(start_date, end_date)).all()

    sheet_data, sheet = GoogleSheetHelper().open_sheet()
    if sheet:
        bay_column = sheet.col_values(2)[1:]

    for request in approved_requests_yesterday:
        try:
            update_(sheet_data, sheet, bay_column, request.hot_desk_ref_no, 'Hot Desk')
        except Exception as error:
            post_bugsnag_exception(
                error, f'Could not reset Hot desk with ref no - {request.hot_desk_ref_no}')
