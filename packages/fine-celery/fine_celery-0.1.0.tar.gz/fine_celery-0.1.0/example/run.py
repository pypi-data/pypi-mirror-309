from nice_celery.celery_app.app import create_celery_app
from nice_celery.example.config.beat import ExampleBeatConfig
from nice_celery.example.tasks import math_tasks, monitor_tasks
import logging

logger = logging.getLogger(__name__)

def create_example_app():
    """创建示例 Celery 应用"""
    app = create_celery_app()

    # 使用示例配置
    example_config = ExampleBeatConfig()
    app.conf.update(
        beat_schedule=example_config.BEAT_SCHEDULE
    )

    # 注册示例任务
    app.autodiscover_tasks(['nice_celery.example.tasks'])

    return app

def test_add_numbers():
    """测试加法任务"""
    app = create_example_app()
    result = math_tasks.add_numbers.delay(5, 3)
    logger.info(f"Task ID: {result.id}")
    sum_result = result.get(timeout=10)
    logger.info(f"Result: 5 + 3 = {sum_result}")

if __name__ == "__main__":
    test_add_numbers()
