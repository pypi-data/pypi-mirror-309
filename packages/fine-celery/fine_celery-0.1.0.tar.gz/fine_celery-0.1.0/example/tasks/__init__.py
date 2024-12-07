from .math_tasks import add_numbers
from .monitor_tasks import heartbeat

__all__ = [
    'add_numbers',
    'heartbeat',
]

from celery_app.app import celery_app
import logging

logger = logging.getLogger(__name__)
logger.info(f"Registered tasks: {list(celery_app.tasks.keys())}") 