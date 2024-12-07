from typing import Optional, Dict, Any
from datetime import timedelta
from pydantic import Field, validator
from .base import BaseConfig

class BeatConfig(BaseConfig):
    """Celery Beat 调度器配置类

    包含所有与 Celery Beat 调度器相关的配置：
    - 调度器存储配置
    - 调度任务配置
    - 性能和同步配置
    - 日志配置
    """
    _PREFIX = "nice_celery:redbeat:"


    # 添加时区配置
    TIMEZONE: str = Field(
        default="Asia/Shanghai",
        description="时区设置。设置为 Asia/Shanghai 后，可以直接用北京时间编写调度规则，"
                   "Celery 会自动处理与服务器时间（如 UTC）的转换"
    )

    ENABLE_UTC: bool = Field(
        default=True,
        description="是否启用 UTC。建议保持为 True，让 Celery 在内部使用 UTC 处理时间，"
                   "这样可以避免夏令时等问题。Celery 会根据 TIMEZONE 设置自动处理时区转换"
    )


    # 调度器存储配置
    BEAT_SCHEDULER: str = Field(
        default="redbeat.RedBeatScheduler",
        description="使用 RedBeat 作为调度器，基于 Redis 存储"
    )

    BEAT_MAX_LOOP_INTERVAL: int = Field(
        default=300,
        description="Beat 循环的最大间隔时间(秒)"
    )

    # RedBeat 特定配置
    REDBEAT_REDIS_URL: Optional[str] = Field(
        default=None,
        description="RedBeat Redis URL，如果为 None 则使用 broker_url"
    )

    REDBEAT_KEY_PREFIX: str = Field(
        default=_PREFIX,
        description="RedBeat 在 Redis 中的键前缀"
    )

    REDBEAT_LOCK_KEY: str = Field(
        default=f"{_PREFIX}lock",
        description="RedBeat 锁键模板"
    )

    REDBEAT_LOCK_TIMEOUT: int = Field(
        default=60,
        description="锁超时时间(秒)"
    )

    # 性能配置
    BEAT_MAX_WAITING_TIME: float = Field(
        default=30.0,
        description="等待新任务的最大时间(秒)"
    )

    BEAT_SYNC_EVERY: int = Field(
        default=180,
        description="同步到磁盘的频率(次)"
    )

    # 日志配置
    BEAT_LOG_LEVEL: str = Field(
        default="INFO",
        description="Beat 日志级别"
    )

    # 默认调度任务配置
    BEAT_SCHEDULE: Dict[str, Dict[str, Any]] = Field(
        # default_factory=lambda: BEAT_SCHEDULES,
        # 默认作为空字典
        default_factory=dict,
        description="Beat 调度任务配置"
    )

    @validator('BEAT_SCHEDULE')
    def validate_schedule(cls, v):
        """验证调度任务配置

        注意：调度时间配置应该使用北京时间
        例如：想在北京时间每天早上 9 点执行任务
        {
            'morning-task': {
                'task': 'your_task',
                'schedule': crontab(hour=9, minute=0)  # 直接使用北京时间 9 点
            }
        }
        """
        for task_name, task_config in v.items():
            required_keys = {'task', 'schedule'}
            if not all(key in task_config for key in required_keys):
                raise ValueError(f"任务 {task_name} 缺少必要的配置项: {required_keys}")
        return v

    class Config:
        """配置示例

        使用示例：
        BEAT_SCHEDULE = {
            'task-name': {
                'task': 'module.tasks.your_task',
                # 以下时间都使用北京时间编写
                'schedule': crontab(hour=9, minute=30),  # 每天早上 9:30
                # 或
                'schedule': crontab(minute='*/15'),      # 每 15 分钟
                # 或
                'schedule': timedelta(hours=1),          # 每小时
                'args': (),                              # 任务参数
                'kwargs': {},                            # 任务关键字参数
                'options': {                             # 任务选项
                    'expires': 3600,                     # 过期时间
                    'queue': 'default',                  # 指定队列
                }
            }
        }
        """
        ...
