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


@shared_task(bind=True, base=CachedTask)
def cached_task(self, func, *args, **kwargs):
    self.func = func
    cached_result = client.get("%s %s %s" % (self.func.func_name, args, kwargs))
    if cached_result:
        return cached_result
    else:
        return self.func(*args, **kwargs)


def add(a, b):
    time.sleep(5)
    return a + b
