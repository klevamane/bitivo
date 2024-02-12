"""Configuring Celery Beat used for running periodic tasks"""

# Third Party
from celery.schedules import crontab

# Services
from api.services import celery_scheduler

celery_scheduler.conf.beat_schedule = {

    # The low_asset_count_notifier task is commented out because
    # the stock level notification mail feature has currently
    # been disabled as a request by the Operations Associate team
    # 'run-asset-count-every-2-day(s)': {
    #     'task': 'low_asset_count_notifier',
    #     'schedule': crontab(day_of_week="1,3,5", hour=7, minute=30)
    # },
    'run-close-request-automatically-every-day': {
        'task': 'close_expired_request',
        'schedule': crontab(hour=0, minute=0)
    },
    'run-schedule-due-date-check-every-day': {
        'task': 'schedule_due_date_notifier',
        'schedule': crontab(hour=8, minute=0)
    },
    'run-reset-hotdesk-spreadsheet-every-day': {
        'task': 'reset_hot_desk_spreadsheet',
        'schedule': crontab(day_of_week='1,2,3,4,5,6', hour=0, minute=0),
    },
}
