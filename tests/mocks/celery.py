from datetime import datetime, timedelta


class Task:
    """Class that holds the task objects accepted by celery_task_state function"""
    last_run_at = timedelta()

    def __init__(self, success=False):
        Task.last_run_at = timedelta() if not success else timedelta(minutes=3)

    class schedule:

        run_every = datetime(
            year=datetime.today().year,
            month=datetime.today().month,
            day=datetime.today().day)

        @staticmethod
        def remaining_estimate(last_run_at):
            return last_run_at
