from typing import Any
from pydantic_settings import BaseSettings

class BaseConfig(BaseSettings):
    """基础配置类，其他配置类继承自此类"""
    
    class Config:
        # 允许从环境变量读取配置
        env_file = ".env"
        env_file_encoding = "utf-8"
        # 大小写不敏感
        case_sensitive = False 