from nice_celery.celery_app.app import celery_app
from celery.bin.celery import CeleryCommand
# from celery.bin.flower import FlowerCommand
import logging

logger = logging.getLogger(__name__)

def start_flower():
    """启动 Celery Flower 监控"""
    try:
        logger.info("Starting Flower on http://localhost:5555")

        # 创建 Flower 命令实例
        flower = FlowerCommand()

        # 设置 Celery 应用
        flower.app = celery_app

        # 设置参数
        options = [
            '--address=0.0.0.0',
            '--port=5555',
            '--persistent=True',
            '--db=flower.db',
            '--inspect_timeout=1000'
        ]

        # 启动 Flower
        return flower.run_from_argv(['flower'] + options)

    except Exception as e:
        logger.error(f"Failed to start Flower: {e}")
        raise

if __name__ == '__main__':
    start_flower()
