from nice_celery.celery_app.app import celery_app
from celery.apps.beat import Beat
from nice_celery.config.beat import BeatConfig

def start_beat():
    """启动 Celery beat"""
    beat_config = BeatConfig()

    # 直接创建 Beat 实例
    beat = Beat(
        app=celery_app,
        loglevel=beat_config.BEAT_LOG_LEVEL,
        # schedule=beat_config.BEAT_SCHEDULE_FILE,
        # max_interval=beat_config.BEAT_MAX_INTERVAL,
        # working_directory=beat_config.BEAT_WORKING_DIR,
        # pidfile=beat_config.BEAT_PID_FILE
    )

    return beat.run()

if __name__ == '__main__':
    start_beat()
