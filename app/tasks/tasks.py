from app.core.celery_app import celery_app
from app.models.user import User
import time


@celery_app.task(name='task1')
def default_task():
    for user in User.select():
        print(user.username)
    return 'default task'


@celery_app.task(name='task2')
def long_task():
    for i in range(10):
        print(i)
    time.sleep(1)
    return 'long task'
