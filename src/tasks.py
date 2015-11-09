from celery import Celery, shared_task


app = Celery('tasks')
app.config_from_object('celeryconfig')


@shared_task
def add(x, y):
    return x + y
