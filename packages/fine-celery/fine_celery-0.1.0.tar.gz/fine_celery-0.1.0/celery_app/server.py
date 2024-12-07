from multiprocessing import Process
from nice_celery.celery_app.worker import start_worker
from nice_celery.celery_app.beat import start_beat
# from celery_app.flower import start_flower
import logging
import time
import signal
import sys

logger = logging.getLogger(__name__)

class CeleryServer:
    """Celery 服务管理器，用于同时管理 worker、beat 和 flower"""

    def __init__(self):
        self.processes = {}
        self.running = True

        # 注册信号处理
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

    def handle_signal(self, signum, frame):
        """处理终止信号"""
        logger.info(f"Received signal {signum}")
        self.shutdown()

    def start_process(self, name: str, target: callable):
        """启动一个新进程"""
        process = Process(target=target, name=name)
        process.daemon = True  # 设置为守护进程
        process.start()
        self.processes[name] = process
        logger.info(f"Started {name} process (PID: {process.pid})")
        return process

    def start(self):
        """启动所有服务"""
        try:
            logger.info("Starting Celery services...")

            # 启动 Worker
            self.start_process('worker', start_worker)
            time.sleep(2)  # 等待 worker 启动

            # 启动 Beat
            self.start_process('beat', start_beat)
            time.sleep(1)  # 等待 beat 启动

            # # 启动 Flower
            # self.start_process('flower', start_flower)

            logger.info("All services started successfully")

            # 监控进程状态
            while self.running:
                for name, process in self.processes.items():
                    if not process.is_alive():
                        logger.error(f"{name} process died, restarting...")
                        self.start_process(name,
                            start_worker if name == 'worker' else
                            start_beat if name == 'beat' else
                            start_flower
                        )
                time.sleep(5)

        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
            self.shutdown()
        except Exception as e:
            logger.error(f"Error starting services: {e}")
            self.shutdown()
            raise

    def shutdown(self):
        """关闭所有服务"""
        logger.info("Shutting down all services...")
        self.running = False

        # 按照相反的顺序关闭服务
        for name in reversed(list(self.processes.keys())):
            process = self.processes[name]
            logger.info(f"Stopping {name} process (PID: {process.pid})")
            process.terminate()
            process.join(timeout=5)

            # 如果进程没有正常退出，强制结束
            if process.is_alive():
                logger.warning(f"{name} process did not terminate gracefully, killing...")
                process.kill()
                process.join()

        logger.info("All services stopped")
        sys.exit(0)

def start_server():
    """启动服务器"""
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
    )

    # 启动服务
    server = CeleryServer()
    server.start()

if __name__ == '__main__':
    start_server()
