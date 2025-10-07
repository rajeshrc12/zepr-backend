from sqlmodel import Session, select
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(session: Session, task_data: TaskCreate):
    task = Task(name=task_data.name)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_tasks(session: Session):
    return session.exec(select(Task)).all()


def get_task(session: Session, task_id: int):
    return session.get(Task, task_id)


def update_task(session: Session, task_id: int, task_data: TaskUpdate):
    task = session.get(Task, task_id)
    if not task:
        return None
    if task_data.name is not None:
        task.name = task_data.name
    if task_data.is_completed is not None:
        task.is_completed = task_data.is_completed
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task_id: int):
    task = session.get(Task, task_id)
    if not task:
        return None
    session.delete(task)
    session.commit()
    return True
