"""Celery Tasks"""

from main import celery_app


@celery_app.task(name="sample_scheduler")
def sample_scheduler():
    """Sample to test `/celery` endpoint has scheduled tasks"""
    return dict(message="sample scheduler")
