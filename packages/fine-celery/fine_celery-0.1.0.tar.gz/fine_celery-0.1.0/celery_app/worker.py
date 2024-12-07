from celery.apps.worker import Worker
from nice_celery.celery_app.app import celery_app
import logging

logger = logging.getLogger(__name__)

import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='celery.platforms')
warnings.filterwarnings('ignore', category=UserWarning, module='kombu.utils.encoding')

def start_worker():
    """启动 Celery worker"""
    worker = Worker(app=celery_app)

    # 打印任务注册信息
    logger.info("Available tasks:")
    for task_name in sorted(celery_app.tasks.keys()):
        # logger.info(f"  . {task_name}")
        print(f"  . {task_name}")

    return worker.start()

if __name__ == '__main__':
    start_worker()
