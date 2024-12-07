from typing import Optional, List
from pydantic import Field, validator
from .base import BaseConfig

class RedisBrokerConfig(BaseConfig):
    """Redis broker 配置类

    此类包含所有与 Redis 消息代理相关的配置，包括：
    - Redis 连接基本配置
    - 连接池配置
    - 连接重试策略
    - SSL/TLS 配置
    - 心跳检测配置
    """

    # Redis基础连接配置
    BROKER_HOST: str = Field(default="localhost", description="Redis broker 主机地址")
    BROKER_PORT: int = Field(default=6379, description="Redis broker 端口号")
    BROKER_DB: int = Field(default=0, description="Redis broker 数据库编号")
    BROKER_USERNAME: Optional[str] = Field(default=None, description="Redis broker 用户名")
    BROKER_PASSWORD: Optional[str] = Field(default=None, description="Redis broker 密码")

    # 连接池配置
    BROKER_POOL_MAX_CONNECTIONS: int = Field(
        default=10,
        description="连接池中允许的最大连接数"
    )
    BROKER_POOL_TIMEOUT: int = Field(
        default=20,
        description="从连接池获取连接的超时时间(秒)"
    )

    # key前缀配置
    BROKER_KEY_PREFIX: str = Field(default="nice_celery:broker:", description="Redis broker key 前缀")

    # 连接重试策略
    BROKER_CONNECTION_RETRY: bool = Field(
        default=True,
        description="连接断开时是否自动重试 (Celery 6.0后将废弃)"
    )
    BROKER_CONNECTION_RETRY_ON_STARTUP: bool = Field(
        default=True,
        description="启动时是否重试连接 (推荐使用此配置替代 BROKER_CONNECTION_RETRY)"
    )
    BROKER_CONNECTION_MAX_RETRIES: int = Field(
        default=100,
        description="连接重试的最大次数，None表示无限重试"
    )
    BROKER_CONNECTION_TIMEOUT: int = Field(
        default=4,
        description="建立连接的超时时间(秒)"
    )

    # 心跳检测配置
    BROKER_HEARTBEAT: int = Field(
        default=120,
        description="心跳间隔(秒)，None表示禁用心跳"
    )
    BROKER_HEARTBEAT_CHECKRATE: int = Field(
        default=2,
        description="心跳检查频率倍数"
    )

    # SSL/TLS配置
    BROKER_USE_SSL: bool = Field(
        default=False,
        description="是否使用SSL/TLS连接"
    )
    BROKER_SSL_CERT_REQS: Optional[str] = Field(
        default=None,
        description="SSL证书验证模式: None, 'optional' 或 'required'"
    )

    # 消息传输配置
    BROKER_TRANSPORT_OPTIONS: dict = Field(
        default_factory=lambda: {
            'visibility_timeout': 3600,  # 消息可见性超时时间
            'fanout_prefix': True,       # 使用扇出前缀
            'fanout_patterns': True,     # 启用扇出模式
            'global_keyprefix': "nice_celery:broker:",
        },
        description="broker传输选项"
    )

    @property
    def broker_url(self) -> str:
        """构建 Redis broker URL

        Returns:
            str: 格式化的Redis URL，包含认证信息(如果提供)
        """
        auth = ""
        if self.BROKER_USERNAME and self.BROKER_PASSWORD:
            auth = f"{self.BROKER_USERNAME}:{self.BROKER_PASSWORD}@"

        return f"redis://{auth}{self.BROKER_HOST}:{self.BROKER_PORT}/{self.BROKER_DB}"
