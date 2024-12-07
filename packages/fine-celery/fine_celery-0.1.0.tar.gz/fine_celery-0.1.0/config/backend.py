from typing import Optional, Dict, Any
from pydantic import Field
from .base import BaseConfig

class RedisBackendConfig(BaseConfig):
    """Redis result backend 配置类"""

    # Redis连接配置
    RESULT_BACKEND_HOST: str = Field(
        default="localhost",
        description="Redis result backend host"
    )
    RESULT_BACKEND_PORT: int = Field(
        default=6379,
        description="Redis result backend port"
    )
    RESULT_BACKEND_DB: int = Field(
        default=0,
        description="Redis result backend database"
    )
    RESULT_BACKEND_USERNAME: Optional[str] = Field(
        default=None,
        description="Redis result backend username"
    )
    RESULT_BACKEND_PASSWORD: Optional[str] = Field(
        default=None,
        description="Redis result backend password"
    )

    # 结果配置
    RESULT_EXPIRES: int = Field(
        default=24 * 3600,  # 1 day
        description="结果过期时间(秒)"
    )

    RESULT_CACHE_MAX: int = Field(
        default=10000,
        description="结果缓存的最大数量"
    )

    # Redis 键配置
    RESULT_KEY_PREFIX: str = Field(
        default='nice_celery:result:',
        description="结果键前缀"
    )

    # 序列化配置
    RESULT_SERIALIZER: str = Field(
        default='json',
        description="结果序列化格式"
    )

    RESULT_COMPRESSION: Optional[str] = Field(
        default=None,
        description="结果压缩方式，例如：gzip, bzip2"
    )

    # 扩展配置
    RESULT_EXTENDED: bool = Field(
        default=False,
        description="是否存储扩展任务信息"
    )

    # 后端特定配置
    REDIS_BACKEND_USE_SSL: bool = Field(
        default=False,
        description="是否使用SSL连接"
    )

    REDIS_BACKEND_SOCKET_TIMEOUT: int = Field(
        default=120,
        description="Socket超时时间(秒)"
    )

    REDIS_BACKEND_SOCKET_CONNECT_TIMEOUT: int = Field(
        default=30,
        description="连接超时时间(秒)"
    )

    REDIS_BACKEND_RETRY_ON_TIMEOUT: bool = Field(
        default=True,
        description="超时时是否重试"
    )

    REDIS_MAX_CONNECTIONS: int | None = Field(
        default=None,
        description="最大连接数，None表示无限制"
    )

    # 健康检查配置
    REDIS_BACKEND_HEALTH_CHECK_INTERVAL: int = Field(
        default=30,
        description="健康检查间隔(秒)"
    )

    @property
    def result_backend_url(self) -> str:
        """构建 Redis result backend URL"""
        auth = ""
        if self.RESULT_BACKEND_USERNAME and self.RESULT_BACKEND_PASSWORD:
            auth = f"{self.RESULT_BACKEND_USERNAME}:{self.RESULT_BACKEND_PASSWORD}@"
        if not self.REDIS_BACKEND_USE_SSL:
            return f"redis://{auth}{self.RESULT_BACKEND_HOST}:{self.RESULT_BACKEND_PORT}/{self.RESULT_BACKEND_DB}"
        else:
            return f"rediss://{auth}{self.RESULT_BACKEND_HOST}:{self.RESULT_BACKEND_PORT}/{self.RESULT_BACKEND_DB}"
    @property
    def backend_transport_options(self) -> Dict[str, Any]:
        """获取后端传输选项"""
        if not self.REDIS_BACKEND_USE_SSL:
            return {
                'retry_on_timeout': self.REDIS_BACKEND_RETRY_ON_TIMEOUT,
                'socket_timeout': self.REDIS_BACKEND_SOCKET_TIMEOUT,
                'socket_connect_timeout': self.REDIS_BACKEND_SOCKET_CONNECT_TIMEOUT,
                'max_connections': self.REDIS_MAX_CONNECTIONS,
                'health_check_interval': self.REDIS_BACKEND_HEALTH_CHECK_INTERVAL,
                'global_keyprefix': self.RESULT_KEY_PREFIX,
            }
        else:
            return {
                'retry_on_timeout': self.REDIS_BACKEND_RETRY_ON_TIMEOUT,
                'socket_timeout': self.REDIS_BACKEND_SOCKET_TIMEOUT,
                'socket_connect_timeout': self.REDIS_BACKEND_SOCKET_CONNECT_TIMEOUT,
                'max_connections': self.REDIS_MAX_CONNECTIONS,
                'health_check_interval': self.REDIS_BACKEND_HEALTH_CHECK_INTERVAL,
                'global_keyprefix': self.RESULT_KEY_PREFIX,

                "socket_timeout": 30,
                "socket_connect_timeout": 30,
                "socket_keepalive": True,
                "health_check_interval": 30,
                'ssl': True,  # 启用 TLS
                'ssl_cert_reqs': 'none',  # 不验证服务器证书
            }
