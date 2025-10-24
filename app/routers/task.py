from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.task import create_task, get_tasks, get_task, update_task, delete_task
from app.schemas.task import Task, TaskUpdate, TaskCreate
from app.worker.tasks import add

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=Task)
def add_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task"""
    return create_task(db, task)


@router.get("/", response_model=list[Task])
def read_tasks(db: Session = Depends(get_db)):
    """Retrieve all tasks"""
    return get_tasks(db)


@router.get("/add")
def call_add(x: int, y: int):
    task = add.delay(x, y)
    return {"task_id": task.id}


@router.get("/{task_id}", response_model=Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    """Retrieve a single task by ID"""
    db_task = get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.put("/{task_id}", response_model=Task)
def modify_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    """Update an existing task"""
    db_task = update_task(db, task_id, task)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.delete("/{task_id}", response_model=Task)
def remove_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task by ID"""
    db_task = delete_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
