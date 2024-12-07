from datetime import timedelta
from celery.schedules import crontab

# 定时任务调度配置
BEAT_SCHEDULES = {
    'heartbeat-every-10-seconds': {
        'task': 'example.tasks.heartbeat',
        'schedule': timedelta(seconds=3),
        # 'options': {
        #     'queue': 'monitor',
        #     'expires': 9  # 如果9秒内没有执行，则放弃该任务
        # }
    },
    
    # 示例：每天凌晨2点执行的任务
    # 'daily-number-addition': {
    #     'task': 'example.tasks.add_numbers',
    #     'schedule': crontab(hour=2, minute=0),
    #     'args': (10, 20),  # 传递给任务的参数
    #     'options': {
    #         'queue': 'math'
    #     }
    # }
} 