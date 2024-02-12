from datetime import datetime, timedelta
now = datetime.now()


def celery_task_state(*args, **kwargs):
    """Function to get statistics about celery-beat scheduled tasks

        Args:
            *args: Variable length argument list and the mandatory position arguments for this list are:
                task (instance): an instance of python Shelve class
                task_name (str): Task name
                ok_tasks (dict): A python dictionary holding celery-beat tasks that run successfully
                down_tasks (dict): A python dictionary holding celery-beat tasks that didn't run successfully

            **kwargs: Variable length keyword argument dictionary and the mandatory keys for this dictionary are:
                is_cron_task (bool): True if the scheduled task is a cron job task otherwise False.
        """
    task, task_name, ok_tasks, down_tasks = args
    is_cron_task = kwargs.get('is_cron_task', True)
    next_run = now + task.schedule.remaining_estimate(task.last_run_at)

    if_condition = timedelta() < task.schedule.remaining_estimate(
        task.last_run_at
    ) if is_cron_task else now < task.last_run_at + task.schedule.run_every

    if if_condition:
        ok_tasks[task_name] = {
            'status': 'Okay',
            'last_run': task.last_run_at,
            'next run': next_run
        }
        return
    down_tasks[task_name] = {
        'status': 'Down',
        'last_run': task.last_run_at,
        'missed run': next_run
    }
