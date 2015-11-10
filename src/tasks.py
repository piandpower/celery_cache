from celery import Celery, shared_task


app = Celery('tasks')
app.config_from_object('celeryconfig')


@shared_task
def cached_task(function, *args, **kwargs):
    return function(*args, **kwargs)

def add(a, b):
    return a + b
