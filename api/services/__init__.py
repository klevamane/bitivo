# Third Party libraries
from celery import Celery

# App configuration
from config import AppConfig

celery_scheduler = Celery(__name__, broker=AppConfig.REDIS_URL)
celery_scheduler.conf.enable_utc = False
