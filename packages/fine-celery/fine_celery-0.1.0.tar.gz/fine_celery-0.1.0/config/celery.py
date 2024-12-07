from typing import Dict, Any
from .broker import RedisBrokerConfig
from .backend import RedisBackendConfig
from .task import TaskConfig
from .logging import LoggingConfig
from .worker import WorkerConfig
from .beat import BeatConfig
from .singleton import SingletonConfig

class CeleryConfig:
    """Celery 配置整合类"""
    
    def __init__(self, external_config=None):
        self.broker_config = RedisBrokerConfig()
        self.backend_config = RedisBackendConfig()
        self.task_config = TaskConfig()
        self.logging_config = LoggingConfig()
        self.worker_config = WorkerConfig()
        self.beat_config = BeatConfig()
        self.singleton_config = SingletonConfig()
        self.external_config = external_config or {}

    
    def get_celery_config(self) -> Dict[str, Any]:
        """获取完整的 Celery 配置字典"""
        config = {}
        
        # 自动添加 broker 配置
        for field in self.broker_config.__fields__:
            config[field.lower()] = getattr(self.broker_config, field)
        # 特殊处理 broker_url
        config["broker_url"] = self.broker_config.broker_url
        
        # 自动添加 backend 配置
        for field in self.backend_config.__fields__:
            config[field.lower()] = getattr(self.backend_config, field)
        # 特殊处理 result_backend_url
        config["result_backend"] = self.backend_config.result_backend_url
        
        # 自动添加 task 配置
        for field in self.task_config.__fields__:
            config[field.lower()] = getattr(self.task_config, field)
        # 特殊处理 task_default_options
        config["task_default_options"] = self.task_config.task_default_options
        
        # 自动添加 worker 配置
        for field in self.worker_config.__fields__:
            config[field.lower()] = getattr(self.worker_config, field)
        
        # 自动添加 beat 配置
        for field in self.beat_config.__fields__:
            config[field.lower()] = getattr(self.beat_config, field)
        
        # 自动添加 logging 配置
        for field in self.logging_config.__fields__:
            config[field.lower()] = getattr(self.logging_config, field)
        
        # Result backend 配置
        config["result_expires"] = self.backend_config.RESULT_EXPIRES
        config["result_cache_max"] = self.backend_config.RESULT_CACHE_MAX
        config["result_serializer"] = self.backend_config.RESULT_SERIALIZER
        config["result_compression"] = self.backend_config.RESULT_COMPRESSION
        config["result_extended"] = self.backend_config.RESULT_EXTENDED
        config["redis_backend_use_ssl"] = self.backend_config.REDIS_BACKEND_USE_SSL
        config["redis_backend_health_check_interval"] = self.backend_config.REDIS_BACKEND_HEALTH_CHECK_INTERVAL
        
        # Redis backend 传输选项
        config["result_backend_transport_options"] = self.backend_config.backend_transport_options
        
        # 添加 singleton 配置
        config["singleton_backend_url"] = (
            self.singleton_config.SINGLETON_BACKEND_URL or 
            self.broker_config.broker_url
        )
        config["singleton_key_prefix"] = self.singleton_config.SINGLETON_KEY_PREFIX
        config["singleton_lock_expiry"] = self.singleton_config.SINGLETON_LOCK_EXPIRY
        config["singleton_raise_on_duplicate"] = self.singleton_config.SINGLETON_RAISE_ON_DUPLICATE
        
        # 使用外部配置覆盖默认配置
        if self.external_config:
            config.update(self.external_config)
            
        return config