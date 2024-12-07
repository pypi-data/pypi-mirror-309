import multiprocessing
from typing import Optional, Literal
from pydantic import Field
from .base import BaseConfig

class WorkerConfig(BaseConfig):
    """Worker 配置类
    
    包含所有与 Celery Worker 运行相关的配置：
    - 基础配置
    - 并发和池配置
    - 事件监控配置
    - 资源限制配置
    - 日志配置
    - 安全配置
    """
    
    # Worker 基础配置
    WORKER_NAME: str = Field(
        default="worker1@%h",
        description="Worker 名称，%h 会被替换为主机名"
    )
    
    WORKER_LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Worker 日志级别"
    )
    
    # 并发和池配置
    WORKER_CONCURRENCY: int = Field(
        default=0,  # 0 表示使用 CPU 核心数
        description="并发工作进程数，0表示使用CPU核心数"
    )
    
    WORKER_POOL: Literal["prefork", "eventlet", "gevent", "solo"] = Field(
        default="prefork",
        description="进程池类型：prefork(多进程)/eventlet/gevent(协程)/solo(单线程)。"
                   "prefork 适合 CPU 密集型任务；"
                   "eventlet/gevent 适合 I/O 密集型任务；"
                   "solo 适合开发和调试"
    )
    
    WORKER_POOL_RESTARTS: bool = Field(
        default=False,
        description="是否允许重启工作池。启用后，worker 可以在需要时自动重启进程池，"
                   "有助于处理内存泄漏，但可能影响性能"
    )
    
    # 事件监控配置
    WORKER_SEND_EVENTS: bool = Field(
        default=False,
        description="是否发送事件消息(-E 选项)。启用后，worker 会发送任务事件到消息队列，"
                   "可用于任务监控和调试，但会增加一些开销"
    )
    
    WORKER_EVENTS: bool = Field(
        default=False,
        description="是否启用事件通知。启用后可以接收来自其他 worker 的事件，"
                   "用于集群监控和管理"
    )
    
    WORKER_EVENT_QUEUE_TTL: int = Field(
        default=60,
        description="事件队列消息的TTL(秒)。超过此时间的事件消息将被丢弃，"
                   "防止事件队列无限增长"
    )
    
    WORKER_EVENT_QUEUE_EXPIRES: int = Field(
        default=60,
        description="事件队列的过期时间(秒)。如果队列在此时间内没有被消费，"
                   "整个队列将被删除"
    )
    
    # 资源限制配置
    WORKER_MAX_TASKS_PER_CHILD: Optional[int] = Field(
        default=None,
        description="每个子进程处理多少任务后自动重启。用于防止内存泄漏，"
                   "None 表示不限制。建议在长期运行的生产环境中设置此值"
    )
    
    WORKER_MAX_MEMORY_PER_CHILD: Optional[int] = Field(
        default=None,
        description="每个子进程最大内存限制(KB)。超过此限制的进程将被重启，"
                   "用于控制内存使用。None 表示不限制"
    )
    
    WORKER_TIME_LIMIT: Optional[int] = Field(
        default=None,
        description="任务硬时间限制(秒)"
    )
    
    WORKER_SOFT_TIME_LIMIT: Optional[int] = Field(
        default=None,
        description="任务软时间限制(秒)"
    )
    
    # 性能配置
    WORKER_PREFETCH_MULTIPLIER: int = Field(
        default=4,
        description="预取任务数量的乘数。决定每个进程可以预取的任务数量，"
                   "较大的值可以提高吞吐量，但可能导致任务分配不均衡"
    )
    
    WORKER_DISABLE_RATE_LIMITS: bool = Field(
        default=False,
        description="是否禁用任务速率限制。启用后将忽略任务的速率限制设置，"
                   "适用于需要最大吞吐量的场景"
    )
    
    WORKER_ENABLE_REMOTE_CONTROL: bool = Field(
        default=True,
        description="是否启用远程控制"
    )
    
    # 队列配置
    WORKER_QUEUES: list = Field(
        default=["celery", "monitor", "math"],
        description="要消费的队列列表。worker 只会从这些队列中获取任务，"
                   "可用于任务分流和优先级控制。包括：\n"
                   "- celery: 默认队列\n"
                   "- monitor: 监控相关任务队列\n"
                   "- math: 数学计算任务队列"
    )
    
    # 持久化配置
    WORKER_STATE_DB: Optional[str] = Field(
        default=None,
        description="状态数据库文件路径。用于保存 worker 的状态信息，"
                   "在 worker 重启后可以恢复。None 表示不保存状态"
    )
    
    # 安全配置
    WORKER_SECURITY_KEY: Optional[str] = Field(
        default=None,
        description="安全密钥。用于消息签名和认证，"
                   "建议在生产环境中设置"
    )
    
    WORKER_SECURITY_CERTIFICATE: Optional[str] = Field(
        default=None,
        description="安全证书路径。用于 SSL/TLS 连接，"
                   "提供服务器身份验证"
    )
    
    WORKER_SECURITY_CERT_STORE: Optional[str] = Field(
        default=None,
        description="证书存储路径。存储受信任的 CA 证书，"
                   "用于验证客户端证书"
    )

    # 用户和组配置
    WORKER_UID: Optional[int] = Field(
        default=None,
        description="Worker 进程的用户 ID。None 表示禁用 uid 检查，"
                   "用于降低权限相关的警告"
    )
    
    WORKER_GID: Optional[int] = Field(
        default=None,
        description="Worker 进程的组 ID。None 表示禁用 gid 检查，"
                   "用于降低权限相关的警告"
    )