from .base import BaseConfig
from pydantic import Field

class SingletonConfig(BaseConfig):
    """Celery Singleton 配置类

    用于控制任务的单例执行行为：
    - Redis 连接配置
    - 锁超时配置
    - 键前缀配置
    """

    # Redis 连接配置
    SINGLETON_BACKEND_URL: str | None = Field(
        default=None,
        description="Singleton Redis URL，如果为 None 则使用 broker_url"
    )

    # 键前缀配置
    SINGLETON_KEY_PREFIX: str = Field(
        default="nice_celery:singleton:",
        description="Singleton 在 Redis 中的键前缀"
    )

    # 锁配置
    SINGLETON_LOCK_EXPIRY: int = Field(
        default=60,
        description="锁超时时间(秒)"
    )

    SINGLETON_RAISE_ON_DUPLICATE: bool = Field(
        default=False,
        description="重复任务时是否抛出异常"
    )
