from nice_celery.celery_app.app import celery_app
from typing import Union
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name="example.tasks.add_numbers")
def add_numbers(x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
    """计算两个数字的和"""
    try:
        result = x + y
        logger.info(f"Successfully calculated {x} + {y} = {result}")
        return result
    except Exception as exc:
        logger.error(f"Failed to calculate sum: {exc}")
        raise  # 如果需要重试，使用 self.retry(exc=exc)
