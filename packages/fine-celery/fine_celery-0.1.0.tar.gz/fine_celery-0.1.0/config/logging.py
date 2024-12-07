from typing import Dict, Any
from pydantic import Field
from .base import BaseConfig

class LoggingConfig(BaseConfig):
    """日志配置类"""
    
    # 日志级别
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    
    # Celery 日志配置
    CELERYD_LOG_FORMAT: str = Field(
        default="[%(asctime)s: %(levelname)s/%(processName)s] %(message)s",
        description="Celery worker log format"
    )
    CELERYD_TASK_LOG_FORMAT: str = Field(
        default="[%(asctime)s: %(levelname)s/%(processName)s] [%(task_name)s(%(task_id)s)] %(message)s",
        description="Celery task log format"
    ) 