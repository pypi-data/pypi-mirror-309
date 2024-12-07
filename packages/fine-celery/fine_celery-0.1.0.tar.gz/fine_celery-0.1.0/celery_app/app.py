from celery import Celery
from celery.signals import (
    task_prerun, task_postrun, task_success,
    task_failure, worker_ready, worker_shutdown
)
from nice_celery.config.celery import CeleryConfig
import logging

logger = logging.getLogger(__name__)

def create_celery_app(app_name: str = "celery_app", config_dict=None) -> Celery:
    """
    创建 Celery 应用实例并配置信号处理器

    Args:
        app_name: Celery 应用名称

    Returns:
        Celery 应用实例
    """
    # 创建 Celery 实例
    celery_app = Celery(app_name)

    # 加载配置，支持外部配置
    config = CeleryConfig(external_config=config_dict)
    celery_app.conf.update(config.get_celery_config())


    # 配置信号处理器
    @task_prerun.connect
    def task_prerun_handler(task_id, task, *args, **kwargs):
        """任务执行前的处理"""
        logger.info(f"Task {task.name}[{task_id}] is about to run")

    @task_postrun.connect
    def task_postrun_handler(task_id, task, *args, retval=None, state=None, **kwargs):
        """任务执行后的处理"""
        logger.info(f"Task {task.name}[{task_id}] finished with state: {state}")

    @task_success.connect
    def task_success_handler(sender=None, **kwargs):
        """任务成功完成的处理"""
        logger.info(f"Task {sender.name} completed successfully")

    @task_failure.connect
    def task_failure_handler(task_id, exception, traceback, sender, **kwargs):
        """任务失败的处理"""
        logger.error(f"Task {sender.name}[{task_id}] failed: {exception}")

    @worker_ready.connect
    def worker_ready_handler(**kwargs):
        """Worker 就绪时的处理"""
        logger.info("Celery worker is ready")

    @worker_shutdown.connect
    def worker_shutdown_handler(**kwargs):
        """Worker 关闭时的处理"""
        logger.info("Celery worker is shutting down")

    return celery_app

if __name__ == "__main__":
    print("\n\n\n\n in celery_app/app.py\n\n\n")
    # 创建 Celery 应用实例
    from nice_celery.example.config.beat import ExampleBeatConfig

    celery_app = create_celery_app()

    # 使用示例配置
    example_config = ExampleBeatConfig()
    celery_app.conf.update(
        beat_schedule=example_config.BEAT_SCHEDULE
    )

    # 修改为包含完整的包路径
    celery_app.autodiscover_tasks(['example'])  # 不需要写 .tasks，它会自动查找 tasks 目录
