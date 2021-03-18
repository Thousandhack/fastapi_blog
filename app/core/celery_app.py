# from celery import Celery
# from app.core.config import settings
# from kombu import Exchange, Queue
#
# celery_app = Celery('worker',
#                     broker=f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}")
#
# celery_app.conf.update(
#     timezone='Asia/Shanghai'
# )
#
# celery_app.conf.task_queues = (
#     Queue('fastapi_default', Exchange('fastapi_default'), routing_key='fastapi_default'),
#     Queue('fastapi_long', Exchange('fastapi_long'), routing_key='fastapi_long')
# )
#
# celery_app.conf.task_routes = {
#     'task1': {'queue': 'fastapi_default', 'routing_key': 'fastapi_default'},
#     'task2': {'queue': 'fastapi_long', 'routing_key': 'fastapi_long'},
#     '*': {'queue': 'fastapi_default', 'routing_key': 'fastapi_default'}
# }
#
# celery_app.conf.beat_schedule = {
#     'default_task': {
#         'task': 'task1',
#         'schedule': 5,
#         'args': (),
#     },
#     'long_task': {
#         'task': 'task2',
#         'schedule': 5,
#         'args': (),
#     },
# }
#
# celery_app.conf.task_default_queue = 'fastapi_default'
# celery_app.conf.task_default_exchange_type = 'direct'
# celery_app.conf.task_default_routing_key = 'fastapi_default'
#
