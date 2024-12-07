from nice_celery.config.beat import BeatConfig
from ..schedules.task_schedules import BEAT_SCHEDULES

class ExampleBeatConfig(BeatConfig):
    """示例 Beat 配置类，用于演示目的"""

    def __init__(self):
        super().__init__()
        # 显式设置示例调度任务
        self.BEAT_SCHEDULE = BEAT_SCHEDULES
