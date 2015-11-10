from celery import Celery, Task, shared_task
from celery.contrib import rdb
import redis
import time

app = Celery()
app.config_from_object('celeryconfig')


client = redis.StrictRedis(host='localhost', port=6379, db=1)


class CachedTask(Task):
    abstract = True

    def after_return(self, status, retval, *args, **kwargs):
        pass


@shared_task(base=CachedTask)
def cached_task(func, *args, **kwargs):
    cached_result = client.get("%s %s %s" % (func.func_name, args, kwargs))
    if cached_result:
        return cached_result
    else:
        return func(*args, **kwargs)


def add(a, b):
    return a + b
