from celery import Celery

celery = Celery(
    "celery_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["app.worker.tasks"]  # register all tasks here
)
