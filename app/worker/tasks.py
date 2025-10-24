from app.worker.providers import celery


@celery.task
def add(x, y):
    return x + y
