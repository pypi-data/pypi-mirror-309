from typing import Dict, Any, List, Optional
from pydantic import Field, validator
from .base import BaseConfig

class TaskConfig(BaseConfig):
    """Task 相关配置类
    
    包含所有与任务执行、路由、序列化、重试等相关的配置项：
    - 任务执行超时和限制
    - 序列化选项
    - 任务路由规则
    - 重试策略
    - 任务传播选项
    - 任务发布确认
    """
    
    # 任务执行配置
    TASK_TRACK_STARTED: bool = Field(
        default=True, 
        description="是否追踪任务的开始状态"
    )
    TASK_TIME_LIMIT: int = Field(
        default=3600, 
        description="任务硬超时时间(秒)，超过此时间任务会被强制终止"
    )
    TASK_SOFT_TIME_LIMIT: int = Field(
        default=3300, 
        description="任务软超时时间(秒)，超过此时间会抛出SoftTimeLimitExceeded异常"
    )
    TASK_IGNORE_RESULT: bool = Field(
        default=False,
        description="是否忽略任务结果"
    )
    
    # 序列化配置
    TASK_SERIALIZER: str = Field(
        default="json",
        description="任务序列化格式(json/pickle/yaml等)"
    )
    RESULT_SERIALIZER: str = Field(
        default="json",
        description="结果序列化格式"
    )
    ACCEPT_CONTENT: List[str] = Field(
        default=["json"],
        description="允许接收的内容类型列表"
    )
    
    # 任务路由配置
    TASK_DEFAULT_QUEUE: str = Field(
        default="celery",
        description="默认队列名称，未指定队列的任务将使用此队列"
    )
    TASK_DEFAULT_EXCHANGE: str = Field(
        default="default",
        description="默认交换机名称"
    )
    TASK_DEFAULT_ROUTING_KEY: str = Field(
        default="default",
        description="默认路由键"
    )
    TASK_ROUTES: Optional[Dict] = Field(
        default=None,
        description="任务路由规则配置"
    )
    
    # 任务重试配置
    TASK_RETRY_DELAY: int = Field(
        default=180,
        description="重试等待时间(秒)"
    )
    TASK_MAX_RETRIES: int = Field(
        default=3,
        description="最大重试次数"
    )
    
    # 任务传播选项
    TASK_ACKS_LATE: bool = Field(
        default=False,
        description="是否在任务执行完成后才确认消息"
    )
    TASK_REJECT_ON_WORKER_LOST: bool = Field(
        default=False,
        description="worker意外退出时是否拒绝任务"
    )
    
    # 任务发布确认
    TASK_PUBLISH_RETRY: bool = Field(
        default=True,
        description="发布任务失败时是否重试"
    )
    TASK_PUBLISH_RETRY_POLICY: Dict = Field(
        default={
            'max_retries': 3,
            'interval_start': 0,
            'interval_step': 0.2,
            'interval_max': 0.2,
        },
        description="任务发布重试策略"
    )
    
    @property
    def task_default_options(self) -> Dict[str, Any]:
        """获取任务默认选项配置
        
        将所有任务相关的配置项都作为默认选项，
        这样所有的任务都会继承这些配置
        """
        return {
            # 基础选项（没有对应配置项的选项）
            'bind': True,
            'retry_backoff': True,
            'retry_jitter': True,
            
            # 执行配置
            'track_started': self.TASK_TRACK_STARTED,
            'time_limit': self.TASK_TIME_LIMIT,
            'soft_time_limit': self.TASK_SOFT_TIME_LIMIT,
            'ignore_result': self.TASK_IGNORE_RESULT,
            
            # 序列化配置
            'serializer': self.TASK_SERIALIZER,
            
            # 重试配置
            'retry_delay': self.TASK_RETRY_DELAY,
            'max_retries': self.TASK_MAX_RETRIES,
            
            # 传播选项
            'acks_late': self.TASK_ACKS_LATE,
            'reject_on_worker_lost': self.TASK_REJECT_ON_WORKER_LOST,
            
            # 发布确认
            'publish_retry': self.TASK_PUBLISH_RETRY,
            'publish_retry_policy': self.TASK_PUBLISH_RETRY_POLICY,
            
            # 路由配置
            'queue': self.TASK_DEFAULT_QUEUE,
            'exchange': self.TASK_DEFAULT_EXCHANGE,
            'routing_key': self.TASK_DEFAULT_ROUTING_KEY,
        }