from api.utilities.helpers.celery import celery_task_state

from tests.mocks.celery import Task


class TestCeleryTaskState:
    """Tests the celery_task_state function"""

    def test_celery_task_state_succeeds(self):
        """Tests that celery_task_state tasks succeeds when scheduled to run at specific intervals"""
        ok = {}
        down = {}

        celery_task_state(Task, 'task_name', ok, down, is_cron_task=False)

        assert down.get('task_name').get('status') == 'Down'

    def test_celery_task_state_with_cron_jobs_succeeds(self):
        """Tests that celery_task_state tasks succeeds when scheduled through a cron job"""
        ok = {}
        down = {}

        celery_task_state(Task(True), 'task_name', ok, down)

        assert ok.get('task_name').get('status') == 'Okay'
