from celery import Celery, Task, shared_task
from celery.contrib import rdb
import redis
import time


app = Celery()
app.config_from_object('celeryconfig')
redis_client = redis.StrictRedis(host='localhost', port=6379, db=1)


class CachedTask(Task):
    abstract = True

    def after_return(self, status, retval, *args, **kwargs):
        pass

    def redis_key(self):
        return str({
            self.func.func_name:{
                "args": self.func_args,
                "kwargs": self.func_kwargs
            }
        })


@shared_task(bind=True, base=CachedTask)
def cached_task(self, func, *args, **kwargs):
    self.func = func
    self.func_args = args
    self.func_kwargs = kwargs
    cached_result = redis_client.get(self.redis_key())
    if cached_result:
        return cached_result
    else:
        return self.func(*args, **kwargs)


def add(a, b):
    time.sleep(5)
    return a + b
