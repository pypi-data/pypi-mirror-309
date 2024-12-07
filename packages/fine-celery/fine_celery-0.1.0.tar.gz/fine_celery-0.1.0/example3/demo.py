from celery import Celery

from src.core.tasks import celery_app

celery_app = Celery()

redis_url = "redis://localhost:6379/0"

from kombu import Queue, Exchange

# 定义前缀


QUEUE_NAME = 'queue:heartbeat'

celery_app.conf.update({
    "broker_url": redis_url,
    "result_backend": redis_url,
    "broker_transport_options": {
        "global_keyprefix": "nice_celery:broker:",
        # "fanout_prefix": True,
        # "fanout_patterns": True,
    },
    "result_backend_transport_options": {
        'global_keyprefix': 'nice_celery:result:'
    },

    # 重要：注册队列
    "task_queues": (
        Queue(QUEUE_NAME),
    ),

    "beat_schedule": {
        "heartbeat-every-second": {
            "task": "example3.demo.heartbeat",
            "schedule": 1.0,
            'options': {'queue':QUEUE_NAME}
        }
    }



})

@celery_app.task(bind=True, queue=QUEUE_NAME)
def heartbeat(self):
    print("in heart beat")


"""
为什么没有用到redbeat


简单的定时任务不需要 Redbeat
需要动态管理定时任务时才使用 Redbeat
Redbeat 主要用于复杂的调度场景
Redbeat 提供了更灵活的任务调度管理


edbeat 是一个专门用于替代默认 Celery Beat 调度器的扩展，它使用 Redis 来存储调度信息。主要在以下场景使用：

需要动态修改定时任务时：
多个 Beat 实例需要协调时：
需要持久化调度配置时：


您当前的代码不需要 Redbeat 是因为：
调度配置是静态的（在代码中写死）
只有一个 Beat 实例
不需要动态修改定时任务
如果您需要以下功能，才需要考虑使用 Redbeat：
运行时动态添加/修改/删除定时任务
多个 Beat 实例协同工作
持久化调度配置
Web 界面管理定时任务
示例 - 使用 Redbeat 的完整代码：


"""

if __name__ == "__main__":
    # print(celery_app.conf)
    ...
