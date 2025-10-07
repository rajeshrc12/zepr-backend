from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_session
from app.schemas.task import TaskCreate, TaskUpdate
from app.crud.task import (
    create_task,
    get_tasks,
    get_task,
    update_task,
    delete_task,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/")
def create_new_task(task_data: TaskCreate, session=Depends(get_session)):
    return create_task(session, task_data)


@router.get("/")
def list_tasks(session=Depends(get_session)):
    return get_tasks(session)


@router.get("/{task_id}")
def read_task(task_id: int, session=Depends(get_session)):
    task = get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}")
def update_existing_task(task_id: int, task_data: TaskUpdate, session=Depends(get_session)):
    task = update_task(session, task_id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}")
def remove_task(task_id: int, session=Depends(get_session)):
    success = delete_task(session, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"ok": True}
