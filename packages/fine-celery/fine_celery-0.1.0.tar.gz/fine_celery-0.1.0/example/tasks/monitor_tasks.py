from nice_celery.celery_app.app import celery_app
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name="example.tasks.heartbeat")
def heartbeat():
    """发送心跳信号，每10秒执行一次"""
    logger.info("Heartbeat task received")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"Heartbeat at {current_time}"
    logger.info(message)
    print(message)
    return message
